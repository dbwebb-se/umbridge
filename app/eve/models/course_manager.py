"""
Model class for eve.index
"""

import os

root_url = os.path.dirname(__file__) + "/../.."

class CourseManager:
    """ Manges test command and courses """
    _COURSES_BASE_FOLDER = f"{root_url}/eve/courses"
    _GIT_REPO_BASE_URL = "https://github.com/dbwebb-se"

    def __init__(self, assignment):
        """ Initiate the class """
        self._course = assignment["course"]
        self._kmom = assignment["kmom"]
        self._acr = assignment["acr"]



    def __str__(self):
        """Class string representation"""
        return f"{self._acr} {self._kmom} {self._course}"



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
        os.system(
            f"git clone {CourseManager._GIT_REPO_BASE_URL}/{self._course}.git "
            f"{self.get_course_repo_dir()}"
        )

        self.run_shell_command_in_course_repo("make docker-install")
        self.run_shell_command_in_course_repo("dbwebb init-me")



    def reset_kmom(self):
        """
        Empties a kmom from the students code

        TODO: Update and remove everything inside the kmoms subdir
            instead of "files only" which it currently does.
        """
        for root, _, files in os.walk(f"{self.get_course_repo_dir()}/{self._kmom}"):
            for file in files:
                os.remove(os.path.join(root, file))



    def update_download_and_run_tests(self):
        """
        Resets the kmom, updates the course repo and runs the tests
        os.system() returns a status-code
            0   => exit code 0 => PASSED
            256 => exit code 1 => FAILED
        """
        self.reset_kmom()
        self.run_shell_command_in_course_repo("dbwebb update")

        result = self.run_shell_command_in_course_repo(
            f"dbwebb test --docker {self._kmom} {self._acr} --download"
        )

        return "PG" if result == 0 else "Ux"



    def get_content_from_test_log(self, filename):
        """ Reads the log results and returns them """
        pathToLogfile = f"{self.get_course_repo_dir()}/.log/test/{filename}"

        with open(pathToLogfile, 'r') as fh:
            content = fh.read()

        return content
