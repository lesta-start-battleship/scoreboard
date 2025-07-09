import logging
import colorlog


def setup_logger(name=None, level=logging.DEBUG):
    """Создаёт и возвращает настроенный colorlog логгер."""
    logger = colorlog.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        handler = colorlog.StreamHandler()
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger