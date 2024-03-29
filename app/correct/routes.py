"""
Contains routes for main purpose of app
"""
from flask import current_app, abort, request
from app.correct import bp
from app import db, auth
from app.models import Course, format_dict
import app.globals as g

from canvasapi import Canvas
from canvasapi.exceptions  import ResourceDoesNotExist
from app.correct import course as correct_course

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



@bp.route('/correct', methods=['GET'])
@auth.requires_authorization_header
def correct():
    """
    Route grading submissions
    """
    canvas = Canvas(
        current_app.config['URL_CANVAS_API'],
        "12133~bOL9ymnmZbOsq9YuHb0QqJ9DKxdwyeZSKcanKTJ6gwXhI0wGEPWacak1ia2g0KEI"
    )
    active_courses = Course.query.filter_by(active=1)

    for c in active_courses:
        try:
            correct_course.course(canvas, c.id, c.name)
        except ResourceDoesNotExist as e:
            # do something here to notify me that course is missing
            raise e


    return { "message": "Successfully fetched new assignments from canvas" }, 201



@bp.route('/re-grade', methods=['GET'])
@auth.requires_authorization_header
def re_grade():
    """
    Route grading already graded submissions
    """
    data = format_dict(request.form)
    current_app.logger.debug(data)

    canvas = Canvas(
        current_app.config['URL_CANVAS_API'],
        current_app.config['TOKEN_CANVAS_API']
    )
    active_courses = Course.query.filter_by(active=1, id=data["id"])

    for c in active_courses:
        try:
            correct_course.course(canvas, c.id, c.name, data["assignment"], "graded")
        except ResourceDoesNotExist as e:
            # do something here to notify me that course is missing
            raise e


    return { "message": "Successfully fetched new assignments from canvas" }, 201



# @bp.route('/reset', methods=['GET'])
# def reset():
#     """
#     Temporary route to reset database and load a test assignment.
#     """
#     from app.models import User

#     course_id, course_name = 2508, 'python'

#     Course.query.filter(Course.id > 0).delete()
#     c1 = Course(id=course_id, name=course_name, active=1)
#     # c2 = Course(id=123, name='ike-aktiv', active=0)
#     db.session.add(c1)
#     # db.session.add(c2)
#     db.session.commit()

#     User.query.filter(User.id > 0).delete()
#     user = User(username='dbwebb')
#     user.password = 'super-secret'
#     db.session.add(user)
#     db.session.commit()

#     return {"message": "Submission and Course table has been reset with dummy data"}



@bp.teardown_request
def teardown_request(error=None):
    """
    Executes after all requests, regardless if error or not.
    """
    if error:
        current_app.logger.info(str(error))

    g.is_fetching_or_grading = False
