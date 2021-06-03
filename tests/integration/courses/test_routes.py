"""
Contains tests for the app.auth module
"""

# pylint: disable=unused-argument, disable=protected-access, disable=redefined-outer-name
import json
from werkzeug.datastructures import Headers
import pytest
from app.models import User, Course
from app import db
from app.courses.routes import get_course


valid_header = Headers([('Authorization', "Basic ZGJ3ZWJiOnN1cGVyLXNlY3JldA==")])
non_existing_user_header = Headers([('Authorization', "Basic dXNlcjpwYXNz")])


@pytest.fixture(autouse=True, scope="function")
def run_before_and_after_tests(client):
    """Fixture to execute asserts before and after a test is run"""
    # Setup:
    u = User(username='dbwebb')
    u.password = 'super-secret'
    db.session.add(u)
    db.session.commit()

    c = Course(id=1, name='python', active=0)
    c1 = Course(id=99, name='oopython', active=1)
    c2 = Course(id=55, name='webapp', active=1)
    db.session.add(c)
    db.session.add(c1)
    db.session.add(c2)
    db.session.commit()

    yield # This is where the testing happens

    # Teardown :
    db.session.rollback()
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



def test_prepare():
    """ Tests the Setup """
    c = Course.query.filter_by(id=1).first()
    c2 = Course.query.filter_by(id=99).first()
    c3 = Course.query.filter_by(id=55).first()
    count = db.session.query(Course).count()

    assert str(c) == "<Course 1, python, Active: False>"
    assert str(c2) == "<Course 99, oopython, Active: True>"
    assert str(c3) == "<Course 55, webapp, Active: True>"
    assert count == 3


def test_get_course():
    """  Tests a helper function """
    valid_course = get_course({ 'id': 55 })
    assert str(valid_course) == "<Course 55, webapp, Active: True>"

    valid_data = get_course({ 'id': 50 })
    assert valid_data is None

    empty_data = get_course({})
    assert empty_data is False

    invalid_data = get_course({ 'name': 'python' })
    assert invalid_data is False

#################  GET  ###################################

def test_get_courses_no_header(client):
    """
    Trys to get courses with no header
    """
    response = client.get('/courses')

    assert response.status_code == 401
    assert b"No Authorization token provided" in response.data


def test_get_courses_invalid_header(client):
    """
    Trys to get courses with a non existing user
    """
    response = client.get('/courses', headers=non_existing_user_header)

    assert response.status_code == 401
    assert b"Invalid username or password" in response.data


def test_get_courses_invalid_user(client):
    """
    Trys to get courses with a non existing user
    """
    response = client.get('/courses', headers=non_existing_user_header)

    assert response.status_code == 401
    assert b"Invalid username or password" in response.data


def test_get_all_courses(client):
    """
    Trys to get all courses with am existing user
    """
    response = client.get('/courses', headers=valid_header)
    r = json.loads(response.data)

    assert response.status_code == 200
    assert len(r['courses']) == 3
    assert r['courses'][0] == { 'id': 55, 'name': 'webapp', 'active': 1 }
    assert r['courses'][1] == { 'id': 99, 'name': 'oopython', 'active': 1 }
    assert r['courses'][2] == { 'id': 1, 'name': 'python', 'active': 0 }


def test_get_all_active_courses(client):
    """
    Trys to get active courses
    """
    response = client.get('/courses?active=1', headers=valid_header)
    r = json.loads(response.data)

    assert response.status_code == 200
    assert len(r['courses']) == 2
    assert r['courses'][0] == { 'id': 55, 'name': 'webapp', 'active': 1 }
    assert r['courses'][1] == { 'id': 99, 'name': 'oopython', 'active': 1 }


def test_get_all_by_multiple_query_params(client):
    """
    Trys to get all active courses with the name oopython
    """
    response = client.get('/courses?active=1&name=oopython', headers=valid_header)
    r = json.loads(response.data)

    assert response.status_code == 200
    assert len(r['courses']) == 1
    assert r['courses'][0] == { 'id': 99, 'name': 'oopython', 'active': 1 }


def test_get_all_by_invalid_query_params(client):
    """
    Trys to get all courses by using invalid params
    """
    response = client.get('/courses?active=1&user_id=2', headers=valid_header)
    r = json.loads(response.data)

    assert response.status_code == 400
    assert r == { 'message': 'One or more parameter(s) does not exist' }


#################  POST ###################################

def test_add_course_no_header(course1_data, client):
    """
    Trys to add course with no header
    """
    response = client.post('/courses', data=course1_data)

    assert response.status_code == 401
    assert b"No Authorization token provided" in response.data



def test_add_course_no_valid_user(course1_data, client):
    """
    Trys to add a course with valid header but non existing user
    """

    response = client.post('/courses', data=course1_data, headers=non_existing_user_header)

    assert response.status_code == 401
    assert b"Invalid username or password" in response.data



def test_add_course_valid(course1_data, client):
    """
    Trys a valid response and checks if it the course is added to db.
    """

    response = client.post('/courses', data=course1_data, headers=valid_header)

    assert response.status_code == 201
    assert b"\"course\": " in response.data

    created = Course.query.filter_by(id=course1_data['id']).first()
    assert created is not None
    assert created.id == course1_data['id']
    assert created.name == course1_data['name']
    assert created.active == 1


def test_add_course_extra_key(client):
    """
    Trys to add keys that does not exist.
    """
    data = { 'id': 35, 'name': 'js', 'active': 0, 'hm': 22 }
    response = client.post('/courses', data=data, headers=valid_header)
    created = Course.query.filter_by(id=35).first()

    assert created is None
    assert response.status_code == 400
    assert b"\'hm\' is an invalid keyword" in response.data


def test_add_course_where_id_exists(client):
    """
    Trys to add a key that exsists in the database
    """
    data = { 'id': 1, 'name': 'js', 'active': 0 }
    response = client.post('/courses', data=data, headers=valid_header)
    assert response.status_code == 400
    assert b"already exists" in response.data


def test_add_course_with_no_data(client):
    """
    Trys to add a course with no data provided
    """
    data4 = {}
    response4 = client.post('/courses', data=data4, headers=valid_header)
    assert response4.status_code == 400
    assert b"No data provided" in response4.data


def test_add_course_without_id(client):
    """
    Trys to add a course with no id
    """
    data = { 'name': 'databas', 'active': 0 }
    response = client.post('/courses', data=data, headers=valid_header)
    assert response.status_code == 400
    assert b"No data provided" in response.data


#################  PUT     ###################################

def test_edit_course_no_header(course1_data, client):
    """
    Trys to edit course with no header
    """
    response = client.put('/courses', data=course1_data)
    assert response.status_code == 401
    assert b"No Authorization token provided" in response.data



def test_edit_course_no_valid_user(course1_data, client):
    """
    Trys to edit a course with valid header but non existing user
    """
    response = client.put('/courses', data=course1_data, headers=non_existing_user_header)
    assert response.status_code == 401
    assert b"Invalid username or password" in response.data


def test_edit_course_valid_active_only(client):
    """
    Trys a valid response and updates its active attribute.
    """
    data = { 'id': 1, 'name': 'python', 'active': 1 }
    before = Course.query.filter_by(id=data['id']).first().serialize

    response = client.put('/courses', data=data, headers=valid_header)

    assert response.status_code == 200

    res_json = json.loads(response.data)['course']
    after = Course.query.filter_by(id=data['id']).first()

    assert res_json == after.serialize
    assert after.id == before['id']
    assert after.name == before['name']
    assert after.active != before['active']
    assert after.active == 1



def test_edit_course_valid_name_only(client):
    """
    Trys a valid response and updates its name attribute.
    """
    data = { 'id': 1, 'name': 'oophp', 'active': 0 }
    before = Course.query.filter_by(id=data['id']).first().serialize

    response = client.put('/courses', data=data, headers=valid_header)

    assert response.status_code == 200

    res_json = json.loads(response.data)['course']
    after = Course.query.filter_by(id=data['id']).first()

    assert res_json == after.serialize
    assert after.id == before['id']
    assert after.name != before['name']
    assert after.active == before['active']
    assert after.name == 'oophp'



def test_edit_course_valid_both_name_and_active(client):
    """
    Trys a valid response and updates both its name and active attribute.
    """
    data = { 'id': 1, 'name': 'oophp', 'active': 1 }
    before = Course.query.filter_by(id=data['id']).first().serialize

    response = client.put('/courses', data=data, headers=valid_header)

    assert response.status_code == 200

    res_json = json.loads(response.data)['course']
    after = Course.query.filter_by(id=data['id']).first()

    assert res_json == after.serialize
    assert after.id == before['id']
    assert after.name != before['name']
    assert after.active != before['active']
    assert after.name == 'oophp'
    assert after.active == 1


def test_edit_course_with_no_data(client):
    """
    Trys to edit a course with no data provided
    """
    data = {}
    response = client.put('/courses', data=data, headers=valid_header)
    assert response.status_code == 400
    assert b"Course not found" in response.data


def test_edit_course_without_id(client):
    """
    Trys to edit a course with no id
    """
    data = { 'name': 'python', 'active': 0 }
    response = client.put('/courses', data=data, headers=valid_header)
    assert response.status_code == 400
    assert b"Course not found" in response.data



#################  DELETE  ###################################

def test_delete_course_no_header(course1_data, client):
    """
    Trys to delete course with no header
    """
    response = client.put('/courses', data=course1_data)
    assert response.status_code == 401
    assert b"No Authorization token provided" in response.data


def test_delete_course_no_valid_user(course1_data, client):
    """
    Trys to delete a course with valid header but non existing user
    """
    response = client.put('/courses', data=course1_data, headers=non_existing_user_header)
    assert response.status_code == 401
    assert b"Invalid username or password" in response.data


def test_delete_course_with_no_data(client):
    """
    Trys to delete a course with no data provided
    """
    data = {}
    response = client.delete('/courses', data=data, headers=valid_header)
    assert response.status_code == 400
    assert b"Course not found" in response.data


def test_delete_course_without_id(client):
    """
    Trys to delete a course with no id
    """
    data = { 'name': 'python', 'active': 0 }
    response = client.put('/courses', data=data, headers=valid_header)
    assert response.status_code == 400
    assert b"Course not found" in response.data


def test_delete_course_valid(client):
    """
    Trys a valid response and updates both its name and active attribute.
    """
    data = { 'id': 1 }
    exists = Course.query.filter_by(id=data['id']).first()
    count = db.session.query(Course).count()

    assert exists is not None
    assert count == 3

    response = client.delete('/courses', data=data, headers=valid_header)

    after_delete = Course.query.filter_by(id=data['id']).first()
    count_after = db.session.query(Course).count()
    assert after_delete is None
    assert count_after == 2

    assert response.status_code == 200
    assert b"<Course 1, python, Active: False> has been deleted" in response.data
