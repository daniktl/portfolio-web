from flask import Flask
import os
import logging
from portfolio.core import bp as core_bp
from portfolio.extensions import db

logger = logging.getLogger(__name__)

BLUEPRINTS = (core_bp,)
CONFIG_MAPPING = {
    "dev": "portfolio.settings.dev.DevConfig",
    "prod": "portfolio.settings.prod.ProdConfig",
    "test": "portfolio.settings.test.TestConfig"
}


def create_app(config_type: str = 'dev'):
    app = Flask(__name__)
    configure_app(app, config_type)
    configure_blueprints(app, blueprints=BLUEPRINTS)
    configure_extensions(app)
    configure_logging(app)
    logger.info("Flask Service Started! PID={}.".format(os.getpid()))
    return app


def configure_app(app: Flask, config_type: str) -> None:
    """Apply configurations based on configuration type"""
    app.config.from_object(CONFIG_MAPPING[config_type])


def configure_blueprints(app: Flask, blueprints: tuple) -> None:
    """Configure all existing blueprints"""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_extensions(app: Flask) -> None:
    """Put all your extensions here"""
    db.init_app(app)


def configure_logging(app: Flask) -> None:
    """Enable logging for all configurations except debug or testing"""
    if app.debug or app.testing:
        return
    app_logger = logging.getLogger("portfolio")
    app_logger.setLevel(app.config.get("LOG_LEVEL", logging.WARNING))
