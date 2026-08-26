"""Task-facing perception objects over direct implementation mappings."""

from __future__ import annotations

from typing import Any

from dfl_toolbox._backends import build_backend, invoke_backend

from .alignment import LOCAL_ALIGNERS
from .pose import POSE_ESTIMATORS
from .segmentation import SEGMENTERS
from .tracking import TRACKERS


class _BackendFacade:
    capability: str
    mapping_file: str
    backends: dict[str, Any]

    def __init__(self, *, backend: str, **options: Any) -> None:
        self.backend, self.implementation = build_backend(
            capability=self.capability,
            backend=backend,
            backends=self.backends,
            mapping_file=self.mapping_file,
            options=options,
        )

    def _invoke(self, method: str, *args: Any, **kwargs: Any) -> Any:
        return invoke_backend(
            self.implementation,
            capability=self.capability,
            backend=self.backend,
            method=method,
            args=args,
            kwargs=kwargs,
        )

    def __getattr__(self, name: str) -> Any:
        """Expose backend-specific operations without widening the common seam."""

        implementation = self.__dict__.get("implementation")
        if implementation is None:
            raise AttributeError(name)
        return getattr(implementation, name)


class Segmenter(_BackendFacade):
    capability = "segmentation"
    mapping_file = "dfl_toolbox/perception/segmentation/__init__.py"
    backends = SEGMENTERS

    def segment(self, image: Any, **kwargs: Any) -> Any:
        return self._invoke("segment", image, **kwargs)


class PoseEstimator(_BackendFacade):
    capability = "pose estimation"
    mapping_file = "dfl_toolbox/perception/pose/__init__.py"
    backends = POSE_ESTIMATORS

    def estimate(self, **kwargs: Any) -> Any:
        return self._invoke("estimate", **kwargs)


class Tracker(_BackendFacade):
    capability = "tracking"
    mapping_file = "dfl_toolbox/perception/tracking/__init__.py"
    backends = TRACKERS

    def initialize(self, **kwargs: Any) -> Any:
        return self._invoke("initialize", **kwargs)

    def update(self, **kwargs: Any) -> Any:
        return self._invoke("update", **kwargs)

    def reset(self) -> Any:
        return self._invoke("reset")


class LocalAlignment(_BackendFacade):
    capability = "local alignment"
    mapping_file = "dfl_toolbox/perception/alignment/__init__.py"
    backends = LOCAL_ALIGNERS

    def compute(self, **kwargs: Any) -> Any:
        return self._invoke("compute", **kwargs)
