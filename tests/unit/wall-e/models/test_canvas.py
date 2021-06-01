"""
Contains tests for app.wall_e.canvas_api.Canvas class
"""
# pylint: disable=unused-argument, disable=protected-access
from unittest import mock
import pytest
from tests.mock.mock_requester import get_mocked_canvas_set_response


@mock.patch('app.wall_e.models.requester.Requester._base_request')
def test_init(mock_base_req, test_app):
    """
    Tests that the courses user are formatted properly.
    """
    get_mocked_canvas_set_response(mock_base_req, [
        { 'login_id': 'moc@bth.se', 'id': 0 }
    ])

    assert mock_base_req.call_count == 2


@mock.patch('app.wall_e.models.requester.Requester._base_request')
def test_users_and_acronyms(mock_base_req, test_app):
    """
    Tests that the courses user are formatted properly.
    """
    c = get_mocked_canvas_set_response(mock_base_req, [
        { 'login_id': 'moc@bth.se', 'id': 0 },
        { 'login_id': 'mabn17@bth.se', 'id': 1 }
    ])
    mock_base_req.reset_mock()

    assert c.users_and_acronyms() == { 0: 'moc', 1: 'mabn17' }
    assert mock_base_req.call_count == 0

    c = get_mocked_canvas_set_response(mock_base_req, [])
    assert c.users_and_acronyms() == {}




@mock.patch('app.wall_e.models.requester.Requester._base_request')
def test_get_user_by_acronym(mock_base_req, test_app):
    """
    Tests that the courses user are formatted properly.
    """

    c = get_mocked_canvas_set_response(mock_base_req, [
        { 'login_id': 'moc@bth.se', 'id': 0 },
        { 'login_id': 'mabn17@student.bth.se', 'id': 1 }
    ])
    mock_base_req.reset_mock()

    assert c.get_user_by_acronym('moc') == { 'login_id': 'moc@bth.se', 'id': 0 }
    assert c.get_user_by_acronym('mabn17') == { 'login_id': 'mabn17@student.bth.se', 'id': 1 }
    assert mock_base_req.call_count == 0

    c = get_mocked_canvas_set_response(mock_base_req, [])
    with pytest.raises(IndexError, match=r"out of range"):
        c.get_user_by_acronym('aar')





@mock.patch('app.wall_e.models.requester.Requester._base_request')
def test_get_assignment_by_name(mock_base_req, test_app):
    """ Tests to get an assignment object by name key """
    c = get_mocked_canvas_set_response(mock_base_req, [
        {'id': 1, 'name': 'kmom01'},
        {'id': 2, 'name': 'kmom02'},
        {'id': 3, 'name': 'kmom03'}
    ])
    mock_base_req.reset_mock()

    assert c.get_assignment_by_name('kmom03') == { 'id': 3, 'name': 'kmom03' }
    assert c.get_assignment_by_name('kmom01') == { 'id': 1, 'name': 'kmom01' }
    assert c.get_assignment_by_name('kmom02') == { 'id': 2, 'name': 'kmom02' }


    with pytest.raises(IndexError, match=r"out of range"):
        c.get_assignment_by_name('kmom10')

    assert mock_base_req.call_count == 0


@mock.patch('app.wall_e.models.requester.Requester._base_request')
def test_get_assignment_name_by_id(mock_base_req, test_app):
    """ Tests to get an assignment name by its id """
    c = get_mocked_canvas_set_response(mock_base_req, [
        {'id': 1, 'name': 'kmom01'},
        {'id': 2, 'name': 'kmom02'},
        {'id': 3, 'name': 'kmom03'}
    ])
    mock_base_req.reset_mock()

    assert c.get_assignment_name_by_id(1) == 'kmom01'
    assert c.get_assignment_name_by_id(3) == 'kmom03'
    assert c.get_assignment_name_by_id(2) == 'kmom02'


    with pytest.raises(IndexError, match=r"out of range"):
        c.get_assignment_name_by_id(10)

    assert mock_base_req.call_count == 0



@mock.patch('app.wall_e.models.requester.Requester._base_request')
def test_get_gradeable_submissions(mock_base_req, test_app):
    """ Tests if gradable submissions filters the correct values """
    mock_values = [
        {'id': 1, 'assignment_id': 1, 'name': 'kmom01'},
        {'id': 2, 'assignment_id': 2, 'name': 'kmom02'},
        {'id': 3, 'assignment_id': 3, 'name': 'kmom03'}
    ]

    c = get_mocked_canvas_set_response(mock_base_req, mock_values)
    mock_base_req.reset_mock()

    c._config = { 'default': { 'ignore_assignments': [] } }
    assert c.get_gradeable_submissions() == mock_values
    assert mock_base_req.call_count == 1

    c._config = { 'default': { 'ignore_assignments': [ 'kmom02' ] } }
    assert c.get_gradeable_submissions() == [
        {'id': 1, 'assignment_id': 1, 'name': 'kmom01'},
        {'id': 3, 'assignment_id': 3, 'name': 'kmom03'}
    ]
