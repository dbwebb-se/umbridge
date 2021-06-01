"""

"""
import os
from app.wall_e.models.requester import Requester
from app.settings import settings
from canvasapi import submission, requester


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
        self.assignments = self.get_assignments()


    def get_users_in_course(self):
        """
        Returns users in course by course_id
        """
        return self._request_get(
            f"/api/v1/courses/{self.course_id}/users?per_page=1000").json()
    
    def get_assignments(self):
        """
        Return assignments
        based on course_id
        """

        return self._request_get(
            f"/api/v1/courses/{self.course_id}/assignments").json()


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
            formatted_users[u["id"]] = u["login_id"].split("@")[0]

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

        return [a["name"] for a in self.assignments if a["id"] == assignment_id][0]


    def get_gradeable_submissions(self):
        """
        Return gradeable submissions
        based on assignment_id
        """
        submissions = self._request_get(
            f"/api/v1/courses/{self.course_id}/students/submissions", payload={
                "student_ids": ["all"],
                "workflow_state": ["submitted"],

            }
        ).json()

        try:
            ignore = self._config[self._course_name]['ignore_assignments']
        except KeyError:
            ignore = self._config['default']['ignore_assignments']

        if ignore:
            submissions = [
                s for s in submissions if self.get_assignment_name_by_id(s['assignment_id']) not in ignore
            ]

        return submissions

class Grader(Requester):
    """
    Model class for wall_e.grade
    """

    def __init__(self, base_url, api_token):
        super().__init__(base_url, api_token)

    def grade_submission(self, sub):
        """
        Grade submission
        """
        payload = {
            "comment": {
                "text_comment": "Automatiska rättningssystemet 'Umbridge' har gått igenom din inlämning.",
            },
            "submission": {
                "posted_grade": sub.grade
            }
        }

        self._request_put(
            f"/api/v1/courses/{sub.course_id}/assignments/{sub.assignment_id}/submissions/{sub.user_id}",
            payload=payload)

        self.create_and_send_logfile(sub)


    def create_and_send_logfile(self, sub):
        """
        Creates a temporary log file
        and sends it as a comment
        """
        file_name = f"{settings.APP_BASE_PATH}/wall_e/temp/feedback_{sub.assignment_name}_{sub.user_acronym}.txt"

        with open(file_name, "w+") as fh:
            fh.write(sub.feedback)

        r = requester.Requester(self._url, self._key)
        s = submission.Submission(
            r, attributes={
            "course_id": sub.course_id,
            "assignment_id": sub.assignment_id,
            "user_id": sub.user_id
        })

        s.upload_comment(file_name)
        os.remove(file_name)
