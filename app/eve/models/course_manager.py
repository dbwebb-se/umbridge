"""
Model class for eve.index
"""

import os
import json
from app.settings import settings

app_base_path = os.path.dirname(__file__) + "/../.."

class CourseManager:
    """ Manges test command and courses """
    _COURSES_BASE_FOLDER = f"{settings.APP_BASE_PATH}/eve/courses"

    def __init__(self, submission):
        """ Initiate the class """
        self._course = submission.course.name
        self.assignment_name = submission.assignment_name
        self._acr = submission.user_acronym
        self._config = settings.get_course_map()


    def __str__(self):
        """Class string representation"""
        return f"{self._acr} {self.assignment_name} {self._course}"



    def get_config_from_course_by_key(self, key):
        """ Gets the configuration value from [course][key] """
        try:
            config = self._config[self._course][key]
        except KeyError:
            config = self._config['default'][key]

        return config.format(
            assignment_name=self.assignment_name,
            acr=self._acr,
            course=self._course,
        )



    def get_course_repo_dir(self):
        """ Gets the full path for the active course repo """
        return f"{CourseManager._COURSES_BASE_FOLDER}/{self._course}"



    def does_course_repo_exist(self):
        """ Checks if the the course repo exist """
        return os.path.exists(self.get_course_repo_dir())



    def run_shell_command_in_course_repo(self, command):
        """ cd into the course repo and executes shell command """
        return os.system(f"cd {self.get_course_repo_dir()} && {command}")



    def create_and_initiate_dbwebb_course_repo(self):
        """
        Clones a new course repo and installs all dependencies
            + init-me
        """
        os.mkdir(self.get_course_repo_dir())

        git_url = self.get_config_from_course_by_key('git_url')
        os.system(f"git clone {git_url} {self.get_course_repo_dir()}")

        commands = self.get_config_from_course_by_key('installation_commands')
        for command in commands:
            self.run_shell_command_in_course_repo(command)



    def update_download_and_run_tests(self):
        """
        Updates the course repo and runs the tests
        os.system() returns a status-code
            0   => exit code 0 => PASSED
            256 => exit code 1 => FAILED
        """
        update_command = self.get_config_from_course_by_key('update_command')
        self.run_shell_command_in_course_repo(update_command)

        test_command = self.get_config_from_course_by_key('test_command')
        result = self.run_shell_command_in_course_repo(test_command)

        return "PG" if result == 0 else "Ux"



    def get_content_from_test_log(self):
        """ Reads the log results and returns them """
        log_file = self.get_config_from_course_by_key('log_file')
        pathToLogfile = f"{self.get_course_repo_dir()}/{log_file}"

        with open(pathToLogfile, 'r') as fh:
            content = fh.read()

        return content
