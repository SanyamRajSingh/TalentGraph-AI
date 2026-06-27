import logging
from pythonjsonlogger import jsonlogger

def setup_logging(level: int = logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)

    # Remove all existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s',
        rename_fields={"levelname": "level", "asctime": "timestamp"}
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    # Suppress noisy logs
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
