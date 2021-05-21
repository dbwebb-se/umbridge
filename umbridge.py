import os
from logging import Formatter
from app import create_app
from app import config


env = os.environ.get('FLASK_ENV')

if env == "development":
    app = create_app(config.DevConfig)
elif env == "production":
    app = create_app(config.ProdConfig)
elif env == "test":
    app = create_app(config.TestConfig)
else:
    app = create_app()
