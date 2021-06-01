"""
Module for mocks
"""
from app.wall_e.models.canvas_api import Canvas

class MockRequester():
    """
    Class to mock Requester
    """

    def __init__(self, val):
        """ Initiates the return value """
        self.json_ = val

    def json(self):
        """ returns the json response """
        return self.json_



def get_mocked_canvas_set_response(mock_obj, mock_value):
    """
    returns a new mock response with the given value
    """
    request_mocker = MockRequester(mock_value)
    mock_obj.return_value = request_mocker

    return Canvas('url', 'token', course_id=1, course_name='name')
