from .base import DB


def init_app(app):
    DB.init_app(app)
