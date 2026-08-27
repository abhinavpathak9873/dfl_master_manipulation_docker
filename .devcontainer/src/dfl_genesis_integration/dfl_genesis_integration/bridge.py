"""A direct, inspectable Genesis-to-ROS bridge for one DFL robot."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import signal
import subprocess
import tempfile
from threading import Lock, Thread
import time
import xml.etree.ElementTree as ET

import genesis as gs
import numpy as np
import rclpy
import torch
import trimesh
from ament_index_python.packages import get_package_share_directory
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.executors import MultiThreadedExecutor
from rosgraph_msgs.msg import Clock
from sensor_msgs.msg import CameraInfo, Image, JointState
from std_msgs.msg import Bool


JOINTS = [f"joint_{index}" for index in range(1, 7)]
HOME = [0.0, 0.0, 1.5708, 0.0, 1.5708, 0.0]
CAMERA_MOUNT_TOOLS = {"vgc10_4cup", "2fg14"}


def expanded_urdf(robot: str, model: str, tool: str) -> Path:
    share = Path(get_package_share_directory("dfl_manipulation_toolbox"))
    description = share / "urdf" / "dfl_robot.urdf.xacro"
    command = ["xacro", str(description), f"robot:={robot}", f"arm_model:={model}", f"tool:={tool}",
               f"namespace:={robot}", "control_backend:=none"]
    output = subprocess.run(command, check=True, text=True, capture_output=True).stdout
    dsr_share = get_package_share_directory("dsr_description2")
    dfl_share = get_package_share_directory("dfl_manipulation_toolbox")
    output = output.replace("package://dsr_description2", dsr_share)
    output = output.replace("package://dfl_manipulation_toolbox", dfl_share)
    document = ET.fromstring(output)
    for joint in document.findall("joint"):
        if joint.get("type") not in {"continuous", "prismatic", "revolute"}:
            continue
        dynamics = joint.find("dynamics")
        if dynamics is None:
            dynamics = ET.SubElement(joint, "dynamics")
        # Genesis' legacy URDF path treats an omitted damping value as an
        # object-typed array, which cannot initialize the rigid solver.
        dynamics.set("damping", dynamics.get("damping", "0.1"))
    for link in document.findall("link"):
        for shape in link.findall("collision"):
            geometry = shape.find("geometry")
            mesh = geometry.find("mesh") if geometry is not None else None
            if mesh is None:
                continue
            source = Path(mesh.get("filename"))
            if source.suffix.lower() == ".dae":
                mesh.set("filename", str(_cached_collision_stl(source)))
    output = ET.tostring(document, encoding="unicode")
    path = Path(tempfile.gettempdir()) / f"dfl_{robot}_{tool}_genesis.urdf"
    path.write_text(output, encoding="utf-8")
    return path


def _cached_collision_stl(source: Path) -> Path:
    """Convert a DAE collision mesh once; Genesis still renders the source visual."""
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    cache = Path.home() / ".cache/dfl_genesis/collision_meshes"
    cache.mkdir(parents=True, exist_ok=True)
    output = cache / f"{digest}.stl"
    if output.exists():
        return output
    loaded = trimesh.load(source, force="mesh", process=False)
    if not isinstance(loaded, trimesh.Trimesh) or loaded.is_empty:
        raise RuntimeError(f"could not convert collision mesh {source}")
    temporary = output.with_suffix(".tmp.stl")
    loaded.export(temporary, file_type="stl")
    temporary.replace(output)
    return output


class RosBridge:
    def __init__(self, robot_name: str, entity, joint_indices: list[int], camera=None) -> None:
        rclpy.init()
        self.node = rclpy.create_node("genesis_bridge", namespace=robot_name)
        self.robot_name = robot_name
        self.entity = entity
        self.joint_indices = joint_indices
        self.camera = camera
        self.measured = dict(zip(JOINTS, HOME))
        self.target = list(HOME)
        self.lock = Lock()
        self.updates = 0
        self.sim_time = 0.0
        self.joints = self.node.create_publisher(JointState, "joint_states", 10)
        self.clock = self.node.create_publisher(Clock, "/clock", 10)
        self.ready = self.node.create_publisher(Bool, "ready", 10)
        self.color = self.node.create_publisher(Image, "camera/color/image_raw", 2) if camera else None
        self.depth = self.node.create_publisher(Image, "camera/depth/image_rect_raw", 2) if camera else None
        self.camera_info = self.node.create_publisher(CameraInfo, "camera/color/camera_info", 2) if camera else None
        self.server = ActionServer(
            self.node, FollowJointTrajectory, "dsr_position_controller/follow_joint_trajectory",
            execute_callback=self._execute, goal_callback=self._goal,
            cancel_callback=lambda _: CancelResponse.ACCEPT,
        )
        self.executor = MultiThreadedExecutor(num_threads=3)
        self.executor.add_node(self.node)
        self.thread = Thread(target=self.executor.spin, daemon=True)
        self.thread.start()

    def _goal(self, request):
        if request.trajectory.joint_names != JOINTS or not request.trajectory.points:
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def _execute(self, goal_handle):
        point = goal_handle.request.trajectory.points[-1]
        requested = list(point.positions)
        if len(requested) != 6:
            goal_handle.abort()
            result = FollowJointTrajectory.Result()
            result.error_code = FollowJointTrajectory.Result.INVALID_GOAL
            return result
        with self.lock:
            self.target = requested
        duration = point.time_from_start.sec + point.time_from_start.nanosec / 1e9
        deadline = time.monotonic() + max(5.0, duration + 3.0)
        result = FollowJointTrajectory.Result()
        while time.monotonic() < deadline:
            if goal_handle.is_cancel_requested:
                with self.lock:
                    self.target = [self.measured[name] for name in JOINTS]
                goal_handle.canceled()
                result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                return result
            with self.lock:
                measured = dict(self.measured)
            if self.updates > 2 and all(abs(measured[name] - value) < 0.035 for name, value in zip(JOINTS, requested)):
                goal_handle.succeed()
                result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                return result
            time.sleep(0.02)
        goal_handle.abort()
        result.error_code = FollowJointTrajectory.Result.GOAL_TOLERANCE_VIOLATED
        result.error_string = f"Genesis articulation did not reach target; measured={measured}, target={requested}"
        return result

    def update(self, sim_time: float) -> None:
        self.sim_time = sim_time
        positions = self.entity.get_dofs_position(self.joint_indices).detach().cpu().reshape(-1).tolist()
        velocities = self.entity.get_dofs_velocity(self.joint_indices).detach().cpu().reshape(-1).tolist()
        with self.lock:
            self.measured = dict(zip(JOINTS, positions))
            target = list(self.target)
        self.entity.control_dofs_position(target, self.joint_indices)
        stamp = _time_message(sim_time)
        joint_state = JointState()
        joint_state.header.stamp = stamp
        joint_state.name = JOINTS
        joint_state.position = positions
        joint_state.velocity = velocities
        self.joints.publish(joint_state)
        clock = Clock()
        clock.clock = stamp
        self.clock.publish(clock)
        ready = Bool()
        ready.data = True
        self.ready.publish(ready)
        self.updates += 1

    def render_camera(self) -> None:
        if not self.camera:
            return
        rgb, depth, _, _ = self.camera.render(rgb=True, depth=True, segmentation=False, normal=False, force_render=True)
        rgb = np.asarray(rgb.detach().cpu() if hasattr(rgb, "detach") else rgb, dtype=np.uint8)
        depth = np.asarray(depth.detach().cpu() if hasattr(depth, "detach") else depth, dtype=np.float32)
        stamp = _time_message(self.sim_time)
        color = Image()
        color.header.stamp = stamp
        color.header.frame_id = "camera_color_optical_frame"
        color.height, color.width = rgb.shape[:2]
        color.encoding = "rgb8"
        color.step = color.width * 3
        color.data = rgb[:, :, :3].tobytes()
        depth_message = Image()
        depth_message.header = color.header
        depth_message.height, depth_message.width = depth.shape[:2]
        depth_message.encoding = "32FC1"
        depth_message.step = depth_message.width * 4
        depth_message.data = depth.tobytes()
        info = CameraInfo()
        info.header = color.header
        info.height, info.width = color.height, color.width
        focal = info.width / (2.0 * np.tan(np.deg2rad(42.5) / 2.0))
        info.k = [focal, 0.0, info.width / 2.0, 0.0, focal, info.height / 2.0, 0.0, 0.0, 1.0]
        self.color.publish(color)
        self.depth.publish(depth_message)
        self.camera_info.publish(info)

    def close(self) -> None:
        self.executor.shutdown(timeout_sec=2.0)
        self.thread.join(timeout=2.0)
        self.node.destroy_node()
        rclpy.shutdown()


def _time_message(seconds: float):
    from builtin_interfaces.msg import Time
    message = Time()
    message.sec = int(seconds)
    message.nanosec = int((seconds - int(seconds)) * 1_000_000_000)
    return message


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot", required=True, choices=("picker1", "picker2", "h2515"))
    parser.add_argument("--model", required=True, choices=("m1013", "h2515"))
    parser.add_argument("--tool", required=True, choices=("vgc10_1cup", "vgc10_4cup", "vgp20", "2fg14"))
    parser.add_argument("--backend", choices=("auto", "cuda", "cpu"), default="auto")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--smoke-steps", type=int, default=0)
    args, _ = parser.parse_known_args()
    if args.backend == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but torch.cuda.is_available() is false")
    using_cuda = args.backend == "cuda" or (args.backend == "auto" and torch.cuda.is_available())
    backend = gs.cuda if using_cuda else gs.cpu
    gs.init(backend=backend, precision="32", logging_level="warning")
    scene = gs.Scene(
        sim_options=gs.options.SimOptions(dt=0.005, substeps=2),
        rigid_options=gs.options.RigidOptions(enable_self_collision=False),
        viewer_options=gs.options.ViewerOptions(camera_pos=(3.5, -3.5, 2.5), camera_lookat=(0, 0, 0.8)),
        show_viewer=not args.headless,
    )
    scene.add_entity(gs.morphs.Plane())
    urdf = expanded_urdf(args.robot, args.model, args.tool)
    entity = scene.add_entity(gs.morphs.URDF(
        file=str(urdf), fixed=True, merge_fixed_links=False,
        convexify=True, decimate=True, decimate_face_num=500,
    ))
    camera = None
    if args.robot.startswith("picker"):
        camera = scene.add_camera(res=(640, 480), fov=42.5, GUI=False, near=0.05, far=10.0)
    scene.build()
    indices = [entity.get_joint(name).dofs_idx_local[0] for name in JOINTS]
    entity.set_dofs_kp([25000.0] * 6, indices)
    entity.set_dofs_kv([500.0] * 6, indices)
    entity.set_dofs_position(HOME, indices, zero_velocity=True)
    entity.control_dofs_position(HOME, indices)
    if camera:
        # The workspace camera plate is in the visual chain only for these two
        # Picker tools. Direct-mount tools still expose the same RGB-D contract,
        # so their simulated sensor is anchored at the flange until a current
        # serial-specific hand-eye calibration supplies the real transform.
        camera_parent = "camera_mount" if args.tool in CAMERA_MOUNT_TOOLS else "link_6"
        camera.attach(entity.get_link(camera_parent), np.eye(4, dtype=np.float32))
    bridge = RosBridge(args.robot, entity, indices, camera)
    running = True
    def stop(*_):
        nonlocal running
        running = False
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    steps = 0
    started = time.monotonic()
    while running and (not args.smoke_steps or steps < args.smoke_steps):
        step_started = time.monotonic()
        scene.step()
        steps += 1
        bridge.update(steps * 0.005)
        if camera and steps % 13 == 0:
            bridge.render_camera()
        time.sleep(max(0.0, 0.005 - (time.monotonic() - step_started)))
    elapsed = time.monotonic() - started
    bridge.close()
    print(json.dumps({
        "robot": args.robot,
        "tool": args.tool,
        "steps": steps,
        "wall_seconds": elapsed,
        "mean_update_hz": steps / elapsed if elapsed else 0.0,
        "backend": "cuda" if using_cuda else "cpu",
        "gpu_memory_allocated_mb": round(torch.cuda.max_memory_allocated() / 1024**2, 1) if using_cuda else 0.0,
        "gpu_memory_reserved_mb": round(torch.cuda.max_memory_reserved() / 1024**2, 1) if using_cuda else 0.0,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
