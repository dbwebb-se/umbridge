"""
Contains error handlers
"""
from flask import render_template, current_app
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    """
    Error handler for code 404
    """
    current_app.logger.info(error)
    return { "message": str(error) }, 404


@bp.app_errorhandler(500)
def internal_error(error):
    """
    Error handler for code 500
    """
    current_app.logger.error(error)
    # här kan vi återställa DB om problem
    # db.session.rollback()
    return { "message": str(error) }, 500
