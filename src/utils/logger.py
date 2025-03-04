import logging


def setup_logger(logger_name):
    """Настройка логгеров.

    Returns:
        Logger: Логгер.
    """

    if len(logging.getLogger().handlers) > 0:
        return logging.getLogger(logger_name)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Custom
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Aiogram
    logging.getLogger("aiogram").setLevel(logging.INFO)

    # Asyncio
    logging.getLogger("asyncio").setLevel(logging.INFO)

    return logger
