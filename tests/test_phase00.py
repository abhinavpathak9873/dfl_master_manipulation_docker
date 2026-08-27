from __future__ import annotations

import hashlib
import itertools
from pathlib import Path
import struct
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

    def test_picker_mesh_assets_match_accepted_workspace_inputs(self):
        expected = {
            "picker1/base.stl": "b0c5c0fb5c3c7a5e28fb66b7a3d1a4bd20356e1d1251e04575eb072349ed1224",
            "picker2/base.stl": "5aedfda5e0a13f9cc0fa8e72f3584c76e5e72a807e10a6618c8c85c115fbb5c1",
            "tools/vgc10_1cup.dae": "17d717e91bfac3c06e7cdbc8ae6fdfde5d730fcc0d0fd271c0e35ed53ad90554",
            "tools/vgc10_4cup.dae": "4c91ab76e4cb772713f4eed9bc0e3db14553211617a7f9fd88ba620ef1eacd85",
            "tools/vgp20.dae": "564547d9526c03477a90193b6cda1a09bd161028c8c6398c7e35806f1d5c7d4e",
            "camera/hand_camera_mount.dae": "bf1c7754ad3d8dcc313a82b3b2c91ab431009d9d63ecde04e0e0cd914704bc00",
        }
        for relative, digest in expected.items():
            contents = (PACKAGE / "meshes" / relative).read_bytes()
            self.assertEqual(digest, hashlib.sha256(contents).hexdigest(), relative)

    def test_checked_gallery_contains_exact_visual_matrix(self):
        gallery = ROOT / "docs/phase_00/gallery"
        expected = {
            gallery / mode / f"{robot}-{tool}.png"
            for mode, robot, tool in itertools.product(
                ("genesis", "gazebo"),
                ("picker1", "picker2", "h2515"),
                ("vgc10_1cup", "vgc10_4cup", "vgp20", "2fg14"),
            )
        }
        actual = set(gallery.glob("*/*.png"))
        self.assertEqual(expected, actual)
        for path in actual:
            data = path.read_bytes()
            self.assertEqual(b"\x89PNG\r\n\x1a\n", data[:8], path)
            width, height = struct.unpack(">II", data[16:24])
            self.assertEqual((1280, 960), (width, height), path)

    def test_gazebo_declares_project_mesh_resource_paths(self):
        compose = (ROOT / ".devcontainer/docker-compose.gazebo.yml").read_text()
        self.assertIn("GZ_SIM_RESOURCE_PATH", compose)
        self.assertIn("dfl_manipulation_toolbox/share", compose)

    def test_gallery_scene_is_packaged(self):
        setup = (PACKAGE / "setup.py").read_text()
        self.assertIn('scenes/gallery', setup)
        self.assertTrue((PACKAGE / "scenes/gallery/world.sdf").is_file())

    def test_genesis_camera_parent_covers_direct_mount_tools(self):
        bridge = (
            ROOT / ".devcontainer/src/dfl_genesis_integration/"
            "dfl_genesis_integration/bridge.py"
        ).read_text()
        self.assertIn('CAMERA_MOUNT_TOOLS = {"vgc10_4cup", "2fg14"}', bridge)
        self.assertIn('else "link_6"', bridge)


if __name__ == "__main__":
    unittest.main()
