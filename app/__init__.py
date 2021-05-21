import logging
from flask import Flask
from flask.logging import default_handler
from app.config import ProdConfig, RequestFormatter

def create_app(config_class=ProdConfig):
    """
    Create flask app, init addons, blueprints and setup logging
    """
    app = Flask(__name__)
    app.config.from_object(config_class)


    #pylint: disable=wrong-import-position, cyclic-import, import-outside-toplevel
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.wall_e import bp as wall_e_bp
    app.register_blueprint(wall_e_bp)

    from app.eve import bp as eve_bp
    app.register_blueprint(eve_bp)
    #pylint: enable=wrong-import-position, cyclic-import, import-outside-toplevel


    if not app.debug and not app.testing:
        formatter = RequestFormatter(
            '[%(asctime)s %(levelname)s] %(remote_addr)s requested %(url)s\n: %(message)s [in %(module)s:%(lineno)d]'
        )
        default_handler.setFormatter(formatter)
        app.logger.setLevel(logging.INFO)

    return app