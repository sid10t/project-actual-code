import logging
from colorlog import ColoredFormatter


class LogUtil:
    def __init__(self, log_file, log_level=logging.DEBUG):
        self.log_file = log_file
        self.log_level = log_level
        self.logger = self._create_logger()

    def _create_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(self.log_level)

        formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)-8s: %(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'white',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'blue',
            },
            secondary_log_colors={},
            style='%'
        )

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


if __name__ == '__main__':
    log = LogUtil('app.log')
    log.info('This is an info message, sidiot!')
    log.debug('This is a debug message, sidiot!')
    log.warning('This is a warning message, sidiot!')
    log.error('This is an error message, sidiot!')
    log.critical('This is a critical message, sidiot!')
