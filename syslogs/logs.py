import logging

logger = logging.getLogger(__name__)


def print_log(msg, level="info"):
    if level not in ["info", "warning", "debug", "error", "critical"]:
        logger.error("Not a valid log level. Should be one of info, warning, debug, error or critical.")
    else:
        getattr(logger, level)(msg)

