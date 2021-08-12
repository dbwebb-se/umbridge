import os
from logging import Formatter
from dotenv import load_dotenv
from app import create_app
from app import config

basedir = os.path.abspath(os.path.dirname(__file__) +  "/..")
load_dotenv(os.path.join(basedir, '.env'))


env = os.environ.get('FLASK_ENV')

if env == "development":
    app = create_app(config.DevConfig)
elif env == "production":
    app = create_app(config.ProdConfig)
elif env == "test":
    app = create_app(config.TestConfig)
else:
    app = create_app()
