"""
Model class for eve.index
"""

import os

base_url = os.path.dirname(__file__) + "/../.."

class DbwebbCli:
    COURSES_BASE_FOLDER = f"{base_url}/eve/courses"
    GIT_REPO_BASE_URL = "https://github.com/dbwebb-se"

    def __init__(self, assignment):
        """ Initiate the class """
        self._course = assignment["course"]
        self._kmom = assignment["kmom"]
        self._acr = assignment["acr"]



    def __str__(self):
        """Class string representation"""
        return f"{self._acr} {self._kmom} {self._course}"



    def get_courses_dir(self):
        """ Gets the full path for eve/courses"""
        return DbwebbCli.COURSES_BASE_FOLDER



    def get_course_repo_dir(self):
        """ Gets the full path for the active course repo """
        return f"{self.get_courses_dir()}/{self._course}"



    def does_course_repo_exist(self):
        """ Checks if the the course repo exist """
        return os.path.exists(self.get_course_repo_dir())



    def create_and_initiate_dbwebb_course_repo(self):
        """
        Clones a new course repo and installs all dependencies
            + init-me
        """
        os.mkdir(self.get_course_repo_dir())
        os.system(f"git clone {DbwebbCli.GIT_REPO_BASE_URL}/{self._course}.git {self.get_course_repo_dir()}")
        os.system(f"cd {self.get_course_repo_dir()} && make docker-install")
        os.system(f"cd {self.get_course_repo_dir()} && dbwebb init-me")



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
        os.system(f"cd {self.get_course_repo_dir()} && dbwebb update")

        result = os.system((
            f"cd {self.get_course_repo_dir()} && "
            f"dbwebb test --docker {self._kmom} {self._acr} --download"
        ))

        return "PASSED" if result == 0 else "FAILED"
