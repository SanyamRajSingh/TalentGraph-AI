import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure application logging.

    TODO: Add structured JSON logging before production/demo hardening.
    """

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    """Dependency injection point for module loggers."""

    return logging.getLogger(name)
