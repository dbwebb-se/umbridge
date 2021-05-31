"""
File to import settings
"""

import os
import json

APP_BASE_PATH = os.path.dirname(__file__) + "/.."

def get_course_map():
    """ Returns the course_map file as dict """
    with open(f'{APP_BASE_PATH}/settings/course_map.json') as fh:
        content = json.load(fh)
    return content
