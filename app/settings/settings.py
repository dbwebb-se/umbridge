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
        return self._config["default"][key]


    def get_with_format_values(self, key, values):
        """
        For config where strings are dynamic, use str.format to insert values
        """
        return self._recursive_format(self[key], values)



    def _recursive_format(self, config, formatter):
        """
        Recursively use str.format on all string values in settings
        """
        if isinstance(config, str):
            return config.format(**formatter)
        elif isinstance(config, list):
            return [self._recursive_format(value, formatter) for value in config]
        elif isinstance(config, dict):
            return {key:self._recursive_format(value, formatter) for key, value in config.items()}
        return config
