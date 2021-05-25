import requests
import app.settings.api_config as api_config


def gradeable_submissions(course_id):
    """
    Return gradeable submissions
    based on assignment_id
    """
    url = "{api_url}/api/v1/courses/{course_id}/students/submissions".format(
            api_url=api_config.API_URL,
            course_id=course_id,
        )

    payload = {
        "student_ids": ["all"],
        "workflow_state": "submitted"
    }

    r = requests.get(url,
        headers=api_config.HEADERS,
        params=payload,
    )

    submissions = r.json()
    return submissions



def grade_submission(course_id, assignment_id, user_id, grade):
    """
    Grade submission
    """
    url = "{api_url}/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}".format(
            api_url=api_config.API_URL,
            course_id=course_id,
            assignment_id=assignment_id,
            user_id=user_id,
        )

    payload = {
        "comment": {
            "text_comment": "Automatiska rättningssystemet 'Wall-E' har gått igenom din inlämning."
        },
        "submission": {
            "posted_grade": grade
        }
    }

    requests.put(
        url,
        headers=api_config.HEADERS,
        json=payload,
    )


def get_course(course_id):
    """
    Return a single course
    based on course_id
    """
    url = api_config.API_URL + "/api/v1/courses/{course_id}".format(course_id=course_id)
    r = requests.get(url, headers=api_config.HEADERS)

    return r.json()



def get_users_in_course(course_id):
    """
    Returns users in course by course_id
    """
    url = api_config.API_URL + "/api/v1/courses/{course_id}/users?per_page=1000".format(course_id=course_id)
    r = requests.get(url, headers=api_config.HEADERS)

    return r.json()




def users_and_acronyms(course_id):
    """
    Returns users in course by course_id
    """
    users = get_users_in_course(course_id=course_id)

    formatted_users = {}

    for u in users:
        formatted_users[u["id"]] = u["login_id"].split("@")[0]

    return formatted_users



def get_user_by_acronym(acronym, course_id):
    """
    Returns a single user in course
    by acronym and course_id
    """
    users = get_users_in_course(course_id=course_id)

    return [u for u in users if "login_id" in u and acronym in u["login_id"]][0]


def get_assignments(course_id):
    """
    Return assignments
    based on course_id
    """
    url = api_config.API_URL + "/api/v1/courses/{course_id}/assignments".format(course_id=course_id)
    r = requests.get(url, headers=api_config.HEADERS)

    return r.json()

def get_assignment_by_name(name, course_id):
    """
    Return a single assingment
    based on name
    """
    assignments = get_assignments(course_id)

    return [a for a in assignments if a["name"] == name][0]