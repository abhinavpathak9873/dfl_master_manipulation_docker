#!/usr/bin/env python3
"""Run the small Phase 00 task against one declared simulator selection."""

from __future__ import annotations

import argparse
import json
import os
import time


JOINTS = [f"joint_{index}" for index in range(1, 7)]
HOME = [0.0, 0.0, 1.5708, 0.0, 1.5708, 0.0]
PROBE = [0.10, -0.08, 1.48, 0.06, 1.50, -0.05]


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
            "finished_at_unix": time.time(),
        })
        print(json.dumps(summary, sort_keys=True))
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
