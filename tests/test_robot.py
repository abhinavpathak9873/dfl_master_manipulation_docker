import unittest
from unittest.mock import patch

import dfl_toolbox as dfl
from dfl_toolbox.robots import ROBOTS


class RecordingArm:
    def __init__(self):
        self.moves = []

    def move_joints(self, target):
        self.moves.append(("joints", target))


class RecordingGripper:
    def open(self):
        return "open"


class RecordingCamera:
    def get_rgbd(self):
        return "rgb", "depth"


class RecordingPicker:
    def __init__(self, **selection):
        self.selection = selection
        self.arm = RecordingArm()
        self.gripper = RecordingGripper()
        self.camera = RecordingCamera()
        self.events = []

    def bringup(self):
        self.events.append("up")

    def bringdown(self):
        self.events.append("down")

    def ros_node(self):
        return "debug-node"


class RobotTests(unittest.TestCase):
    def test_robot_selects_and_exposes_real_structure(self):
        with patch.dict(
            ROBOTS,
            {("picker1", "gazebo"): RecordingPicker},
            clear=True,
        ):
            robot = dfl.Robot(
                model="picker1",
                mode="gazebo",
                gripper="vgc10",
                scene="empty",
            )
            robot.bringup()
            robot.arm.move_joints(dfl.Joints(0, 1))

        self.assertEqual(robot.implementation.events, ["up"])
        self.assertEqual(robot.camera.get_rgbd(), ("rgb", "depth"))
        self.assertEqual(robot.ros_node(), "debug-node")
        self.assertEqual(robot.implementation.selection["gripper"], "vgc10")
        with self.assertRaisesRegex(AttributeError, "no 'base'"):
            _ = robot.base

    def test_context_manager_bringup_and_bringdown(self):
        with patch.dict(
            ROBOTS,
            {("picker1", "gazebo"): RecordingPicker},
            clear=True,
        ):
            with dfl.Robot(model="picker1", mode="gazebo") as robot:
                self.assertEqual(robot.implementation.events, ["up"])

        self.assertEqual(robot.implementation.events, ["up", "down"])


if __name__ == "__main__":
    unittest.main()
