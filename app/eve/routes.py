"""
Contains routes for main purpose of app
"""
from flask import current_app
from app.eve import bp
from app.eve.models.course_manager import CourseManager
import app.eve.globals as g

# blueprints does not recognize "un-imported" names .. look for better fix.
g.is_test_running = False

@bp.before_request
def before_request():
    """
    Executes before the requests
    """
    if g.is_test_running:
        return {"Status": "Eve is busy, try again in a few minutes"}

    g.is_test_running = True



@bp.route('/eve', methods=['GET', 'POST'])
def index():
    """
    Route for index page

    TODO:
    1. Use the database.
    2. Update the database with the new grade and feedback, then ping Wall-E.
    3. Write tests
    """

    CM = CourseManager({
        "course": "python",
        "kmom": "kmom01",
        "acr": "mabn17"
    })

    if not CM.does_course_repo_exist():
        CM.create_and_initiate_dbwebb_course_repo()

    grade = CM.update_download_and_run_tests()
    log_content = CM.get_content_from_test_log()

    print(f"{CM} - {grade}!")

    return {
        "assignment": str(CM),
        "grade": grade,
        "log": log_content
    }


@bp.teardown_request
def teardown_request(error=None):
    """
    Executes after all requests, regardless if error or not.
    """
    if error:
        current_app.logger.info(str(error))

    g.is_test_running = False
