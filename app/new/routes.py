"""
Contains routes for main purpose of app
"""
from flask import current_app, abort
from app.wall_e import bp
from app import db, auth
from app.models import Submission, Course, format_dict
import app.globals as g

from canvasapi import Canvas
from app.runner import run

@bp.route('/new/grade', methods=['GET'])
@auth.requires_authorization_header
def fetch():
    """
    Route grading submissions
    """
    canvas = Canvas(
        current_app.config['URL_CANVAS_API'],
        current_app.config['TOKEN_CANVAS_API']
    )
    active_courses = Course.query.filter_by(active=1)

    for c in active_courses:

        run.grade_course(canvas, c.id, c.name)
        # get submision


        students = canvas.users_and_acronyms()
        subs = canvas.get_gradeable_submissions()

        for sub in subs:
            assignment_id = sub["assignment_id"]
            user_id = sub["user_id"]

            # Ignores the submission if it exists
            stud_attempts = Submission.query.filter_by(
                assignment_id=assignment_id, user_id=user_id)
            exists = [a for a in stud_attempts if a.workflow_state in ['new', 'tested']]

            if exists:
                continue
            try:
                user_acronym = students[user_id]
            except KeyError:
                current_app.logger.info(
                    f"User id {user_id} from submission {sub['id']} is not among students fetched from Canvas."
                )
                continue
            assignment_name = canvas.get_assignment_name_by_id(assignment_id=assignment_id)

            s = Submission(
                assignment_id=assignment_id, assignment_name=assignment_name, user_id=user_id,
                user_acronym=user_acronym, course_id=c.id, attempt_nr=sub["attempt"])
            current_app.logger.info(f"Found submission for {user_acronym} in assignment {assignment_name}.")


            db.session.add(s)
            db.session.commit()

    return { "message": "Successfully fetched new assignments from canvas" }, 201



# blueprints does not recognize "un-imported" names .. look for better fix.
g.is_fetching_or_grading = False

@bp.before_request
def before_request():
    """
    update last_seen for User before handling request
    """
    if g.is_fetching_or_grading:
        abort(423, { "message": "New is busy, try again in a few minutes" })

    g.is_fetching_or_grading = True

    # här kan vi logga saker
    # current_app.logger.info("Testar logging")



@bp.teardown_request
def teardown_request(error=None):
    """
    Executes after all requests, regardless if error or not.
    """
    if error:
        current_app.logger.info(str(error))

    g.is_fetching_or_grading = False
