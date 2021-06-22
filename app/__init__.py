
"""
Factory for application
"""


import logging
from os import system
import click
from flask import Flask
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import ProdConfig, RequestFormatter

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=ProdConfig):
    """
    Create flask app, init addons, blueprints and setup logging
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    

    #pylint: disable=wrong-import-position, cyclic-import, import-outside-toplevel
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.wall_e import bp as wall_e_bp
    app.register_blueprint(wall_e_bp)

    from app.eve import bp as eve_bp
    app.register_blueprint(eve_bp)

    from app.courses import bp as courses_bp
    app.register_blueprint(courses_bp)

    from app.results import bp as results_bp
    app.register_blueprint(results_bp)
    #pylint: enable=wrong-import-position, cyclic-import, import-outside-toplevel


    if not app.debug and not app.testing:
        formatter = RequestFormatter(
            '[%(asctime)s %(levelname)s] %(remote_addr)s requested %(url)s\n: %(message)s [in %(module)s:%(lineno)d]'
        )
        default_handler.setFormatter(formatter)
        app.logger.setLevel(logging.INFO)


    @app.cli.command()
    @click.argument("token", default="ZGJ3ZWJiOnN1cGVyLXNlY3JldA==")
    def grade(token):
        """
        Ro run scheduled job.
        Fetches the assignments, corrects reports the grades to canvas.

        * * * * * cd /path/to/repo && .venv/bin/flask grade {token}
        """
        curl = f'curl -i -H "Authorization: Basic {token}"'
        host = 'http://localhost:5000'

        system(f"{curl} {host}/wall-e/fetch-submissions")
        system(f"{curl} {host}/eve/test")
        system(f"{curl} {host}/wall-e/grade")


    return app

from app import models #pylint: disable=wrong-import-position, cyclic-import, import-outside-toplevel
