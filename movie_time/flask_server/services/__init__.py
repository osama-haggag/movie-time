from .logger import APP_LOGGER
#from .database import DB_MANAGER


def init_app(app):
    APP_LOGGER.init_app(app)
#    DB_MANAGER.init_app(app)
