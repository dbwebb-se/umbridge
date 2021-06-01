"""
Contains tests for app.models.User class
"""

# pylint: disable=redefined-outer-name
import pytest
from app.models import Submission, Course


@pytest.fixture
def submission1():
    """
    Submission object
    """
    course = Course(
        id=3,
        name='python',
        active=1
    )

    return Submission(
        user_id=1,
        user_acronym="moc",
        assignment_name='kmom02',
        assignment_id=2,
        course_id=3,
        course=course,
        grade="PG",
        feedback="Ok",
        workflow_state="graded"
    )


def test_new_submission(submission1):
    """
    Test that user object contain correct values
    """
    assert submission1.user_id == 1
    assert submission1.user_acronym == 'moc'
    assert submission1.assignment_name == 'kmom02'
    assert submission1.assignment_id == 2
    assert submission1.course_id == 3
    assert submission1.grade == 'PG'
    assert submission1.feedback == 'Ok'
    assert submission1.workflow_state == 'graded'
    assert str(submission1) == '<Assignment moc, kmom02, python>'
