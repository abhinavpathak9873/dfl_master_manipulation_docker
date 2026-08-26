"""Clear task-facing errors shared by the small toolbox foundation."""

from __future__ import annotations

from collections.abc import Iterable


class ToolboxError(RuntimeError):
    """Base error for expected toolbox failures."""


class BackendNotFoundError(ToolboxError):
    """Raised when a named implementation is absent from its direct mapping."""

    def __init__(
        self,
        *,
        capability: str,
        backend: str,
        available: Iterable[str],
        mapping_file: str,
    ) -> None:
        choices = ", ".join(sorted(available)) or "none"
        super().__init__(
            f"Unknown {capability} backend {backend!r}. "
            f"Available backends: {choices}. "
            f"Add the implementation and mapping in {mapping_file}."
        )
        self.capability = capability
        self.backend = backend
        self.available = tuple(sorted(available))
        self.mapping_file = mapping_file


class BackendInterfaceError(ToolboxError):
    """Raised when a selected backend lacks the requested robotics operation."""


class ObjectDBError(ToolboxError):
    """Base error for local object asset failures."""


class ObjectNotFoundError(ObjectDBError):
    """Raised when an object directory or record cannot be found."""


class InvalidObjectError(ObjectDBError):
    """Raised when an object record is malformed or unsafe."""


class MissingAssetError(ObjectDBError):
    """Raised when a path declared by an object record does not exist."""
