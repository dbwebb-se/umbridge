"""
Contains tests for the app.auth module
"""

# pylint: disable=unused-argument, disable=protected-access
from unittest import mock
import pytest
from werkzeug.exceptions import Unauthorized
from app.auth import requires_authorization_header
from app.models import User


invalid_base64_token = 'Basic Token'
valid_base64_not_basic = 'Basic dG9rZW4=' # token
valid_token = 'Basic dXNlcm5hbWU6cGFzcw==' # username:pass


@mock.patch("app.auth.request")
@mock.patch("app.models.User")
def test_auth_header_invalid_base64(mock_user, mock_request, test_app):
    """
    Testing authorization function
    """

    mock_request.headers.get.return_value = invalid_base64_token
    first = mock.Mock().first.return_value = None
    mock_user.query.filter_by.return_value = first

    @requires_authorization_header
    def decorator_test():
        """ Dummy function for authorization header"""
        return True

    with pytest.raises(Unauthorized, match="401 Unauthorized: Incorrect token value"):
        decorator_test()


@mock.patch("app.auth.request")
@mock.patch("app.models.User")
def test_auth_header_valid_base64_not_basic(mock_user, mock_request, test_app):
    """
    Testing authorization function
    """

    mock_request.headers.get.return_value = valid_base64_not_basic
    first = mock.Mock().first.return_value = None
    mock_user.query.filter_by.return_value = first

    @requires_authorization_header
    def decorator_test():
        """ Dummy function for authorization header"""
        return True

    with pytest.raises(Unauthorized, match="401 Unauthorized: Incorrect token value"):
        decorator_test()


@mock.patch("app.auth.request")
@mock.patch("app.models.User")
def test_auth_header_valid_token_user_not_exist(mock_user, mock_request, test_app):
    """
    Testing authorization function
    """

    mock_request.headers.get.return_value = valid_token
    first = mock.Mock().first.return_value = 1
    mock_user.query.filter_by.return_value = first

    @requires_authorization_header
    def decorator_test():
        """ Dummy function for authorization header"""
        return True

    with pytest.raises(Unauthorized, match="401 Unauthorized: Invalid username or password"):
        decorator_test()


@mock.patch("app.auth.request")
@mock.patch("app.models.User.query")
def test_auth_header_valid_token_user_exists(mock_user, mock_request, test_app):
    """
    Testing authorization function
    """

    usr = User(username='username')
    usr.password = 'pass'


    mock_request.headers.get.return_value = valid_token
    first = mock.Mock()
    first.first.return_value = usr
    #first.first.return_value = usr
    mock_user.filter_by.return_value = first

    # User.query = mock_user
    #usr = User.query.filter_by(username=username).first()


    @requires_authorization_header
    def decorator_test():
        """ Dummy function for authorization header"""
        return True


    assert decorator_test() is True
