"""
Class to work with settings
"""

import os
import json

APP_BASE_PATH = os.path.dirname(__file__) + "/.."

class Config():
    """
    Custom config class.
    Will use default's key in course's key is missing 
    """

    def __init__(self, course_name):
        self.course_name = course_name
        with open(f'{APP_BASE_PATH}/settings/course_map.json') as fh:
            self._config = json.load(fh) 

    def __getitem__(self, key):
        if key in self._config[self.course_name]:
            return self._config[self.course_name][key]
        return self._config["default"][self._config[self.course_name]]
