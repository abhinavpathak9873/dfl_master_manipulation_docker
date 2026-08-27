from __future__ import annotations

import itertools
from pathlib import Path
import sys
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / ".devcontainer/src/dfl_manipulation_toolbox"
sys.path.insert(0, str(PACKAGE))

from dfl_manipulation_toolbox.profiles import ProfileError, Selection, resolve, validate_all


class Phase00Tests(unittest.TestCase):
    def test_profiles_define_exact_24_case_matrix(self):
        with (ROOT / "config/phase0_matrix.yaml").open() as stream:
            matrix = yaml.safe_load(stream)
        cases = list(itertools.product(matrix["modes"], matrix["robots"], matrix["tools"]))
        self.assertEqual(24, len(cases))
        self.assertEqual(24, len({"-".join(case) for case in cases}))
        self.assertEqual([], validate_all(PACKAGE / "config"))
        for mode, robot, tool in cases:
            resolved = resolve(Selection(robot, tool, mode), PACKAGE / "config")
            self.assertEqual(mode, resolved["selection"].mode_id)

    def test_invalid_ids_fail_with_choices(self):
        with self.assertRaisesRegex(ProfileError, "unknown robot"):
            resolve(Selection("picker3", "2fg14", "gazebo"), PACKAGE / "config")

    def test_source_revisions_are_full_git_shas(self):
        with (ROOT / "dependencies.repos").open() as stream:
            repositories = yaml.safe_load(stream)["repositories"]
        self.assertEqual({"doosan-robot2", "moveit2_calibration"}, set(repositories))
        for specification in repositories.values():
            revision = specification["version"]
            self.assertEqual(40, len(revision))
            int(revision, 16)

    def test_real_mode_is_never_commissioned_by_default(self):
        with (PACKAGE / "config/robots.yaml").open() as stream:
            robots = yaml.safe_load(stream)["robots"]
        self.assertTrue(all(robot["commissioning"] == "not_yet_verified" for robot in robots.values()))
        self.assertIn("DFL_REAL_MOTION_ENABLED", (ROOT / "tasks/phase0_fixed_task.py").read_text())

    def test_description_has_each_tool_and_both_arm_models(self):
        text = (PACKAGE / "urdf/dfl_robot.urdf.xacro").read_text()
        for identifier in ("m1013", "h2515", "vgc10_1cup", "vgc10_4cup", "vgp20", "2fg14"):
            self.assertIn(identifier, text)


if __name__ == "__main__":
    unittest.main()
