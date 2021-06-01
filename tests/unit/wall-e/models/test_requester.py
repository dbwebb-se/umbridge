"""
Contains tests for app.wall_e.canvas_api.Canvas class
"""
# pylint: disable=unused-argument, disable=protected-access
from unittest import mock
from app.wall_e.models.requester import Requester


def test_init(test_app):
    """
    Tests if the url_parser returns the correct value
    """
    url, token = 'url', 'token'
    r = Requester(url, token)

    assert r._key == token
    assert r._url == url


def test_get_headers(test_app):
    """
    Checks if the default header values are correct
    and if it updates on params
    """
    r = Requester('url', 'token')

    res = r._get_headers()
    assert res == { 'Authorization': 'Basic token' }

    res_with_extra = r._get_headers({ 'Content-Type': 'application/json' })
    assert res_with_extra == {
        'Authorization': 'Basic token',
        'Content-Type': 'application/json'
    }

    res_with_extras = r._get_headers({
        'Content-Type': 'application/json',
        'Keep-Alive': 'timeout=5, max=1000'
    })
    assert res_with_extras == {
        'Authorization': 'Basic token',
        'Content-Type': 'application/json',
        'Keep-Alive': 'timeout=5, max=1000'
    }


def test_get_base_url(test_app):
    """
    Tests if the url_parser returns the correct value
    """
    r = Requester('url', 'token')

    res = r._get_base_url('endpoint')
    assert res == 'url/endpoint'


@mock.patch('app.wall_e.models.requester.Requester._base_request')
def test_request_get(mock_base_req, test_app):
    """
    Checks so the request is called from _request_get
    """
    mock_base_req.return_value = {}
    r = Requester('url', 'token')

    r._request_get('endpoint')
    assert mock_base_req.call_count == 1
    mock_base_req.assert_called_with(mock.ANY, 'endpoint', None, params={})

    mock_base_req.reset_mock()
    r._request_get('endpoint', payload={'data': 'data'},
        headers={'Content-Type': 'application/json'})
    mock_base_req.assert_called_with(
        mock.ANY, 'endpoint', {'Content-Type': 'application/json'},
        params={'data': 'data'})


@mock.patch('app.wall_e.models.requester.Requester._base_request')
def test_request_post(mock_base_req, test_app):
    """
    Checks so the request is called from _request_post
    """
    mock_base_req.return_value = {}
    r = Requester('url', 'token')

    r._request_post('endpoint')
    assert mock_base_req.call_count == 1
    mock_base_req.assert_called_with(mock.ANY, 'endpoint', None, data={})

    mock_base_req.reset_mock()
    r._request_post('endpoint', payload={'data': 'data'},
        headers={'Content-Type': 'application/json'})
    mock_base_req.assert_called_with(
        mock.ANY, 'endpoint', {'Content-Type': 'application/json'},
        data={'data': 'data'})


@mock.patch('app.wall_e.models.requester.Requester._base_request')
def test_request_put(mock_base_req, test_app):
    """
    Checks so the request is called from _request_put
    """
    mock_base_req.return_value = {}
    r = Requester('url', 'token')

    r._request_put('endpoint')
    assert mock_base_req.call_count == 1
    mock_base_req.assert_called_with(mock.ANY, 'endpoint', None, json={})

    mock_base_req.reset_mock()
    r._request_put('endpoint', payload={'data': 'data'},
        headers={'Content-Type': 'application/json'})
    mock_base_req.assert_called_with(
        mock.ANY, 'endpoint', {'Content-Type': 'application/json'},
        json={'data': 'data'})



@mock.patch('app.wall_e.models.requester.Requester._base_request')
def test_request_delete(mock_base_req, test_app):
    """
    Checks so the request is called from _request_delete
    """
    mock_base_req.return_value = {}
    r = Requester('url', 'token')

    r._request_delete('endpoint')
    assert mock_base_req.call_count == 1
    mock_base_req.assert_called_with(mock.ANY, 'endpoint', None, json={})

    mock_base_req.reset_mock()
    r._request_delete('endpoint', payload={'data': 'data'},
        headers={'Content-Type': 'application/json'})
    mock_base_req.assert_called_with(
        mock.ANY, 'endpoint', {'Content-Type': 'application/json'},
        json={'data': 'data'})
