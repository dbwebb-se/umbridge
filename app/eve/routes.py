"""
Contains routes for main purpose of app
"""
from flask import current_app
from app.eve import bp
from app.eve.models.course_manager import CourseManager
import app.eve.globals as g
from app import db
from app.models import Assignment

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


@bp.route('/eve/reset', methods=['GET', 'POST'])
def reset():
    """
    Temporary route to reset database and load a test assignment.
    """

    Assignment.query.filter(Assignment.id > 0).delete()
    a = Assignment(acronym="mabn17", kmom="kmom01", course="python")
    db.session.add(a)
    db.session.commit()

    return "Assignment table has been reset"


@bp.route('/eve', methods=['GET', 'POST'])
def index():
    """
    Route for index page
    """

    submissions = Assignment.query.filter_by(status="PENDING")
    for sub in submissions:

        CM = CourseManager(sub)

        if not CM.does_course_repo_exist():
            CM.create_and_initiate_dbwebb_course_repo()

        grade = CM.update_download_and_run_tests()
        feedback = CM.get_content_from_test_log()

        sub.update_status_grade_feedback('GRADED', grade, feedback)
        db.session.commit()

    return {"Status": f"Corrected {len(submissions)} assignments!"}


@bp.teardown_request
def teardown_request(error=None):
    """
    Executes after all requests, regardless if error or not.
    """
    if error:
        current_app.logger.info(str(error))

    g.is_test_running = False
