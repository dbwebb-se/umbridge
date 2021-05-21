from flask import Flask
from app.config import ProdConfig, RequestFormatter

def create_app(config_class=ProdConfig):
    """
    Create flask app, init addons, blueprints and setup logging
    """
    app = Flask(__name__)
    app.config.from_object(config_class)


    #pylint: disable=wrong-import-position, cyclic-import, import-outside-toplevel
    from app.wall_e import bp as wall_e_bp
    app.register_blueprint(wall_e_bp)

    from app.eve import bp as eve_bp
    app.register_blueprint(eve_bp)
    #pylint: enable=wrong-import-position, cyclic-import, import-outside-toplevel


    return app