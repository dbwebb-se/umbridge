"""
Contains routes for main purpose of app
"""
from flask import redirect, url_for, request, current_app
from app.wall_e import bp



@bp.before_request
def before_request():
    """
    update last_seen for User before handling request
    """
    pass
    # här kan vi logga saker
    current_app.logger.info("Testar logging")



@bp.route('/wall-e', methods=['GET', 'POST'])
def index():
    """
    Route for index page
    """
    # gör saker
    return "hej"
