"""
Create Blurprint for main
"""
from flask import Blueprint

bp = Blueprint('new', __name__)

#pylint: disable=wrong-import-position, cyclic-import
from app.new import routes
#pylint: enable=wrong-import-position, cyclic-import
