"""
Contains routes for main purpose of app
"""
from flask import redirect, url_for, request, current_app
from app.eve import bp



@bp.before_request
def before_request():
    """
    update last_seen for User before handling request
    """
    pass
    # här kan vi logga saker
    # current_app.logger.debug("{} is authenticated".format(current_user))



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required 
def index():
    """
    Route for index page
    """
    # gör saker
    pass
