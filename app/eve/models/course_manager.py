"""
Model class for eve.index
"""

import os
import sys
from re import sub
import subprocess
import shutil
from flask import current_app
from app.settings import settings


class CourseManager:
    """ Manges test command and courses """
    _COURSES_BASE_FOLDER = f"{settings.APP_BASE_PATH}/eve/courses"

    KNOWN_ERRORS = {
        7: {
            "docs": "failed potatoe",
            "grade": "U",
        },
        124: {
            "docs": "timeout",
            "grade": "Ux",
        },
        137: {
            "docs", "timeout with SIGKILL",
            "grade", "Ux"
        }
    }

    def __init__(self, submission):
        """ Initiate the class """
        self._course = submission.course.name
        self.assignment_name = submission.assignment_name
        self._assignment_id = submission.assignment_id
        self._user_id = submission.user_id
        self._acr = submission.user_acronym
        self._config = settings.get_course_map()
        self._attempt = submission.attempt_nr


    def __str__(self):
        """Class string representation"""
        return f"{self._acr} {self.assignment_name} {self._course}"



    def get_config_from_course_by_key(self, key):
        """ Gets the configuration value from [course][key] """
        try:
            config = self._config[self._course][key]
        except KeyError:
            config = self._config['default'][key]

        formatter = {
            'kmom': self.assignment_name,
            'acr': self._acr,
            'course': self._course
        }

        return self._recursive_format(config, formatter)



    def _recursive_format(self, config, formatter):
        """
        Recursively format all string values in settings
        """
        if isinstance(config, str):
            return config.format(**formatter)
        elif isinstance(config, list):
            return [self._recursive_format(value, formatter) for value in config]
        elif isinstance(config, dict):
            return {key:self._recursive_format(value, formatter) for key, value in config.items()}
        return config



    def get_course_repo_dir(self):
        """ Gets the full path for the active course repo """
        return f"{CourseManager._COURSES_BASE_FOLDER}/{self._course}"



    def does_course_repo_exist(self):
        """ Checks if the the course repo exist """
        return os.path.exists(self.get_course_repo_dir())



    def run_shell_command_in_course_repo(self, command, print_output=False):
        """ cd into the course repo and executes shell command """
        current_app.logger.debug(f"Running command {command}")
        output = subprocess.run(
            command, cwd=f"{self.get_course_repo_dir()}",
            capture_output=True,
        )
        if print_output:
            print(output.stdout.decode("utf-8"))

        if output.stderr:
            current_app.logger.error(output.stderr)

        current_app.logger.debug(f"Got output {output}")

        return output.returncode



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


    def prepare_for_students_code(self):
        """
        Run prepare command in course repo to prepare for testing student
        """
        prepare_command = self.get_config_from_course_by_key('prepare_student')
        self.run_shell_command_in_course_repo(prepare_command)



    def update_download_and_run_tests(self):
        """
        Updates the course repo and runs the tests
        os.system() returns a status-code
            0   => exit code 0 => PASSED
            256 => exit code 1 => FAILED
        """
        current_app.logger.info(f"Updating repo")
        update_command = self.get_config_from_course_by_key('update_command')
        self.run_shell_command_in_course_repo(update_command)

        current_app.logger.info(f"Testing code")
        test_command = self.get_config_from_course_by_key('test_command')
        result = self.run_shell_command_in_course_repo(test_command, print_output=True)
        current_app.logger.info(f"Got exit code {result} from test command!")

        if result == 0:
            return "PG"
        if result in self.KNOWN_ERRORS: # add more know exit codes for errors when find them
            current_app.logger.error(f"Test returned {result} for {self._acr} in assignment {self.assignment_name}")
            return self.KNOWN_ERRORS[result]["grade"] # return U when known error happens
        return "Ux"



    def get_content_from_test_log(self):
        """ Reads the log results and returns them """
        log_file = self.get_config_from_course_by_key('log_file')
        pathToLogfile = f"{self.get_course_repo_dir()}/{log_file}"

        with open(pathToLogfile, 'r') as fh:
            content = fh.read()

        return content



    def copy_and_zip_student_code(self, feedback, grade):
        """
        Copy students code and log file to temp and create zip folder.
        Then remove original folder
        """
        dest_dir_name = f"{self._assignment_id}{self._user_id}{self._attempt}"
        dest_parent_path = f"{settings.APP_BASE_PATH}/wall_e/temp"
        dest = f"{dest_parent_path}/{dest_dir_name}"
        src_folders = self.get_config_from_course_by_key("assignment_folders")[self.assignment_name]
        exclude = self.get_config_from_course_by_key("assignment_folders")["exclude"]

        current_app.logger.debug(f"config for copy/zip - dest:{dest}, srcs:{src_folders}, exclude:{exclude}")

        try:
            os.makedirs(dest)
        except FileExistsError:
            shutil.rmtree(dest)

        for src in src_folders:
            self.run_shell_command_in_course_repo(
                ["rsync", "-avq", f"{src}", f"{dest}/", "--exclude", f"{','.join(exclude)}"]
            )

        with open(f"{dest}/log.txt", "w") as fd:
            fd.write(feedback)

        shutil.make_archive(dest+"z", 'zip', dest) # has to distinguise archive name (z), otherwise it didn't create
        shutil.rmtree(dest)

        return dest+"z.zip"



    def clean_up_students_code(self):
        """
        Run clean up command in course repo to remove students code
        """
        clean_up_command = self.get_config_from_course_by_key('clean_up_student')
        self.run_shell_command_in_course_repo(clean_up_command)
