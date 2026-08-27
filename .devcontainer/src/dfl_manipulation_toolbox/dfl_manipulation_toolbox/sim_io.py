"""Honest simulator-only tool, planar-base, and readiness state.

This node does not pretend to model suction, grip force, or object retention.
It echoes accepted tool commands and integrates planar odometry so task and
diagnostic paths can be exercised consistently in both simulators.
"""

from __future__ import annotations

import argparse
import json
import math

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image
from std_msgs.msg import Bool, String


class SimulatorIo(Node):
    def __init__(self, robot: str, tool: str, has_base: bool, publish_camera: bool) -> None:
        super().__init__("sim_io", namespace=robot)
        self.robot = robot
        self.tool = tool
        self.has_base = has_base
        self.x = self.y = self.yaw = 0.0
        self.linear = self.angular = 0.0
        self.last_command_ns = self.get_clock().now().nanoseconds
        self.tool_state = self.create_publisher(String, "tool/state", 10)
        self.ready = self.create_publisher(Bool, "ready", 10)
        self.create_subscription(String, "tool/command", self._tool_command, 10)
        if publish_camera and robot.startswith("picker"):
            self.color = self.create_publisher(Image, "camera/color/image_raw", 2)
            self.depth = self.create_publisher(Image, "camera/depth/image_rect_raw", 2)
            self.camera_info = self.create_publisher(CameraInfo, "camera/color/camera_info", 2)
            self.create_timer(1.0 / 15.0, self._publish_camera)
        if has_base:
            self.odom = self.create_publisher(Odometry, "odom", 10)
            self.create_subscription(Twist, "cmd_vel", self._cmd_vel, 10)
        self.create_timer(0.02, self._update)
        self.create_timer(0.5, self._publish_ready)

    def _tool_command(self, message: String) -> None:
        try:
            command = json.loads(message.data)
        except json.JSONDecodeError:
            command = {"operation": message.data}
        operation = command.get("operation")
        allowed = {"vacuum_on", "release", "stop"}
        if self.tool == "2fg14":
            allowed |= {"set_width", "grip"}
        if operation not in allowed:
            state = {"accepted": False, "reason": f"unsupported operation {operation!r}"}
        else:
            state = {"accepted": True, "tool": self.tool, "commanded": command, "measured": False}
        response = String()
        response.data = json.dumps(state, sort_keys=True)
        self.tool_state.publish(response)

    def _cmd_vel(self, message: Twist) -> None:
        self.linear = max(-0.25, min(0.25, message.linear.x))
        self.angular = max(-0.5, min(0.5, message.angular.z))
        self.last_command_ns = self.get_clock().now().nanoseconds

    def _publish_ready(self) -> None:
        message = Bool()
        message.data = True
        self.ready.publish(message)

    def _update(self) -> None:
        if not self.has_base:
            return
        now = self.get_clock().now()
        if now.nanoseconds - self.last_command_ns > 250_000_000:
            self.linear = self.angular = 0.0
        dt = 0.02
        self.yaw += self.angular * dt
        self.x += self.linear * math.cos(self.yaw) * dt
        self.y += self.linear * math.sin(self.yaw) * dt
        message = Odometry()
        message.header.stamp = now.to_msg()
        message.header.frame_id = f"{self.robot}_odom"
        message.child_frame_id = f"{self.robot}_base_footprint"
        message.pose.pose.position.x = self.x
        message.pose.pose.position.y = self.y
        message.pose.pose.orientation.w = math.cos(self.yaw / 2.0)
        message.pose.pose.orientation.z = math.sin(self.yaw / 2.0)
        message.twist.twist.linear.x = self.linear
        message.twist.twist.angular.z = self.angular
        self.odom.publish(message)

    def _publish_camera(self) -> None:
        """Publish a deterministic calibration target, not photorealistic sensor data."""
        width, height = 640, 480
        now = self.get_clock().now().to_msg()
        row = bytes((40 if (column // 40) % 2 else 180 for column in range(width) for _ in range(3)))
        color = Image()
        color.header.stamp = now
        color.header.frame_id = "camera_color_optical_frame"
        color.height, color.width = height, width
        color.encoding = "rgb8"
        color.step = width * 3
        color.data = row * height
        depth = Image()
        depth.header = color.header
        depth.height, depth.width = height, width
        depth.encoding = "32FC1"
        depth.step = width * 4
        import struct
        depth.data = struct.pack("<f", 1.0) * width * height
        info = CameraInfo()
        info.header = color.header
        info.height, info.width = height, width
        info.k = [615.0, 0.0, width / 2.0, 0.0, 615.0, height / 2.0, 0.0, 0.0, 1.0]
        self.color.publish(color)
        self.depth.publish(depth)
        self.camera_info.publish(info)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot", required=True, choices=("picker1", "picker2", "h2515"))
    parser.add_argument("--tool", required=True, choices=("vgc10_1cup", "vgc10_4cup", "vgp20", "2fg14"))
    parser.add_argument("--publish-camera", action="store_true")
    args, _ = parser.parse_known_args()
    rclpy.init()
    node = SimulatorIo(args.robot, args.tool, args.robot.startswith("picker"), args.publish_camera)
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
