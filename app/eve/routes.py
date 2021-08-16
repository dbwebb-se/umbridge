"""
Contains routes for main purpose of app
"""
from flask import current_app, abort
from app.eve import bp
from app.eve.models.course_manager import CourseManager
import app.globals as g
from app import db, auth
from app.models import Submission, Course, User

# blueprints does not recognize "un-imported" names .. look for better fix.
g.is_test_running = False

@bp.before_request
def before_request():
    """
    Executes before the requests
    """
    if g.is_test_running:
        abort(423, { "message": "Eve is busy, try again in a few minutes" })

    g.is_test_running = True



@bp.route('/eve/reset', methods=['GET', 'POST'])
def reset():
    """
    Temporary route to reset database and load a test assignment.
    """
    course_id, course_name = 2508, 'python'

    Course.query.filter(Course.id > 0).delete()
    c1 = Course(id=course_id, name=course_name, active=1)
    c2 = Course(id=123, name='ike-aktiv', active=0)
    db.session.add(c1)
    db.session.add(c2)
    db.session.commit()

    Submission.query.filter(Submission.id > 0).delete()
    db.session.commit()

    User.query.filter(User.id > 0).delete()
    user = User(username='dbwebb')
    user.password = 'super-secret'
    db.session.add(user)
    db.session.commit()

    return {"message": "Submission and Course table has been reset with dummy data"}



@bp.route('/eve/test', methods=['GET', 'POST'])
@auth.requires_authorization_header
def test():
    """
    Route for index page
    """

    submissions = Submission.query.filter_by(workflow_state="new")
    for sub in submissions:
        CM = CourseManager(sub)

        if not CM.does_course_repo_exist():
            CM.create_and_initiate_dbwebb_course_repo()




        grade = CM.update_download_and_run_tests()

        feedback = CM.get_content_from_test_log()

        zip_path = CM.copy_and_zip_student_code(feedback)

        sub.workflow_state = 'tested'
        sub.grade = grade
        sub.feedback = feedback
        sub.zip_file_path = zip_path

        db.session.commit()

    return { "message": "All new assignments has been corrected" }


@bp.teardown_request
def teardown_request(error=None):
    """
    Executes after all requests, regardless if error or not.
    """
    if error:
        current_app.logger.info(str(error))

    g.is_test_running = False
