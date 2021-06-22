"""
Contains Prod, Dev and Test config classes.
Also Custom class for logging, RequestFormatter.
"""


import os
from logging import Formatter
from flask import request


basedir = os.path.abspath(os.path.dirname(__file__) +  "/..")



class Config():
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CANVAS_API_URL = 'https://bth.instructure.com'
    CANVAS_API_TOKEN = os.environ.get('CANVAS_API_TOKEN') or \
        '12133~WhTU1hL4C472pg4wpGkXiIryQL61gEvxzbhTpbcyBcR8T03shtT9xtPRDo2yjOkJ'


class ProdConfig(Config):
    """Production configuration"""
    ENV = "production"
    DEBUG = False

class DevConfig(Config):
    """Development configuration"""
    ENV = 'development' # Pointless attribut, needs to be set in environment
    DEBUG = True # Pointless attribut, needs to be set in environment

class TestConfig(Config):
    """Test configuration"""
    ENV = "test"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class RequestFormatter(Formatter):
    """
    Custom class for formatting logger to include url and ip
    """
    def format(self, record):
        """
        Add url and remote_addr to record
        """
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)
