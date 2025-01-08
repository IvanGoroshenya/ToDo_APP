from loguru import logger


def create_logger(app_name: str, level="DEBUG"):
    logger.add(
        f"logs/{app_name}.log",
        rotation="500 MB",
        retention="10 days",
        level=level,
        format="{time} {level} {message}"
    )

    return logger


service_logger = create_logger('main')