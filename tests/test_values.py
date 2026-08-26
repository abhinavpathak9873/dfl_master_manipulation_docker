import math
import unittest

from dfl_toolbox import Joints, Pose


class PoseTests(unittest.TestCase):
    def test_sequence_and_positional_forms_match(self):
        sequence = Pose(
            position=[1, 2, 3],
            quaternion=[0, 0, 0, 2],
            frame="odom",
        )
        positional = Pose(1, 2, 3, q=[0, 0, 0, 1], frame="odom")

        self.assertEqual(sequence, positional)
        self.assertEqual(positional.position, (1.0, 2.0, 3.0))
        self.assertEqual(positional.q, (0.0, 0.0, 0.0, 1.0))

    def test_parent_and_tool_offsets_are_explicit(self):
        quarter_turn = math.sqrt(0.5)
        pose = Pose(
            1,
            2,
            3,
            q=[0, 0, quarter_turn, quarter_turn],
            frame="odom",
        )

        self.assertEqual(pose.offset(x=0.1).position, (1.1, 2.0, 3.0))
        tool_offset = pose.offset(x=0.1, relative_to="tool")
        self.assertAlmostEqual(tool_offset.x, 1.0)
        self.assertAlmostEqual(tool_offset.y, 2.1)
        self.assertAlmostEqual(tool_offset.z, 3.0)

    def test_compose_transforms_child_pose(self):
        quarter_turn = math.sqrt(0.5)
        parent = Pose(
            1,
            2,
            3,
            q=[0, 0, quarter_turn, quarter_turn],
            frame="world",
        )
        child = Pose(0.2, 0, 0, frame="object")

        result = parent.compose(child)

        self.assertAlmostEqual(result.x, 1.0)
        self.assertAlmostEqual(result.y, 2.2)
        self.assertAlmostEqual(result.z, 3.0)
        self.assertEqual(result.frame, "world")

    def test_invalid_pose_fails_clearly(self):
        with self.assertRaisesRegex(ValueError, "quaternion cannot be zero"):
            Pose(0, 0, 0, q=[0, 0, 0, 0], frame="odom")
        with self.assertRaisesRegex(ValueError, "frame"):
            Pose(0, 0, 0, frame="")


class JointsTests(unittest.TestCase):
    def test_iterable_and_positional_forms(self):
        iterable = Joints([0, 90], unit="deg")
        positional = Joints(0, 90, unit="deg")

        self.assertEqual(iterable, positional)
        self.assertAlmostEqual(positional.values[1], math.pi / 2)
        self.assertEqual(positional.as_unit("deg"), (0.0, 90.0))

    def test_names_are_validated(self):
        with self.assertRaisesRegex(ValueError, "same length"):
            Joints([0, 1], names=["joint_1"])
        with self.assertRaisesRegex(ValueError, "unique"):
            Joints([0, 1], names=["joint_1", "joint_1"])


if __name__ == "__main__":
    unittest.main()
