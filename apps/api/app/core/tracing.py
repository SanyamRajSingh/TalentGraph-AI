from contextlib import contextmanager
from collections.abc import Iterator


@contextmanager
def trace_span(name: str, **attributes: object) -> Iterator[None]:
    """No-op tracing span for deterministic local demo runs."""

    _ = (name, attributes)
    yield
