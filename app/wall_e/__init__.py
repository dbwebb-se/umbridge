"""
Create Blurprint for main
"""
from flask import Blueprint

bp = Blueprint('wall-e', __name__)

#pylint: disable=wrong-import-position, cyclic-import
from app.wall_e import routes
#pylint: enable=wrong-import-position, cyclic-import