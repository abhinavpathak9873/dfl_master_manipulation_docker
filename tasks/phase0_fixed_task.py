#!/usr/bin/env python3
"""Run the small Phase 00 task against one declared simulator selection."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import time
import xml.etree.ElementTree as ET

import numpy as np


JOINTS = [f"joint_{index}" for index in range(1, 7)]
HOME = [0.0, 0.0, 1.5708, 0.0, 1.5708, 0.0]
PROBE = [0.10, -0.08, 1.48, 0.06, 1.50, -0.05]


def _transform(xyz, rpy):
    roll, pitch, yaw = rpy
    cr, sr = np.cos(roll), np.sin(roll)
    cp, sp = np.cos(pitch), np.sin(pitch)
    cy, sy = np.cos(yaw), np.sin(yaw)
    rotation = np.array([
        [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
        [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
        [-sp, cp * sr, cp * cr],
    ])
    result = np.eye(4)
    result[:3, :3] = rotation
    result[:3, 3] = xyz
    return result


def _axis_rotation(axis, angle):
    axis = np.asarray(axis, dtype=float)
    axis /= np.linalg.norm(axis)
    cross = np.array([
        [0.0, -axis[2], axis[1]],
        [axis[2], 0.0, -axis[0]],
        [-axis[1], axis[0], 0.0],
    ])
    result = np.eye(4)
    result[:3, :3] = np.eye(3) + np.sin(angle) * cross + (1.0 - np.cos(angle)) * (cross @ cross)
    return result


def _expanded_chain(robot, tool):
    from ament_index_python.packages import get_package_share_directory

    model = "h2515" if robot == "h2515" else "m1013"
    description = Path(get_package_share_directory("dfl_manipulation_toolbox")) / "urdf/dfl_robot.urdf.xacro"
    output = subprocess.run([
        "xacro", str(description), f"robot:={robot}", f"arm_model:={model}", f"tool:={tool}",
        f"namespace:={robot}", "control_backend:=none",
    ], check=True, capture_output=True, text=True).stdout
    document = ET.fromstring(output)
    by_child = {}
    for joint in document.findall("joint"):
        child = joint.find("child").get("link")
        origin = joint.find("origin")
        xyz = [float(value) for value in (origin.get("xyz", "0 0 0") if origin is not None else "0 0 0").split()]
        rpy = [float(value) for value in (origin.get("rpy", "0 0 0") if origin is not None else "0 0 0").split()]
        axis_element = joint.find("axis")
        axis = [float(value) for value in (axis_element.get("xyz", "1 0 0") if axis_element is not None else "1 0 0").split()]
        limit = joint.find("limit")
        by_child[child] = {
            "name": joint.get("name"), "type": joint.get("type"),
            "parent": joint.find("parent").get("link"), "origin": _transform(xyz, rpy), "axis": axis,
            "lower": float(limit.get("lower", "-6.2832")) if limit is not None else -6.2832,
            "upper": float(limit.get("upper", "6.2832")) if limit is not None else 6.2832,
        }
    chain = []
    link = "tool_tcp"
    while link != "base_link":
        if link not in by_child:
            raise RuntimeError(f"description has no base_link -> tool_tcp chain at {link}")
        joint = by_child[link]
        chain.append(joint)
        link = joint["parent"]
    return list(reversed(chain))


def _forward(chain, positions):
    values = dict(zip(JOINTS, positions))
    result = np.eye(4)
    for joint in chain:
        result = result @ joint["origin"]
        if joint["type"] in {"continuous", "revolute"}:
            result = result @ _axis_rotation(joint["axis"], values[joint["name"]])
    return result


def _relative_tcp_target(chain, positions, distance_m=0.02):
    positions = np.asarray(positions, dtype=float)
    start = _forward(chain, positions)
    target = start[:3, 3] + start[:3, :3] @ np.array([0.0, 0.0, distance_m])
    movable = {joint["name"]: joint for joint in chain if joint["name"] in JOINTS}
    lower = np.array([movable[name]["lower"] for name in JOINTS])
    upper = np.array([movable[name]["upper"] for name in JOINTS])
    result = positions.copy()
    epsilon = 1e-5
    for _ in range(80):
        current = _forward(chain, result)[:3, 3]
        error = target - current
        if np.linalg.norm(error) < 0.0004:
            return result.tolist(), target
        jacobian = np.empty((3, 6))
        for index in range(6):
            offset = result.copy()
            offset[index] += epsilon
            jacobian[:, index] = (_forward(chain, offset)[:3, 3] - current) / epsilon
        delta = jacobian.T @ np.linalg.solve(jacobian @ jacobian.T + 1e-5 * np.eye(3), error)
        result = np.clip(result + np.clip(delta, -0.025, 0.025), lower, upper)
    raise RuntimeError("relative TCP inverse kinematics did not converge")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot", required=True, choices=("picker1", "picker2", "h2515"))
    parser.add_argument("--tool", required=True, choices=("vgc10_1cup", "vgc10_4cup", "vgp20", "2fg14"))
    parser.add_argument("--mode", required=True, choices=("gazebo", "genesis", "real"))
    parser.add_argument("--scene", default="empty")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--describe", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.mode == "real" and os.environ.get("DFL_REAL_MOTION_ENABLED") != "1":
        raise SystemExit("real motion refused: run scripts/real_mode_guard.sh after current-session authorization")
    from dfl_manipulation_toolbox.profiles import Selection, resolve
    resolved = resolve(Selection(args.robot, args.tool, args.mode, args.scene))
    summary = {
        "robot": args.robot, "tool": args.tool, "mode": args.mode, "scene": args.scene,
        "controller": resolved["robot"]["controller"], "started_at_unix": time.time(),
    }
    if args.describe:
        summary["status"] = "description_valid"
        print(json.dumps(summary, sort_keys=True))
        return

    import rclpy
    from control_msgs.action import FollowJointTrajectory
    from geometry_msgs.msg import Twist
    from nav_msgs.msg import Odometry
    from rclpy.action import ActionClient
    from rclpy.node import Node
    from sensor_msgs.msg import Image, JointState
    from std_msgs.msg import Bool, String
    from trajectory_msgs.msg import JointTrajectoryPoint

    class TaskNode(Node):
        def __init__(self):
            super().__init__("phase0_fixed_task")
            prefix = f"/{args.robot}"
            self.action = ActionClient(self, FollowJointTrajectory, prefix + "/dsr_position_controller/follow_joint_trajectory")
            self.tool = self.create_publisher(String, prefix + "/tool/command", 10)
            self.base = self.create_publisher(Twist, prefix + "/cmd_vel", 10)
            self.last_joint = self.last_tool = self.last_odom = self.last_image = self.ready = None
            self.create_subscription(JointState, prefix + "/joint_states", lambda msg: setattr(self, "last_joint", msg), 10)
            self.create_subscription(String, prefix + "/tool/state", lambda msg: setattr(self, "last_tool", msg), 10)
            self.create_subscription(Odometry, prefix + "/odom", lambda msg: setattr(self, "last_odom", msg), 10)
            self.create_subscription(Image, prefix + "/camera/color/image_raw", lambda msg: setattr(self, "last_image", msg), 2)
            self.create_subscription(Bool, prefix + "/ready", lambda msg: setattr(self, "ready", msg.data), 10)

        def wait_for(self, predicate, label):
            deadline = time.monotonic() + args.timeout
            while time.monotonic() < deadline:
                rclpy.spin_once(self, timeout_sec=0.1)
                if predicate():
                    return
            raise RuntimeError(f"timed out waiting for {label}")

        def move(self, positions, seconds=1.5):
            if not self.action.wait_for_server(timeout_sec=args.timeout):
                raise RuntimeError(f"trajectory action unavailable: {self.action._action_name}")
            goal = FollowJointTrajectory.Goal()
            goal.trajectory.joint_names = JOINTS
            point = JointTrajectoryPoint()
            point.positions = positions
            point.time_from_start.sec = int(seconds)
            point.time_from_start.nanosec = int((seconds % 1) * 1e9)
            goal.trajectory.points = [point]
            future = self.action.send_goal_async(goal)
            rclpy.spin_until_future_complete(self, future, timeout_sec=args.timeout)
            handle = future.result()
            if not handle or not handle.accepted:
                raise RuntimeError("trajectory goal rejected")
            result = handle.get_result_async()
            rclpy.spin_until_future_complete(self, result, timeout_sec=args.timeout)
            response = result.result()
            if response is None or response.result.error_code != FollowJointTrajectory.Result.SUCCESSFUL:
                raise RuntimeError(f"trajectory failed: {response}")

        def cancel_probe(self):
            goal = FollowJointTrajectory.Goal()
            goal.trajectory.joint_names = JOINTS
            point = JointTrajectoryPoint()
            # The preceding motion ends at PROBE.  Cancel toward the distinct
            # HOME target so a fast simulator cannot report success before the
            # cancellation request is exercised.
            point.positions = HOME
            point.time_from_start.sec = 5
            goal.trajectory.points = [point]
            future = self.action.send_goal_async(goal)
            rclpy.spin_until_future_complete(self, future, timeout_sec=args.timeout)
            handle = future.result()
            if not handle or not handle.accepted:
                raise RuntimeError("cancel probe was rejected")
            cancel = handle.cancel_goal_async()
            rclpy.spin_until_future_complete(self, cancel, timeout_sec=args.timeout)
            if not cancel.result() or not cancel.result().goals_canceling:
                raise RuntimeError("controller did not accept cancel")

    rclpy.init()
    node = TaskNode()
    try:
        node.wait_for(lambda: node.ready is True and node.last_joint is not None, "ready joint state")
        node.move(HOME)
        node.move(PROBE)
        chain = _expanded_chain(args.robot, args.tool)
        current = {name: value for name, value in zip(node.last_joint.name, node.last_joint.position)}
        relative_joints, relative_target = _relative_tcp_target(chain, [current[name] for name in JOINTS])
        node.move(relative_joints)
        relative_error = float("inf")
        deadline = time.monotonic() + args.timeout
        while time.monotonic() < deadline:
            rclpy.spin_once(node, timeout_sec=0.05)
            measured = {name: value for name, value in zip(node.last_joint.name, node.last_joint.position)}
            relative_error = float(np.linalg.norm(
                _forward(chain, [measured[name] for name in JOINTS])[:3, 3] - relative_target
            ))
            if relative_error <= 0.004:
                break
        else:
            raise RuntimeError(
                f"relative TCP probe missed target by {relative_error:.6f} m; "
                f"commanded_joints={relative_joints}, measured_joints="
                f"{[measured[name] for name in JOINTS]}"
            )
        command = String()
        command.data = json.dumps({"operation": "grip" if args.tool == "2fg14" else "vacuum_on", "width_m": 0.03})
        node.tool.publish(command)
        node.wait_for(lambda: node.last_tool is not None, "tool command acknowledgement")
        tool_state = json.loads(node.last_tool.data)
        if not tool_state.get("accepted"):
            raise RuntimeError(f"tool command rejected: {tool_state}")
        if args.robot.startswith("picker"):
            node.wait_for(lambda: node.last_image is not None and node.last_odom is not None, "camera and base state")
            stop = Twist()
            node.base.publish(stop)
        node.cancel_probe()
        stop_tool = String()
        stop_tool.data = json.dumps({"operation": "stop"})
        node.tool.publish(stop_tool)
        summary.update({
            "status": "passed", "joint_count": len(node.last_joint.name),
            "tool_feedback": tool_state, "camera_checked": args.robot.startswith("picker"),
            "base_checked": args.robot.startswith("picker"), "cancel_checked": True,
            "relative_tcp_checked": True, "relative_tcp_error_m": relative_error,
            "finished_at_unix": time.time(),
        })
        print(json.dumps(summary, sort_keys=True))
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
