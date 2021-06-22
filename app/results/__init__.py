"""
Create Blurprint for main
"""
from flask import Blueprint

bp = Blueprint('results', __name__)

#pylint: disable=wrong-import-position, cyclic-import
from app.results import routes
#pylint: enable=wrong-import-position, cyclic-import
