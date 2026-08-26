import unittest
from unittest.mock import patch

import dfl_toolbox as dfl
from dfl_toolbox.errors import BackendInterfaceError, BackendNotFoundError
from dfl_toolbox.perception.segmentation import SEGMENTERS
from dfl_toolbox.perception.tracking import TRACKERS


class TinySegmenter:
    def __init__(self, *, model):
        self.model = model
        self.calls = 0

    def segment(self, image, *, prompt=None):
        self.calls += 1
        return {"image": image, "prompt": prompt, "model": self.model}

    def debug_render(self):
        return f"debug:{self.calls}"


class TinyTracker:
    def __init__(self, *, object):
        self.object = object
        self.pose = None

    def initialize(self, *, pose, **_inputs):
        self.pose = pose

    def update(self, **_inputs):
        return self.pose

    def reset(self):
        self.pose = None


class BackendTests(unittest.TestCase):
    def test_folder_constructor_accepts_filename_style_backend(self):
        with patch.dict(SEGMENTERS, {"tiny": TinySegmenter}, clear=True):
            segmenter = dfl.perception.segmentation.create(
                backend="tiny.py",
                model="tiny.engine",
            )

            first = segmenter.segment("rgb", prompt="tray")
            second = segmenter.segment("rgb-2")

        self.assertEqual(first["model"], "tiny.engine")
        self.assertEqual(second["image"], "rgb-2")
        self.assertEqual(segmenter.debug_render(), "debug:2")
        self.assertIs(segmenter.implementation, segmenter.implementation)

    def test_unknown_backend_names_mapping_file(self):
        with patch.dict(SEGMENTERS, {}, clear=True):
            with self.assertRaises(BackendNotFoundError) as raised:
                dfl.perception.segmentation.create(backend="missing.py")

        self.assertIn(
            "dfl_toolbox/perception/segmentation/__init__.py",
            str(raised.exception),
        )

    def test_missing_capability_method_is_clear(self):
        with patch.dict(SEGMENTERS, {"broken": lambda: object()}, clear=True):
            segmenter = dfl.perception.Segmenter(backend="broken")
            with self.assertRaisesRegex(BackendInterfaceError, "segment"):
                segmenter.segment("rgb")

    def test_state_lives_in_tracker_backend(self):
        pose = dfl.Pose(1, 2, 3, frame="odom")
        with patch.dict(TRACKERS, {"tiny": TinyTracker}, clear=True):
            tracker = dfl.perception.tracking.create(
                backend="tiny",
                object="small_tray",
            )
            tracker.initialize(rgb="rgb", depth="depth", pose=pose)
            self.assertEqual(tracker.update(rgb="next", depth="next"), pose)
            tracker.reset()
            self.assertIsNone(tracker.update())


if __name__ == "__main__":
    unittest.main()
