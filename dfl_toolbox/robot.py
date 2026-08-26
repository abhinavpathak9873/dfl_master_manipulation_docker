"""Convenience robot construction without a hidden runtime."""

from __future__ import annotations

from typing import Any

from ._backends import build_backend, invoke_backend
from .errors import BackendInterfaceError
from .robots import ROBOTS


def _selector(value: str, *, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip().lower()


class Robot:
    """Select and expose one concrete composite robot adapter."""

    def __init__(
        self,
        *,
        model: str,
        mode: str,
        gripper: str | None = None,
        scene: str | None = None,
        **options: Any,
    ) -> None:
        self.model = _selector(model, name="model")
        self.mode = _selector(mode, name="mode")
        self.gripper_id = (
            None if gripper is None else _selector(gripper, name="gripper")
        )
        self.scene = None if scene is None else _selector(scene, name="scene")
        key = (self.model, self.mode)
        factories = {
            f"{robot_model}:{robot_mode}": factory
            for (robot_model, robot_mode), factory in ROBOTS.items()
        }
        backend_id, implementation = build_backend(
            capability="robot",
            backend=f"{self.model}:{self.mode}",
            backends=factories,
            mapping_file="dfl_toolbox/robots/__init__.py",
            options={
                "model": self.model,
                "mode": self.mode,
                "gripper": self.gripper_id,
                "scene": self.scene,
                **options,
            },
        )
        self.backend = backend_id
        self.implementation = implementation

    def _part(self, name: str) -> Any:
        try:
            return getattr(self.implementation, name)
        except AttributeError as exc:
            raise AttributeError(
                f"Robot {self.model!r} in mode {self.mode!r} has no {name!r} "
                "subassembly."
            ) from exc

    @property
    def arm(self) -> Any:
        return self._part("arm")

    @property
    def left_arm(self) -> Any:
        return self._part("left_arm")

    @property
    def right_arm(self) -> Any:
        return self._part("right_arm")

    @property
    def gripper(self) -> Any:
        return self._part("gripper")

    @property
    def camera(self) -> Any:
        return self._part("camera")

    @property
    def base(self) -> Any:
        return self._part("base")

    def bringup(self) -> Any:
        return invoke_backend(
            self.implementation,
            capability="robot",
            backend=self.backend,
            method="bringup",
            args=(),
            kwargs={},
        )

    def bringdown(self) -> Any:
        return invoke_backend(
            self.implementation,
            capability="robot",
            backend=self.backend,
            method="bringdown",
            args=(),
            kwargs={},
        )

    def __enter__(self) -> "Robot":
        self.bringup()
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        try:
            self.bringdown()
        except BackendInterfaceError:
            if exc is None:
                raise

    def __getattr__(self, name: str) -> Any:
        """Expose honest adapter-specific functionality for debugging."""

        if name in {"arm", "left_arm", "right_arm", "gripper", "camera", "base"}:
            return self._part(name)
        implementation = self.__dict__.get("implementation")
        if implementation is None:
            raise AttributeError(name)
        return getattr(implementation, name)
