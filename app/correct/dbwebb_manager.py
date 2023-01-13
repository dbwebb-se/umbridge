import os
import subprocess
import shutil
from flask import current_app
from app.settings import settings


class DbwebbManager:
    """ Manges test command and courses """
    _COURSES_BASE_FOLDER = f"{settings.APP_BASE_PATH}/correct/courses"
    _TEMP_PATH = f"{settings.APP_BASE_PATH}/correct/temp"

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

    def __init__(self, course_name, assignment, submission, config):
        """ Initiate the class """
        self._course_name = course_name
        self._assignment_name = assignment["name"]
        self._assignment_id = assignment["id"]
        self._user_id = submission.user_id
        self._acr = self.get_user_acronym(submission)
        self._config = config
        self._attempt = submission.attempt

    def get_user_acronym(self, submission):
        try:
            return submission.user["login_id"].split("@")[0]
        except TypeError:
            current_app.logger.error(f"could not extract acronym for user {u}")
        except KeyError:
            current_app.logger.error(f"could not find key 'login_id' for {u}")



    def __str__(self):
        """Class string representation"""
        return f"{self._acr} {self._assignment_name} {self._course_name}"



    def test(self):

        if not self.does_course_repo_exist():
            current_app.logger.info(f"Missing course repo for {self._course_name}, initiating!")
            self.create_and_initiate_dbwebb_course_repo()

        current_app.logger.info(f"Grading {self._acr} in assignment {self._assignment_name}")
        self.prepare_for_students_code()

        grade = self.update_download_and_run_tests()
        current_app.logger.info(f"{self._acr} got grade {grade}")

        current_app.logger.info("Getting logfile")
        feedback = self.get_content_from_test_log()

        current_app.logger.debug(f"Copying and zipping code for {self._acr} in assignment {self._assignment_name}")
        zip_path = self.copy_and_zip_student_code(feedback, grade)

        self.clean_up_students_code()


        return {
            "grade": grade,
            "feedback": feedback,
            "zip_path": zip_path,
        }


    def get_config_from_course_by_key(self, key):
        """ Gets the configuration value from [course][key] """
        formatter = {
            'kmom': self._assignment_name,
            'acr': self._acr,
            'course': self._course_name
        }

        return self._config.get_with_format_values(key, formatter)



    def get_course_repo_dir(self):
        """ Gets the full path for the active course repo """
        return f"{self._COURSES_BASE_FOLDER}/{self._course_name}"



    def does_course_repo_exist(self):
        """ Checks if the the course repo exist """
        return os.path.exists(self.get_course_repo_dir())



    def run_shell_command_in_course_repo(self, command, print_output=False):
        """ cd into the course repo and executes shell command """
        current_app.logger.info(f"Running command {command}")
        output = subprocess.run(
            command, cwd=f"{self.get_course_repo_dir()}",
            capture_output=True,
        )
        if print_output:
            print(output.stdout.decode("utf-8"))

        if output.stderr:
            current_app.logger.error(output.stderr)

        current_app.logger.info(f"Got output {output}")

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
        current_app.logger.debug(f"Updating repo")
        update_command = self.get_config_from_course_by_key('update_command')
        self.run_shell_command_in_course_repo(update_command)

        current_app.logger.debug(f"Testing code")
        test_command = self.get_config_from_course_by_key('test_command')
        result = self.run_shell_command_in_course_repo(test_command, print_output=False)
        current_app.logger.info(f"Got exit code {result} from test command!")

        if result == 0:
            return "PG"
        if result in self.KNOWN_ERRORS: # add more know exit codes for errors when find them
            current_app.logger.error(f"Test returned {result} for {self._acr} in assignment {self._assignment_name}")
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
        dest_parent_path = self._TEMP_PATH
        dest = f"{dest_parent_path}/{dest_dir_name}"
        src_folders = self.get_config_from_course_by_key("assignment_folders")[self._assignment_name]
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
