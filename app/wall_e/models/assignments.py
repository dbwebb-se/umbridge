import requests
import app.settings.api_config as api_config


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