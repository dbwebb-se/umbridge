"""
Create Blurprint for main
"""
from flask import Blueprint

bp = Blueprint('eve', __name__)

#pylint: disable=wrong-import-position, cyclic-import
from app.eve import routes
#pylint: enable=wrong-import-position, cyclic-import