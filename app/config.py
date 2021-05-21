
import os
from logging import Formatter
from flask import request


basedir = os.path.abspath(os.path.dirname(__file__) +  "/..")



class Config():
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

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