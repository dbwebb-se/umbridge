"""
Contains error handlers
"""
from flask import current_app, request
from app.errors import bp
from app import db

@bp.app_errorhandler(404)
def not_found_error(error):
    """
    Error handler for code 404
    """
    current_app.logger.info(f"{error} URL:{request.path}")
    return { "message": str(error) }, 404



@bp.app_errorhandler(500)
def internal_error(error):
    """
    Error handler for code 500
    """
    current_app.logger.error(error)
    # här kan vi återställa DB om problem
    db.session.rollback()
    return { "message": str(error) }, 500
