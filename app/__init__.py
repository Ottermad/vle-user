"""Main Package."""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name="default"):
    """Create Flask object called app and return it."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from .main.views import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
