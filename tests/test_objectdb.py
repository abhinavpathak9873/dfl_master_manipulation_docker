import json
import math
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import dfl_toolbox as dfl
from dfl_toolbox.errors import (
    InvalidObjectError,
    MissingAssetError,
    ObjectNotFoundError,
)


class ObjectDBTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.objects_root = Path(self.temporary.name)
        self.object_root = self.objects_root / "small_tray"
        (self.object_root / "models").mkdir(parents=True)
        (self.object_root / "mesh.glb").write_bytes(b"mesh")
        (self.object_root / "models" / "segmentation.engine").write_bytes(b"model")
        self.record = {
            "id": "small_tray",
            "mesh": "mesh.glb",
            "models": {"segmentation": "models/segmentation.engine"},
            "dimensions": {"x": 0.3, "y": 0.2, "z": 0.05},
            "annotations": {"material": "plastic"},
            "grasp_anchors": [
                {
                    "id": "top",
                    "pose": {
                        "position": [0.1, 0, 0],
                        "quaternion": [0, 0, 0, 1],
                        "frame": "small_tray",
                    },
                    "tool": "vgc10",
                }
            ],
        }
        self._write_record()

    def tearDown(self):
        self.temporary.cleanup()

    def _write_record(self):
        (self.object_root / "object.json").write_text(
            json.dumps(self.record),
            encoding="utf-8",
        )

    def test_loads_local_assets_and_attribute_models(self):
        tray = dfl.objectdb.load("small_tray", root=self.objects_root)

        self.assertEqual(tray.id, "small_tray")
        self.assertEqual(tray.mesh, self.object_root / "mesh.glb")
        self.assertEqual(
            tray.models.segmentation,
            self.object_root / "models" / "segmentation.engine",
        )
        self.assertEqual(tray.grasp_anchors[0].metadata["tool"], "vgc10")
        self.assertEqual(tray.annotations["material"], "plastic")

    def test_transforms_object_frame_grasps_locally(self):
        quarter_turn = math.sqrt(0.5)
        tray = dfl.objectdb.load("small_tray", root=self.objects_root)
        object_pose = dfl.Pose(
            1,
            2,
            3,
            q=[0, 0, quarter_turn, quarter_turn],
            frame="odom",
        )

        grasp = tray.grasp_anchors.transform(object_pose)[0]

        self.assertAlmostEqual(grasp.x, 1.0)
        self.assertAlmostEqual(grasp.y, 2.1)
        self.assertAlmostEqual(grasp.z, 3.0)
        self.assertEqual(grasp.frame, "odom")

    def test_environment_root_is_supported(self):
        with patch.dict(
            os.environ,
            {"DFL_OBJECTS_ROOT": str(self.objects_root)},
            clear=False,
        ):
            tray = dfl.objectdb.load("small_tray")

        self.assertEqual(tray.root, self.object_root)

    def test_list_load_is_a_small_convenience(self):
        objects = dfl.objectdb.load(["small_tray"], root=self.objects_root)

        self.assertEqual([item.id for item in objects], ["small_tray"])

    def test_missing_object_and_asset_are_clear(self):
        with self.assertRaises(ObjectNotFoundError):
            dfl.objectdb.load("not_here", root=self.objects_root)

        self.record["mesh"] = "missing.glb"
        self._write_record()
        with self.assertRaisesRegex(MissingAssetError, "missing.glb"):
            dfl.objectdb.load("small_tray", root=self.objects_root)

    def test_asset_path_cannot_escape_object_directory(self):
        (self.objects_root / "outside.glb").write_bytes(b"outside")
        self.record["mesh"] = "../outside.glb"
        self._write_record()

        with self.assertRaisesRegex(InvalidObjectError, "escapes"):
            dfl.objectdb.load("small_tray", root=self.objects_root)

    def test_object_id_cannot_be_a_path(self):
        with self.assertRaisesRegex(InvalidObjectError, "cannot contain a path"):
            dfl.objectdb.load("../small_tray", root=self.objects_root)


if __name__ == "__main__":
    unittest.main()
