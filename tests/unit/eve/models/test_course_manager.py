"""
Contains tests for app.eve.models.CourseManager class
"""
# pylint: disable=unused-argument, disable=protected-access, disable=redefined-outer-name
from unittest import mock
import pytest
from app.models import Submission, Course
from app.eve.models.course_manager import CourseManager
#import pytest

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

def test_init(submission1, test_app):
    """ Tests the initialization """
    cm = CourseManager(submission1)

    assert cm._course == 'python'
    assert cm.assignment_name == 'kmom02'
    assert cm._acr == 'moc'
    assert cm._config is not None
    assert str(cm) == 'moc kmom02 python'


def test_get_config_from_course_by_key_normal(submission1, test_app):
    """ Test so the configuration loader """
    cm = CourseManager(submission1)

    cm._config = { 'default': { 'name': 'value', 'val': 'name' } }
    assert cm.get_config_from_course_by_key('name') == 'value'

    cm._config = {
        'default': { 'name': 'value', 'val': 'name' },
        'python': { 'name': 'value2' }
    }
    assert cm.get_config_from_course_by_key('name') == 'value2'
    assert cm.get_config_from_course_by_key('val') == 'name'


def test_get_config_from_course_by_key_formatted(submission1, test_app):
    """ Test so the configuration loaders formatting """
    cm = CourseManager(submission1)

    cm._config = {
        "default": {
            "git_url": "https://github.com/dbwebb-se/{course}.git",
            "installation_commands": [
                "make docker-install",
                "dbwebb init-me"
            ],
            "test_command": "dbwebb test --docker {kmom} {acr} --download",
            "update_command": "dbwebb update",
            "log_file": ".log/test/docker/main.ansi",
            "ignore_assignments": []
        },
        "python": {
            "ignore_assignments": [ '{kmom}', 'kmom03' ]
        }
    }

    assert cm.get_config_from_course_by_key('git_url') \
        == 'https://github.com/dbwebb-se/python.git'
    assert cm.get_config_from_course_by_key('installation_commands') \
        == [ "make docker-install", "dbwebb init-me" ]
    assert cm.get_config_from_course_by_key('test_command') \
        == 'dbwebb test --docker kmom02 moc --download'
    assert cm.get_config_from_course_by_key('update_command') \
        == 'dbwebb update'
    assert cm.get_config_from_course_by_key('log_file') \
        == '.log/test/docker/main.ansi'
    assert cm.get_config_from_course_by_key('ignore_assignments') \
        == [ 'kmom02', 'kmom03' ]


def test_get_course_repo_dir(submission1, test_app):
    """ Test so the configuration loader """
    cm = CourseManager(submission1)

    res = cm.get_course_repo_dir()
    assert res == f'{cm._COURSES_BASE_FOLDER}/python'


@mock.patch('app.eve.models.course_manager.CourseManager.run_shell_command_in_course_repo')
def test_update_download_and_run_tests(mock_shell_cmd, submission1, test_app):
    """ Only tests if it returns the correct grade value """
    mock_shell_cmd.return_value = 256
    cm = CourseManager(submission1)
    
    grade = cm.update_download_and_run_tests()
    assert grade == 'Ux'
    assert mock_shell_cmd.called is True

    mock_shell_cmd.return_value = 0
    grade2 = cm.update_download_and_run_tests()
    assert grade2 == 'PG'

    mock_shell_cmd.return_value = 1
    grade3 = cm.update_download_and_run_tests()
    assert grade3 == 'Ux'
