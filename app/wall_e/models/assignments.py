import requests
from app.settings.api_config import API_URL, HEADERS


def get_assignments(course_id):
    """
    Return assignments
    based on course_id
    """
    url = API_URL + "/api/v1/courses/{course_id}/assignments".format(course_id=course_id)
    r = requests.get(url, headers=HEADERS)

    return r.json()



def get_assignment_by_name(name, course_id):
    """
    Return a single assignment
    based on name
    """
    assignments = get_assignments(course_id)

    return [a for a in assignments if a["id"] == name][0]



def get_assignment_name_by_id(assignment_id, course_id):
    """
    Return a single assignment
    based on its id
    """
    assignments = get_assignments(course_id)

    return [a["name"] for a in assignments if a["id"] == assignment_id][0]
