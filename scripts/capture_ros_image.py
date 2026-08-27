#!/usr/bin/env python3
"""Save the first useful ROS Image message as a PNG."""

from __future__ import annotations

import argparse
from pathlib import Path

from cv_bridge import CvBridge
import numpy as np
from PIL import Image
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image as ImageMessage


class Capture(Node):
    def __init__(self, topic: str, output: Path) -> None:
        super().__init__("dfl_gallery_capture")
        self.output = output
        self.bridge = CvBridge()
        self.saved = False
        self.create_subscription(ImageMessage, topic, self.on_image, 1)

    def on_image(self, message: ImageMessage) -> None:
        array = self.bridge.imgmsg_to_cv2(message, desired_encoding="rgb8")
        pixels = np.asarray(array, dtype=np.uint8)
        if pixels.size == 0 or float(pixels.std()) < 1.0:
            return
        self.output.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(pixels).save(self.output, optimize=True)
        self.saved = True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("topic")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rclpy.init()
    node = Capture(args.topic, args.output)
    while rclpy.ok() and not node.saved:
        rclpy.spin_once(node, timeout_sec=1.0)
    node.destroy_node()
    rclpy.shutdown()
    print(args.output)


if __name__ == "__main__":
    main()
