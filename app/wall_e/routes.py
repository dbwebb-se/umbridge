"""
Contains routes for main purpose of app
"""
from flask import current_app
from app.wall_e import bp
from app import db
from app.models import Submission, Course
from app.settings.api_config import API_KEY, API_URL
from app.wall_e.models.canvas_api import Canvas, Grader

@bp.before_request
def before_request():
    """
    update last_seen for User before handling request
    """
    pass
    # här kan vi logga saker
    # current_app.logger.info("Testar logging")


@bp.route('/wall-e/fetch-submissions', methods=['GET', 'POST'])
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

    return {}



@bp.route('/wall-e/grade', methods=['GET', 'POST'])
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

    return {}
