"""

"""
import os
from flask import current_app
from canvasapi import submission, requester
from app.wall_e.models.requester import Requester
from app.settings import settings


class Canvas(Requester):
    """
    Model class for wall_e.fetch
    """
    def __init__(self, base_url, api_token, course_id, course_name):
        super().__init__(base_url, api_token)

        self.course_id = course_id
        self._course_name = course_name
        self._config = settings.get_course_map()
        self.set_assignments_and_users()

    def set_assignments_and_users(self):
        """ Caches assignments and students in a course """
        self.users = self.get_users_in_course()
        current_app.logger.debug(f"Course {self._course_name} has the following users: {self.users}")
        self.assignments = self.get_assignments()
        current_app.logger.debug(f"Course {self._course_name} has the following assignments: {self.assignments}")


    def get_users_in_course(self):
        """
        Returns users in course by course_id
        """
        data = self.request_get_paging(
            f"/api/v1/courses/{self.course_id}/users?page={{page}}&per_page=100")
        return data

    def get_assignments(self):
        """
        Return assignments
        based on course_id
        """
        return self._request_get(
            f"/api/v1/courses/{self.course_id}/assignments?per_page=100").json()


    def get_course(self):
        """
        Return a single course
        based on course_id
        """
        return self._request_get(f"/api/v1/courses/{self.course_id}").json()

    def users_and_acronyms(self):
        """
        Returns users in course by course_id
        """
        formatted_users = {}
        for u in self.users:
            try:
                formatted_users[u["id"]] = u["login_id"].split("@")[0]
            except TypeError:
                current_app.logger.error(f"could not extract acronym for user {u}")
            except KeyError:
                current_app.logger.error(f"could not find key 'login_id' for {u}")


        return formatted_users

    def get_user_by_acronym(self, acronym):
        """
        Returns a single user in course
        by acronym and course_id
        """
        return [
            u for u in self.users if "login_id" in u and acronym in u["login_id"]
        ][0]


    def get_assignment_by_name(self, name):
        """
        Return a single assignment
        based on name
        """
        return [a for a in self.assignments if a["name"] == name][0]



    def get_assignment_name_by_id(self, assignment_id):
        """
        Return a single assignment
        based on its id
        """
        for assignment in self.assignments:
            if assignment["id"] == assignment_id:
                name = self._config[self._course_name]['canvas_name_to_assignment'].get(
                    assignment["name"],
                    assignment["name"]
                )
                current_app.logger.debug(f"Found the name {name} for assignment {assignment['name']}")

                return name
        current_app.logger.error(f"could not find a matching assignment id to {assignment['id']}")
        return None



    def get_gradeable_submissions(self):
        """
        Return gradeable submissions
        based on assignment_id
        """
        # submitted = all assignments that has not been graded on canvas
        submissions = self.request_get_paging(
            f"/api/v1/courses/{self.course_id}/students/submissions?page={{page}}&per_page=100", payload={
                "student_ids": ["all"],
                "workflow_state": ["submitted"],
            }
        )

        current_app.logger.info(f"Course {self._course_name} has {len(submissions)} submissions")
        current_app.logger.debug(f"Course {self._course_name} has the following submissions: {submissions}")

        try:
            ignore = self._config[self._course_name]['ignore_assignments']
        except KeyError:
            ignore = self._config['default']['ignore_assignments']

        if ignore:
            submissions = [
                s for s in submissions if self.get_assignment_name_by_id(s['assignment_id']) not in ignore
            ]

        return submissions



    def get_graded_submissions(self, assignment):
        """
        Return already graded submissions
        based on assignment name
        """
        submissions = self.request_get_paging(
            f"/api/v1/courses/{self.course_id}/students/submissions?page={{page}}&per_page=100", payload={
                "student_ids": ["all"],
                "workflow_state": ["graded"],
                "assignment_ids": self.get_assignment_by_name(assignment)["id"],
            }
        )

        current_app.logger.info(f"Course {self._course_name} has {len(submissions)} already graded submissions")
        current_app.logger.debug(f"Course {self._course_name} has the following already graded submissions: {submissions}")

        try:
            ignore = self._config[self._course_name]['ignore_assignments']
        except KeyError:
            ignore = self._config['default']['ignore_assignments']

        if ignore:
            submissions = [
                s for s in submissions if assignment not in ignore
            ]

        return submissions

class Grader(Requester):
    """
    Model class for wall_e.grade
    """

    def __init__(self, base_url, api_token):
        super().__init__(base_url, api_token)

    def grade_submission(self, sub, url):
        """
        Grade submission
        """
        passed_comment = "Testerna har passerat. En r??ttare kommer l??sa din redovisningstext, kolla p?? koden och s??tta betyg."
        failed_comment = "Tyv??rr gick n??got fel i testerna. L??s igenom loggfilen f??r att se vad som gick fel. L??s felet och g??r en ny inl??mning."
        error_comment = "N??got gick fel i umbridge, kontakta kursansvarig."

        respons = self.send_zip_archive(sub)

        if respons is not None:
            if sub.grade.lower() == "pg":
                feedback = passed_comment
            elif sub.grade.lower() == "ux":
                feedback = failed_comment
            else:
                feedback = error_comment

            id_ = respons["id"]
            uuid = respons["uuid"]

            feedback_text = (
                "Automatiska r??ttningssystemet 'Umbridge' har g??tt igenom din inl??mning.\n\n"
                f"{feedback}\n\n"
                f"Loggfilen f??r alla tester kan du se via f??ljande l??nk: {url}/results/feedback/{sub.uuid}-{sub.id}\n\n"
                f"Du kan inspektera filerna som anv??ndes vid r??ttning via f??ljande l??nk: {url}/results/inspect/{id_}/{uuid}\n\n"
                "Kontakta en av de kursansvariga om resultatet ??r felaktigt."
            )
        else:
            feedback_text = (
                "Automatiska r??ttningssystemet 'Umbridge' har g??tt igenom din inl??mning.\n\n"
                f"Umbridge kunde inte hitta filerna efter r??ttningen, f??rs??k g??ra en ny inl??mning. Om det inte hj??lper, kontakta kursansvarig.\n\n"
                f"Loggfilen f??r alla tester kan du se via f??ljande l??nk: {url}/results/feedback/{sub.uuid}-{sub.id}\n\n"
            )

        payload = {
            "comment": {
                "text_comment": feedback_text,
            },
            "submission": {
                "posted_grade": sub.grade
            }
        }

        current_app.logger.debug(f"Set grade {sub.grade} for {sub.user_acronym} in assignment {sub.assignment_id}")

        self._request_put(
            f"/api/v1/courses/{sub.course_id}/assignments/{sub.assignment_id}/submissions/{sub.user_id}",
            payload=payload)



    def send_zip_archive(self, sub):
        """
        Sends archive as a comment
        """
        file_name = sub.zip_file_path

        r = requester.Requester(self._url, self._key)
        s = submission.Submission(
            r, attributes={
            "course_id": sub.course_id,
            "assignment_id": sub.assignment_id,
            "user_id": sub.user_id
        })
        current_app.logger.debug(f"Sending zip as comment to {sub.user_acronym} in assignment {sub.assignment_id}")
        try:
            respons = s.upload_comment(file_name)
        except IOError:
            current_app.logger.error(f"File {file_name} is missing, can't upload file for {sub.user_acronym} in {sub.assignment_name}.")
            sub.grade = "U"
            return None
        current_app.logger.debug(f"zip respons: {respons}")
        os.remove(file_name)
        return respons[1]
