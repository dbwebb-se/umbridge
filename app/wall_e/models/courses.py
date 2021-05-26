import requests
from app.settings.api_config import API_URL, HEADERS

def get_course(course_id):
    """
    Return a single course
    based on course_id
    """
    url = API_URL + "/api/v1/courses/{course_id}".format(course_id=course_id)
    r = requests.get(url, headers=HEADERS)

    return r.json()



def get_users_in_course(course_id):
    """
    Returns users in course by course_id
    """
    url = API_URL + "/api/v1/courses/{course_id}/users?per_page=1000".format(course_id=course_id)
    r = requests.get(url, headers=HEADERS)

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
