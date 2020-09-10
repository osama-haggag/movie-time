from .home import home_bp


def init_app(app):
    app.register_blueprint(home_bp)
