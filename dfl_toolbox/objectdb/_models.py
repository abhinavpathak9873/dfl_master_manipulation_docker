"""Values returned by local ObjectDB loading."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from dfl_toolbox.values import Pose


class AssetMap(Mapping[str, Path]):
    """Named asset paths with both mapping and attribute access."""

    def __init__(self, values: Mapping[str, Path] | None = None) -> None:
        self._values = MappingProxyType(dict(values or {}))

    def __getitem__(self, key: str) -> Path:
        return self._values[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def __getattr__(self, name: str) -> Path:
        try:
            return self._values[name]
        except KeyError as exc:
            available = ", ".join(sorted(self._values)) or "none"
            raise AttributeError(
                f"No object model named {name!r}. Available models: {available}."
            ) from exc


@dataclass(frozen=True)
class GraspAnchor:
    """A named TCP pose expressed in the object's frame."""

    id: str
    pose: Pose
    metadata: Mapping[str, Any]


class GraspAnchors(Sequence[GraspAnchor]):
    """An immutable anchor collection with local world-pose transformation."""

    def __init__(self, anchors: Sequence[GraspAnchor] = ()) -> None:
        self._anchors = tuple(anchors)

    def __getitem__(self, index: int | slice) -> GraspAnchor | tuple[GraspAnchor, ...]:
        return self._anchors[index]

    def __len__(self) -> int:
        return len(self._anchors)

    def transform(self, object_pose: Pose) -> tuple[Pose, ...]:
        if not isinstance(object_pose, Pose):
            raise TypeError("object_pose must be a Pose")
        return tuple(object_pose.compose(anchor.pose) for anchor in self._anchors)


@dataclass(frozen=True)
class ObjectAsset:
    """Useful local data produced by ObjectDB for one physical object."""

    id: str
    root: Path
    mesh: Path | None
    models: AssetMap
    grasp_anchors: GraspAnchors
    reference_frames: Mapping[str, Pose]
    dimensions: Any
    annotations: Mapping[str, Any]
    raw: Mapping[str, Any]
