"""
Contains routes for main purpose of app
"""
from flask import redirect, url_for, request, current_app
from app.eve import bp
from app.eve.models.correct import DbwebbCli
import os

@bp.before_request
def before_request():
    """
    update last_seen for User before handling request
    """
    pass
    # här kan vi logga saker
    # current_app.logger.debug("{} is authenticated".format(current_user))


@bp.route('/eve', methods=['GET', 'POST'])
def index():
    """
    Route for index page
    """
    CLI = DbwebbCli({
        "course": "python",
        "kmom": "kmom01",
        "acr": "mabn17"
    })

    if not CLI.does_course_repo_exist():
        CLI.create_and_initiate_dbwebb_course_repo()

    status = CLI.update_download_and_run_tests()
    print(f"{CLI} - {status}!")

    return ""
