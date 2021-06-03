"""
Contains tests for helper functions in app.models 
"""
from app.models import format_dict


def test_format_dict():
    """
    Checks if the return value is propper when you pass
    a dict with both string, didgits None values
    """
    data = { 'id': '1', 'name': 'python' }
    formated_data = format_dict(data)
    data2 = {}
    formated_data2 = format_dict(data2)
    data3 = { '1': '1' }
    formated_data3 = format_dict(data3)
    data4 = None
    formated_data4 = format_dict(data4)
    data5 = { 'name': 'python' }
    formated_data5 = format_dict(data5)

    assert formated_data == { 'id': 1, 'name': 'python' }
    assert formated_data2 == {}
    assert formated_data3 == { '1': 1 }
    assert formated_data4 == {}
    assert formated_data5 == { 'name': 'python' }
