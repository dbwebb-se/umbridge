"""
Contains routes for main purpose of app
"""
from flask import current_app
from app.eve import bp
from app.eve.models.course_manager import CourseManager
import app.eve.globals as g
from app import db
from app.models import Submission, Course

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
    course_id, course_name = 2508, 'python'
    # user_id, user_acronym, kmom = 5954, 'mabn17', 'kmom01'
    # assignment_id = 21567

    Course.query.filter(Course.id > 0).delete()
    c = Course(id=course_id, name=course_name)
    db.session.add(c)
    db.session.commit()

    Submission.query.filter(Submission.id > 0).delete()
    db.session.commit()

    return "Submission and Course table has been reset with dummy data"


@bp.route('/eve/test', methods=['GET', 'POST'])
def index():
    """
    Route for index page
    """

    submissions = Submission.query.filter_by(workflow_state="submitted")
    for sub in submissions:
        CM = CourseManager(sub)

        if not CM.does_course_repo_exist():
            CM.create_and_initiate_dbwebb_course_repo()

        grade = CM.update_download_and_run_tests()
        feedback = CM.get_content_from_test_log()

        sub.workflow_state = 'pending_review'
        sub.grade = grade
        sub.feedback = feedback

        db.session.commit()

    return {"Status": "Corrected all assignments!"}


@bp.teardown_request
def teardown_request(error=None):
    """
    Executes after all requests, regardless if error or not.
    """
    if error:
        current_app.logger.info(str(error))

    g.is_test_running = False
