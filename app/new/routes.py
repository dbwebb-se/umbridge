"""
Contains routes for main purpose of app
"""
from flask import current_app, abort
from app.new import bp
from app import db, auth
from app.models import Submission, Course, format_dict
import app.globals as g

from canvasapi import Canvas
from canvasapi.exceptions  import ResourceDoesNotExist
from app.correct import course as correct_course

@bp.route('/new/grade', methods=['GET'])
@auth.requires_authorization_header
def grade():
    """
    Route grading submissions
    """
    canvas = Canvas(
        current_app.config['URL_CANVAS_API'],
        current_app.config['TOKEN_CANVAS_API']
    )
    active_courses = Course.query.filter_by(active=1)

    for c in active_courses:

        try:
            correct_course.course(canvas, c.id, c.name)
        except ResourceDoesNotExist as e:
            # do something here to notify me that course is missing
            raise e


    return { "message": "Successfully fetched new assignments from canvas" }, 201



# blueprints does not recognize "un-imported" names .. look for better fix.
# g.is_fetching_or_grading = False

# @bp.before_request
# def before_request():
#     """
#     update last_seen for User before handling request
#     """
#     if g.is_fetching_or_grading:
#         abort(423, { "message": "New is busy, try again in a few minutes" })

#     g.is_fetching_or_grading = True

#     # här kan vi logga saker
#     # current_app.logger.info("Testar logging")



# @bp.teardown_request
# def teardown_request(error=None):
#     """
#     Executes after all requests, regardless if error or not.
#     """
#     if error:
#         current_app.logger.info(str(error))

#     g.is_fetching_or_grading = False
