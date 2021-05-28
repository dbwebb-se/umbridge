from app.models import User
import base64
from flask import request, abort
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        authorization = request.headers.get('Authorization')

        if not authorization:
            abort(401, "No Authorization token provided")

        _type, credentials = authorization.split(' ')

        try:
            message = base64.b64decode(credentials).decode('utf-8')
            print(message)
        except:
            abort(401, "Incorrect token value")

        username, password = message.split(":")
        usr = User.query.filter_by(username=username).first()

        if not usr or not usr.verify_password(password):
            abort(401, "Invalid username or password")

        return f(*args, **kws)
    return decorated_function
