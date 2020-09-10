import logging
from logging.handlers import RotatingFileHandler


class Logging:
    def __init__(self):
        self.logger = None

    def init_app(self, app):
        # set the logging levels
        # logging.basicConfig(filename='application.log', level=logging.INFO,
        #                     format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
        # logging.getLogger('werkzeug').setLevel(logging.DEBUG)

        file_handler = RotatingFileHandler('application.log', maxBytes=1024000, backupCount=10, encoding='utf-8')
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(name)s %(funcName)s %(levelname)-10s  %(message)s')
        )
        file_handler.setLevel(logging.INFO)

        log = logging.getLogger('application')
        log.setLevel(logging.DEBUG)
        log.addHandler(file_handler)

        self.logger = log
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)
        # self.logger.setLevel(logging.DEBUG)  # Set the log level to debug


APP_LOGGER = Logging()
