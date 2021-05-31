"""
Contains routes for main purpose of app
"""
from flask import request
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from app.courses import bp
from app import auth
from app.models import Course



def get_course(data):
    """
    Checks if the request data is valid
    and returns the course
    """
    if not data or 'id' not in data:
        return False

    return Course.query.filter_by(id=data['id']).first()



@bp.route('/courses', methods=['GET'])
@auth.requires_authorization_header
def get_courses():
    """
    Route to display all courses
    """
    params = request.args

    if params:
        try:
            result = Course.query.filter_by(**params).order_by(Course.active.desc())
        except InvalidRequestError:
            return { 'message': 'One or more parameter(s) does not exist' }, 400
    else:
        result = Course.query.order_by(Course.active.desc())

    return { "courses": [c.serialize for c in result] }



@bp.route('/courses', methods=['POST'])
@auth.requires_authorization_header
def create_course():
    """
    Route to add new courses
    """
    data = request.form

    if not data:
        return { "message": "No data provided" }, 400

    try:
        course = Course.create(**data)
    except (InvalidRequestError, TypeError) as e:
        return { "message": "Invalid data", 'info': str(e) }, 400
    except IntegrityError:
        return { "message": f"Id {data['id']} already exists." }, 400

    return { "course": course.serialize }, 201



@bp.route('/courses', methods=['PUT'])
@auth.requires_authorization_header
def update_course():
    """
    Route to update a course
    """
    data = request.form
    course = get_course(data)

    if not course:
        return { "message": 'Course not found' }, 400

    course.update(data)
    return { "course": course.serialize }



@bp.route('/courses', methods=['DELETE'])
@auth.requires_authorization_header
def delete_course():
    """
    Route to remove a course
    """
    data = request.form
    course = get_course(data)

    if not course:
        return { "message": 'Course not found' }, 400

    course.delete()
    return { "message": f"{course} has been deleted" }
