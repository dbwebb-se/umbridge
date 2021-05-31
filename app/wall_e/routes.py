"""
Contains routes for main purpose of app
"""

from flask import current_app, abort
from app.wall_e import bp
from app import db, auth
from app.models import Submission, Course
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
        abort(423, { "message": "Wall-E is busy, try again in a few minutes" })

    g.is_fetching_or_grading = True

    # här kan vi logga saker
    # current_app.logger.info("Testar logging")


@bp.route('/wall-e/fetch-submissions', methods=['GET', 'POST'])
@auth.requires_authorization_header
def fetch():
    """
    Route for fetching gradable submissions
    """
    active_courses = Course.query.filter_by(active=1)

    for c in active_courses:
        canvas = Canvas(
            base_url=current_app.config['CANVAS_API_URL'],
            api_token=current_app.config['CANVAS_API_TOKEN'],
            course_id=c.id,
            course_name=c.name)

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
            assignment_name = canvas.get_assignment_name_by_id(assignment_id=assignment_id)
            s = Submission(
                assignment_id=assignment_id, assignment_name=assignment_name, user_id=user_id,
                user_acronym=user_acronym, course_id=c.id)

            db.session.add(s)
            db.session.commit()

    return { "message": "Successfully fetched new assignments from canvas" }, 201



@bp.route('/wall-e/grade', methods=['GET', 'POST'])
@auth.requires_authorization_header
def grade():
    """
    Route for grading students
    """
    grader = Grader(
        base_url=current_app.config['CANVAS_API_URL'],
        api_token=current_app.config['CANVAS_API_TOKEN'])

    graded_submissions = Submission.query.filter_by(workflow_state="pending_review")

    for sub in graded_submissions:
        grader.grade_submission(sub)
        sub.workflow_state = "graded"
        db.session.commit()

    return { "message": "Canvas has been updated with the new grades." }, 200


@bp.teardown_request
def teardown_request(error=None):
    """
    Executes after all requests, regardless if error or not.
    """
    if error:
        current_app.logger.info(str(error))

    g.is_fetching_or_grading = False
