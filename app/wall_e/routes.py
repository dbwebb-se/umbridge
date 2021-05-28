"""
Contains routes for main purpose of app
"""
from flask import current_app, request
from app.wall_e import bp
from app import db, auth
from app.models import Submission, Course
from app.settings.api_config import API_KEY, API_URL
from app.wall_e.models.canvas_api import Canvas, Grader
import app.globals as g

# blueprints does not recognize "un-imported" names .. look for better fix.
g.is_fetching_or_grading = False

@bp.before_request
def before_request():
    """
    update last_seen for User before handling request
    """
    if g.is_fetching_or_grading:
        return { "message": "Wall-E is busy, try again in a few minutes" }

    g.is_fetching_or_grading = True

    # här kan vi logga saker
    # current_app.logger.info("Testar logging")


@bp.route('/wall-e/fetch-submissions', methods=['GET', 'POST'])
@auth.login_required
def fetch():
    """
    Route for fetching gradable submissions
    """
    active_courses = Course.query.filter_by(active=1)

    for c in active_courses:
        canvas = Canvas(API_URL, API_KEY, course_id=c.id)
        students = canvas.users_and_acronyms()
        subs = canvas.get_gradeable_submissions()

        for sub in subs:
            assignment_id = sub["assignment_id"]
            user_id = sub["user_id"]

            exists = Submission.query.filter_by(
                assignment_id=assignment_id, workflow_state='submitted',
                user_id=user_id
            ).count()

            if exists:
                continue

            user_acronym = students[user_id]
            kmom = canvas.get_assignment_name_by_id(assignment_id=assignment_id)
            s = Submission(
                assignment_id=assignment_id, kmom=kmom, user_id=user_id,
                user_acronym=user_acronym, course_id=c.id)

            db.session.add(s)
            db.session.commit()

    return { "message": "Successfully fetched new assignments from canvas" }



@bp.route('/wall-e/grade', methods=['GET', 'POST'])
@auth.login_required
def grade():
    """
    Route for grading students
    """
    grader = Grader(API_URL, API_KEY)
    graded_submissions = Submission.query.filter_by(workflow_state="pending_review")

    for sub in graded_submissions:
        grader.grade_submission(sub)
        sub.workflow_state = "graded"
        db.session.commit()

    return { "message": "Canvas has been updated with the new grades." }


@bp.teardown_request
def teardown_request(error=None):
    """
    Executes after all requests, regardless if error or not.
    """
    if error:
        current_app.logger.info(str(error))

    g.is_fetching_or_grading = False