"""Lightweight robotics values with no ROS dependency."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


def _finite_tuple(values: Iterable[float], *, length: int, name: str) -> tuple[float, ...]:
    try:
        parsed = tuple(float(value) for value in values)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must contain {length} numeric values") from exc
    if len(parsed) != length:
        raise ValueError(f"{name} must contain exactly {length} values")
    if not all(math.isfinite(value) for value in parsed):
        raise ValueError(f"{name} values must be finite")
    return parsed


def _normalize_quaternion(values: Iterable[float]) -> tuple[float, float, float, float]:
    x, y, z, w = _finite_tuple(values, length=4, name="quaternion")
    norm = math.sqrt(x * x + y * y + z * z + w * w)
    if norm <= 1.0e-12:
        raise ValueError("quaternion cannot be zero")
    return x / norm, y / norm, z / norm, w / norm


def _quaternion_multiply(
    left: Iterable[float], right: Iterable[float]
) -> tuple[float, float, float, float]:
    lx, ly, lz, lw = _normalize_quaternion(left)
    rx, ry, rz, rw = _normalize_quaternion(right)
    return _normalize_quaternion(
        (
            lw * rx + lx * rw + ly * rz - lz * ry,
            lw * ry - lx * rz + ly * rw + lz * rx,
            lw * rz + lx * ry - ly * rx + lz * rw,
            lw * rw - lx * rx - ly * ry - lz * rz,
        )
    )


def _rotate(
    quaternion: Iterable[float], vector: Iterable[float]
) -> tuple[float, float, float]:
    x, y, z, w = _normalize_quaternion(quaternion)
    vx, vy, vz = _finite_tuple(vector, length=3, name="vector")
    tx = 2.0 * (y * vz - z * vy)
    ty = 2.0 * (z * vx - x * vz)
    tz = 2.0 * (x * vy - y * vx)
    return (
        vx + w * tx + (y * tz - z * ty),
        vy + w * ty + (z * tx - x * tz),
        vz + w * tz + (x * ty - y * tx),
    )


@dataclass(frozen=True)
class Pose:
    """A pose in metres with an explicit parent frame."""

    position: tuple[float, float, float]
    quaternion: tuple[float, float, float, float]
    frame: str

    def __init__(
        self,
        position: Iterable[float] | float,
        y: float | None = None,
        z: float | None = None,
        quaternion: Iterable[float] | None = None,
        *,
        frame: str,
        q: Iterable[float] | None = None,
    ) -> None:
        if not isinstance(frame, str) or not frame.strip():
            raise ValueError("frame must be a non-empty string")
        if isinstance(position, (int, float)):
            if y is None or z is None:
                raise ValueError("x, y, and z are all required for positional Pose input")
            parsed_position: Iterable[float] = (position, y, z)
        else:
            if y is not None or z is not None:
                raise ValueError(
                    "pass Pose position as either [x, y, z] or three positional values"
                )
            parsed_position = position
        if quaternion is not None and q is not None:
            raise ValueError("pass quaternion or q, not both")
        orientation = quaternion if quaternion is not None else q
        if orientation is None:
            orientation = (0.0, 0.0, 0.0, 1.0)
        object.__setattr__(
            self,
            "position",
            _finite_tuple(parsed_position, length=3, name="position"),
        )
        object.__setattr__(self, "quaternion", _normalize_quaternion(orientation))
        object.__setattr__(self, "frame", frame.strip())

    @property
    def x(self) -> float:
        return self.position[0]

    @property
    def y(self) -> float:
        return self.position[1]

    @property
    def z(self) -> float:
        return self.position[2]

    @property
    def q(self) -> tuple[float, float, float, float]:
        return self.quaternion

    def offset(
        self,
        *,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        relative_to: str = "parent",
    ) -> "Pose":
        """Return a translated copy in the parent or tool coordinate frame."""

        delta = _finite_tuple((x, y, z), length=3, name="offset")
        if relative_to == "tool":
            delta = _rotate(self.quaternion, delta)
        elif relative_to not in {"parent", self.frame}:
            raise ValueError(
                f"relative_to must be 'parent', 'tool', or {self.frame!r}"
            )
        return Pose(
            position=tuple(
                current + change
                for current, change in zip(self.position, delta, strict=True)
            ),
            quaternion=self.quaternion,
            frame=self.frame,
        )

    def compose(self, child: "Pose") -> "Pose":
        """Compose this parent pose with a child-frame pose."""

        if not isinstance(child, Pose):
            raise TypeError("child must be a Pose")
        translated = _rotate(self.quaternion, child.position)
        return Pose(
            position=tuple(
                parent + offset
                for parent, offset in zip(self.position, translated, strict=True)
            ),
            quaternion=_quaternion_multiply(self.quaternion, child.quaternion),
            frame=self.frame,
        )


@dataclass(frozen=True)
class Joints:
    """An ordered joint configuration normalized to radians."""

    values: tuple[float, ...]
    names: tuple[str, ...]
    unit: str = "rad"

    def __init__(
        self,
        values: Iterable[float] | float,
        *additional_values: float,
        names: Iterable[str] | None = None,
        unit: str = "rad",
    ) -> None:
        try:
            if isinstance(values, (int, float)):
                parsed = tuple(float(value) for value in (values, *additional_values))
            else:
                if additional_values:
                    raise ValueError(
                        "pass joint values as either one iterable or positional numbers"
                    )
                parsed = tuple(float(value) for value in values)
        except (TypeError, ValueError) as exc:
            if isinstance(exc, ValueError) and str(exc).startswith("pass joint values"):
                raise
            raise ValueError("joint values must be numeric") from exc
        if not parsed:
            raise ValueError("at least one joint value is required")
        if not all(math.isfinite(value) for value in parsed):
            raise ValueError("joint values must be finite")

        normalized_unit = unit.strip().lower() if isinstance(unit, str) else ""
        if normalized_unit in {"deg", "degree", "degrees"}:
            parsed = tuple(math.radians(value) for value in parsed)
        elif normalized_unit not in {"rad", "radian", "radians"}:
            raise ValueError(f"unsupported joint unit {unit!r}; use 'rad' or 'deg'")

        parsed_names = tuple(names or ())
        if parsed_names and len(parsed_names) != len(parsed):
            raise ValueError("joint names and values must have the same length")
        if len(set(parsed_names)) != len(parsed_names):
            raise ValueError("joint names must be unique")
        if any(not isinstance(name, str) or not name.strip() for name in parsed_names):
            raise ValueError("joint names must be non-empty strings")

        object.__setattr__(self, "values", parsed)
        object.__setattr__(self, "names", parsed_names)
        object.__setattr__(self, "unit", "rad")

    def as_unit(self, unit: str) -> tuple[float, ...]:
        normalized_unit = unit.strip().lower()
        if normalized_unit in {"rad", "radian", "radians"}:
            return self.values
        if normalized_unit in {"deg", "degree", "degrees"}:
            return tuple(math.degrees(value) for value in self.values)
        raise ValueError(f"unsupported joint unit {unit!r}; use 'rad' or 'deg'")


@dataclass(frozen=True)
class GripperResult:
    """Small result used by task-level grasp decisions."""

    success: bool
    final_width: float | None = None
    force: float | None = None
    details: object | None = None
