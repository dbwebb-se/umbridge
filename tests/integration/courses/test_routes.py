"""
Contains tests for the app.auth module
"""

# pylint: disable=unused-argument, disable=protected-access, disable=redefined-outer-name
from werkzeug.datastructures import Headers
import pytest
from app.models import User, Course
from app import db


valid_header = Headers([('Authorization', "Basic ZGJ3ZWJiOnN1cGVyLXNlY3JldA==")])
non_exsiting_user_header = Headers([('Authorization', "Basic dXNlcjpwYXNz")])


@pytest.fixture(autouse=True)
def run_before_and_after_tests(client):
    """Fixture to execute asserts before and after a test is run"""
    # Setup:
    u = User(username='dbwebb')
    u.password = 'super-secret'
    db.session.add(u)
    db.session.commit()

    c = Course(id=1, name='python', active=1)
    db.session.add(c)
    db.session.commit()

    yield # This is where the testing happens

    # Teardown :
    Course.query.filter(Course.id > 0).delete()
    User.query.filter(User.id > 0).delete()
    db.session.commit()


@pytest.fixture
def course1_data():
    """
    Course object
    """
    return {
        'id': 5,
        'name': "htmlphp"
    }

#################  GET  ###################################

#################  POST ###################################

def test_add_course_no_header(course1_data, client):
    """
    Trys to add course with a no header
    """
    response = client.post('/courses', data=course1_data)

    assert response.status_code == 401
    assert b"No Authorization token provided" in response.data



def test_add_course_no_valid_user(course1_data, client):
    """
    Trys to add a course with valid header but non existing user
    """

    response = client.post('/courses', data=course1_data, headers=non_exsiting_user_header)

    assert response.status_code == 401
    assert b"Invalid username or password" in response.data



def test_add_course_valid(course1_data, client):
    """
    Trys a valid response and checks if it the course is added to db.
    Then, to add wrong inputs and duplicated ids.
    """

    response = client.post('/courses', data=course1_data, headers=valid_header)

    assert response.status_code == 201
    assert b"\"course\": " in response.data

    created = Course.query.filter_by(id=course1_data['id']).first()
    assert created is not None
    assert created.id == course1_data['id']
    assert created.name == course1_data['name']
    assert created.active == 1


    data = { 'id': 35, 'name': 'js', 'active': 0, 'hm': 22 }
    response = client.post('/courses', data=data, headers=valid_header)
    created = Course.query.filter_by(id=35).first()

    assert created is None
    assert response.status_code == 400
    assert b"\'hm\' is an invalid keyword" in response.data


    data = { 'id': course1_data['id'], 'name': 'js', 'active': 0 }
    response = client.post('/courses', data=data, headers=valid_header)
    assert response.status_code == 400
    assert b"already exists" in response.data

#################  PUT     ###################################

#################  DELETE  ###################################
