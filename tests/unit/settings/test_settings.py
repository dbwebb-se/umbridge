"""
Contains tests for app.models.User class
"""

# pylint: disable=redefined-outer-name
from app.settings import settings


def test_get_course_map():
    """
    Test that user object contain correct values
    """
    config = settings.get_course_map()
    assert 'default' in config
