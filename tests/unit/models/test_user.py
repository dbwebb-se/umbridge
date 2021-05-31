"""
Contains tests for app.models.User class
"""

# pylint: disable=redefined-outer-name
import pytest
from app.models import User


@pytest.fixture
def user1():
    """
    User object
    """
    return User(
        username='dbwebb',
        password="Hello"
    )

def test_new_user(user1):
    """
    Test that user object contain correct values
    """
    assert user1.username == 'dbwebb'
    assert str(user1) == "<User dbwebb>"
    with pytest.raises(AttributeError, match=r"not readable"):
        assert user1.password == 'rise when accessing password'



def test_password_hashing(user1):
    """
    Test setting password for user
    """
    user1.password = 'cat'
    assert user1.compare_password('dog') is False
    assert user1.compare_password('cat') is True
