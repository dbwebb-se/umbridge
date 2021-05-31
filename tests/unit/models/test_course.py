"""
Contains tests for app.models.User class
"""

# pylint: disable=redefined-outer-name
import pytest
from app.models import Course


@pytest.fixture
def course1():
    """
    Course object
    """
    return Course(
        id=200,
        name="python",
        active=0
    )



def test_new_courses(course1):
    """
    Test that user object contain correct values
    """
    assert course1.id == 200
    assert course1.name == 'python'
    assert course1.active == 0
    assert str(course1) == "<Course 200, python, Active: False>"
