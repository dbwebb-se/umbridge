"""
Contains routes for main purpose of app
"""
from flask import current_app
from app.wall_e import bp
from app.wall_e.models import courses, assignments, submissions
from app import db
from app.models import Submission

@bp.before_request
def before_request():
    """
    update last_seen for User before handling request
    """
    pass
    # här kan vi logga saker
    # current_app.logger.info("Testar logging")


@bp.route('/wall-e/fetch-submissions', methods=['GET', 'POST'])
def index():
    """
    Route for fetching gradable submissions

    TODO: Vad skall man göra om submission redan finns?
      (WHERE assignment_id=assignment_id AND user_id=user_id)
          Lägg inte till den i databasen då den inväntar rättning?
    """
    course_id = 2508

    students = courses.users_and_acronyms(course_id=course_id)
    subs = submissions.gradeable_submissions(course_id=course_id)

    for sub in subs:
        assignment_id = sub["assignment_id"]
        kmom = assignments.get_assignment_name_by_id(assignment_id=assignment_id, course_id=course_id)

        user_id = sub["user_id"]
        user_acronym = students[user_id]

        s = Submission(assignment_id=assignment_id, kmom=kmom, user_id=user_id, user_acronym=user_acronym, course_id=course_id)
        db.session.add(s)
        db.session.commit()

    return { "subs": subs }



@bp.route('/wall-e/grade', methods=['GET', 'POST'])
def grade():
    """
    Route for grading students
    """

    graded_submissions = Submission.query.filter_by(workflow_state="pending_review")
    for sub in graded_submissions:
        submissions.grade_submission(
            sub=sub
        )

        sub.workflow_state="graded"
        db.session.commit()

    return "Klar!"