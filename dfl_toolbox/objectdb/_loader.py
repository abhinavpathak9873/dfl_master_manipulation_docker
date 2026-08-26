"""Read ObjectDB assets directly from ordinary files."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import json
import os
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any

from dfl_toolbox.errors import (
    InvalidObjectError,
    MissingAssetError,
    ObjectNotFoundError,
)
from dfl_toolbox.values import Pose

from ._models import AssetMap, GraspAnchor, GraspAnchors, ObjectAsset

_OBJECT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")


def _objects_root(root: str | os.PathLike[str] | None) -> Path:
    if root is not None:
        return Path(root).expanduser().resolve()
    configured = os.environ.get("DFL_OBJECTS_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path.cwd() / "objects").resolve()


def _read_json(path: Path, *, label: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ObjectNotFoundError(f"{label} was not found at {path}.") from exc
    except json.JSONDecodeError as exc:
        raise InvalidObjectError(
            f"{label} at {path} is not valid JSON: line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}."
        ) from exc


def _mapping(value: Any, *, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise InvalidObjectError(f"{field} must be a JSON object.")
    return value


def _safe_asset(object_root: Path, value: Any, *, field: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise InvalidObjectError(f"{field} must be a non-empty relative path.")
    relative = Path(value)
    if relative.is_absolute():
        raise InvalidObjectError(f"{field} must be relative to {object_root}.")
    resolved = (object_root / relative).resolve()
    try:
        resolved.relative_to(object_root)
    except ValueError as exc:
        raise InvalidObjectError(
            f"{field} escapes the object directory: {value!r}."
        ) from exc
    if not resolved.exists():
        raise MissingAssetError(f"{field} references missing asset {resolved}.")
    return resolved


def _pose(value: Any, *, field: str, default_frame: str) -> Pose:
    record = _mapping(value, field=field)
    try:
        return Pose(
            position=record["position"],
            quaternion=record.get("quaternion", (0.0, 0.0, 0.0, 1.0)),
            frame=record.get("frame", default_frame),
        )
    except KeyError as exc:
        raise InvalidObjectError(f"{field} requires position.") from exc
    except (TypeError, ValueError) as exc:
        raise InvalidObjectError(f"{field} is invalid: {exc}") from exc


def _grasp_records(object_root: Path, record: Mapping[str, Any]) -> list[Any]:
    if "grasp_anchors" in record:
        value = record["grasp_anchors"]
    else:
        grasp_file = object_root / "grasps.json"
        if not grasp_file.exists():
            return []
        value = _read_json(grasp_file, label="grasp record")
        if isinstance(value, Mapping):
            value = value.get("grasp_anchors", [])
    if not isinstance(value, list):
        raise InvalidObjectError("grasp_anchors must be a JSON array.")
    return value


def _anchors(
    object_root: Path, object_id: str, record: Mapping[str, Any]
) -> GraspAnchors:
    anchors: list[GraspAnchor] = []
    seen: set[str] = set()
    for index, value in enumerate(_grasp_records(object_root, record)):
        anchor = _mapping(value, field=f"grasp_anchors[{index}]")
        anchor_id = anchor.get("id")
        if not isinstance(anchor_id, str) or not anchor_id.strip():
            raise InvalidObjectError(
                f"grasp_anchors[{index}].id must be a non-empty string."
            )
        if anchor_id in seen:
            raise InvalidObjectError(f"Duplicate grasp anchor ID {anchor_id!r}.")
        seen.add(anchor_id)
        pose_value = anchor.get("pose", anchor)
        pose = _pose(
            pose_value,
            field=f"grasp_anchors[{index}].pose",
            default_frame=object_id,
        )
        metadata = {
            key: item
            for key, item in anchor.items()
            if key not in {"id", "pose", "position", "quaternion", "frame"}
        }
        anchors.append(
            GraspAnchor(
                id=anchor_id,
                pose=pose,
                metadata=MappingProxyType(metadata),
            )
        )
    return GraspAnchors(anchors)


def load(
    object_id: str | Sequence[str],
    *,
    root: str | os.PathLike[str] | None = None,
) -> ObjectAsset | list[ObjectAsset]:
    """Load one object, or a list of objects, from local files."""

    if not isinstance(object_id, str) and isinstance(object_id, Sequence):
        return [load(item, root=root) for item in object_id]
    if not isinstance(object_id, str) or not _OBJECT_ID.fullmatch(object_id):
        raise InvalidObjectError(
            "object_id must use letters, numbers, '.', '_', or '-' and cannot "
            "contain a path."
        )
    objects_root = _objects_root(root)
    object_root = (objects_root / object_id).resolve()
    try:
        object_root.relative_to(objects_root)
    except ValueError as exc:
        raise InvalidObjectError(f"Object ID {object_id!r} escapes {objects_root}.") from exc
    if not object_root.is_dir():
        raise ObjectNotFoundError(
            f"Object {object_id!r} was not found under {objects_root}."
        )

    record_path = object_root / "object.json"
    record = _mapping(
        _read_json(record_path, label=f"object record for {object_id!r}"),
        field="object record",
    )
    record_id = record.get("id")
    if record_id != object_id:
        raise InvalidObjectError(
            f"Object directory {object_id!r} contains record ID {record_id!r}."
        )

    mesh = (
        None
        if record.get("mesh") is None
        else _safe_asset(object_root, record["mesh"], field="mesh")
    )

    model_record = _mapping(record.get("models", {}), field="models")
    models = AssetMap(
        {
            name: _safe_asset(object_root, value, field=f"models.{name}")
            for name, value in model_record.items()
        }
    )

    frame_record = _mapping(
        record.get("reference_frames", {}), field="reference_frames"
    )
    reference_frames = MappingProxyType(
        {
            name: _pose(value, field=f"reference_frames.{name}", default_frame=object_id)
            for name, value in frame_record.items()
        }
    )

    annotations = MappingProxyType(
        dict(_mapping(record.get("annotations", {}), field="annotations"))
    )
    raw = MappingProxyType(dict(record))

    return ObjectAsset(
        id=object_id,
        root=object_root,
        mesh=mesh,
        models=models,
        grasp_anchors=_anchors(object_root, object_id, record),
        reference_frames=reference_frames,
        dimensions=record.get("dimensions"),
        annotations=annotations,
        raw=raw,
    )


def validate(
    object_id: str,
    *,
    root: str | os.PathLike[str] | None = None,
) -> None:
    """Validate an object by loading its complete declared runtime surface."""

    load(object_id, root=root)
