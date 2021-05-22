"""
Contains routes for main purpose of app
"""
from flask import redirect, url_for, request, current_app
from app.eve import bp
from app.eve.models.course_repo import CourseManager
import os

@bp.before_request
def before_request():
    """
    Executes before the requests
    """
    pass
    # här kan vi logga saker
    # current_app.logger.debug("{} is authenticated".format(current_user))


@bp.route('/eve', methods=['GET', 'POST'])
def index():
    """
    Route for index page

    TODO:
    1. Database (sqlite) - how does Wall-E data look like?
      - Handle the assignment object differently - Create a class for it.
    2. Add a queue system so tests does not overlap?
    3. Update the database with the new grade and ping Wall-E
    4. Extra assignments?
      - Maybe not, it does not affect the grade YET and they can run it locally.
      - If yes, change how it works in the examiner module.
    """

    CM = CourseManager({
        "course": "python",
        "kmom": "kmom01",
        "acr": "mabn17"
    })

    if not CM.does_course_repo_exist():
        CM.create_and_initiate_dbwebb_course_repo()

    grade = CM.update_download_and_run_tests()
    log_content = CM.get_content_from_test_log('docker/main.ansi')

    print(f"{CM} - {grade}!")

    return {
        "assignment": str(CM),
        "grade": grade,
        "log": log_content
    }
