"""
Authorization decorators
"""


import base64
from functools import wraps
from flask import request, abort
from app.models import User


def requires_authorization_header(f):
    """
    Decorator for locked routes
    """
    @wraps(f)
    def decorator(*args, **kws):
        """
        Looks for an Authorization header
        and compares it to the user database
        """
        authorization = request.headers.get('Authorization')

        if not authorization:
            abort(401, "No Authorization token provided")

        try:
            _type, credentials = authorization.split(' ')
            message = base64.b64decode(credentials).decode('utf-8')
            username, password = message.split(":")
        except (base64.binascii.Error, UnicodeDecodeError, ValueError):
            abort(401, "Incorrect token value")

        usr = User.query.filter_by(username=username).first()

        if not usr or not usr.compare_password(password):
            abort(401, "Invalid username or password")

        return f(*args, **kws)
    return decorator
