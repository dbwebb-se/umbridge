"""
Contains routes for main purpose of app
"""
from flask import current_app
from app.wall_e import bp
from app.wall_e.models import canvas_requests as cr

@bp.before_request
def before_request():
    """
    update last_seen for User before handling request
    """
    pass
    # här kan vi logga saker
    # current_app.logger.info("Testar logging")



@bp.route('/wall-e', methods=['GET', 'POST'])
def index():
    """
    Route for index page
    """
    course_id = 2508
    students = cr.users_and_acronyms(course_id=course_id)
    subs = cr.gradeable_submissions(course_id=course_id)

    for sub in subs:
        try:
            print(students[sub["user_id"]])
        except:
            print('acr not found')

        print(sub)

        # TODO: fetch code and run tests
        # assign to grade variable

        # submissions.grade_submission(
        #     course_id=course_id,
        #     assignment_id=sub["assignment_id"],
        #     user_id=sub["user_id"],
        #     grade=grade
        # )

    return { "students": students, "subs": subs }
