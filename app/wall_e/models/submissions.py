import requests
import os
from app.settings.api_config import API_URL, HEADERS, API_KEY

from canvasapi import submission, requester

app_base_path = os.path.dirname(__file__) + "/../.."

def gradeable_submissions(course_id):
    """
    Return gradeable submissions
    based on assignment_id
    """
    url = f"{API_URL}/api/v1/courses/{course_id}/students/submissions"

    payload = {
        "student_ids": ["all"],
        "workflow_state": ["submitted"]
    }

    r = requests.get(url,
        headers=HEADERS,
        params=payload,
    )

    submissions = r.json()

    return submissions



def grade_submission(sub):
    """
    Grade submission
    """
    url = "{api_url}/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}".format(
            api_url=API_URL,
            course_id=sub.course_id,
            assignment_id=sub.assignment_id,
            user_id=sub.user_id,
        )

    payload = {
        "comment": {
            "text_comment": "Automatiska rättningssystemet 'Umbridge' har gått igenom din inlämning.",
        },
        "submission": {
            "posted_grade": sub.grade
        }
    }

    r = requests.put(
        url,
        headers=HEADERS,
        json=payload,
    )

    file_name = f"{app_base_path}/feedback_{sub.kmom}_{sub.user_acronym}.txt"
    with open(file_name, "w+") as fh:
        fh.write(sub.feedback)

    r = requester.Requester(API_URL, API_KEY)
    s = submission.Submission(r, attributes={"course_id": sub.course_id, "assignment_id": sub.assignment_id,"user_id":sub.user_id})
    s.upload_comment(file_name)


    os.remove(file_name)