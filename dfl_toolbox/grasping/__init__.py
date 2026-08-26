"""Algorithmic grasp generation behind one small direct mapping."""

from __future__ import annotations

from typing import Any

from dfl_toolbox._backends import BackendFactory, build_backend, invoke_backend

GRASP_GENERATORS: dict[str, BackendFactory] = {}


class GraspGenerator:
    def __init__(self, *, backend: str, **options: Any) -> None:
        self.backend, self.implementation = build_backend(
            capability="grasp generation",
            backend=backend,
            backends=GRASP_GENERATORS,
            mapping_file="dfl_toolbox/grasping/__init__.py",
            options=options,
        )

    def compute(self, **kwargs: Any) -> Any:
        return invoke_backend(
            self.implementation,
            capability="grasp generation",
            backend=self.backend,
            method="compute",
            args=(),
            kwargs=kwargs,
        )

    def __getattr__(self, name: str) -> Any:
        implementation = self.__dict__.get("implementation")
        if implementation is None:
            raise AttributeError(name)
        return getattr(implementation, name)


__all__ = ["GRASP_GENERATORS", "GraspGenerator"]
