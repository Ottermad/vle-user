"""Main Package."""
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import config
from services import Services
from internal.exceptions import CustomError

db = SQLAlchemy()
services = Services()


def create_app(config_name="default"):
    """Create Flask object called app and return it."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    @app.errorhandler(CustomError)
    def custom_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.before_request
    def get_user_details_from_header():
        pass

    db.init_app(app)
    services.init_app(app)

    from .school.views import school_blueprint
    app.register_blueprint(school_blueprint)

    from .user.views import user_blueprint
    app.register_blueprint(user_blueprint)

    from .permissions.views import permissions_blueprint
    app.register_blueprint(permissions_blueprint)


    return app
