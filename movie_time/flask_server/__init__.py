from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def _init_app_config(flask_app):
    from . import settings
    flask_app.config.update(settings.CONFIG)


def create_app():
    flask_app = Flask(__name__)

    from . import routes, services, models
    _init_app_config(flask_app)
    DB = SQLAlchemy(flask_app)
    models.init_app(flask_app)
    services.init_app(flask_app)
    routes.init_app(flask_app)
    return flask_app

