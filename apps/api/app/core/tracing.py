from contextlib import contextmanager
from collections.abc import Iterator


@contextmanager
def trace_span(name: str, **attributes: object) -> Iterator[None]:
    """Placeholder tracing span.

    TODO: Replace with OpenTelemetry or platform tracing if needed for the demo.
    """

    _ = (name, attributes)
    yield
