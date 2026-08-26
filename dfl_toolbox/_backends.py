"""Tiny helpers for source-controlled backend mappings."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from .errors import BackendInterfaceError, BackendNotFoundError

BackendFactory = Callable[..., Any]


def normalize_backend_id(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("backend must be a non-empty string")
    backend = value.strip().lower()
    if backend.endswith(".py"):
        backend = backend[:-3]
    if not backend:
        raise ValueError("backend must contain a name before the optional '.py'")
    return backend


def build_backend(
    *,
    capability: str,
    backend: str,
    backends: Mapping[str, BackendFactory],
    mapping_file: str,
    options: Mapping[str, Any],
) -> tuple[str, Any]:
    backend_id = normalize_backend_id(backend)
    factory = backends.get(backend_id)
    if factory is None:
        raise BackendNotFoundError(
            capability=capability,
            backend=backend_id,
            available=backends,
            mapping_file=mapping_file,
        )
    return backend_id, factory(**dict(options))


def invoke_backend(
    implementation: Any,
    *,
    capability: str,
    backend: str,
    method: str,
    args: tuple[Any, ...],
    kwargs: Mapping[str, Any],
) -> Any:
    operation = getattr(implementation, method, None)
    if not callable(operation):
        raise BackendInterfaceError(
            f"{capability} backend {backend!r} does not implement {method}()."
        )
    return operation(*args, **dict(kwargs))
