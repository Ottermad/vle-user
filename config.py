"""Configurations."""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE_NAME = "user_db"


class Config:
    """Base Config Object containing settings that should always be present."""

    SECRET_KEY = os.environ.get('SECRET_KEY', "this_needs_to_be_more_secure")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVICE_NAME = 'user'


class Development(Config):
    """Config used in development."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db/{}'.format(DATABASE_NAME)


class Testing(Config):
    """Config used when running unit tests."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'testing-database.sqlite')
    PRESERVE_CONTEXT_ON_EXCEPTION = False

config = {
    'development': Development,
    'testing': Testing,
    'default': Development
}
