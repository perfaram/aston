__name__ = "exOTP"
__author__ = "Mathis Rodriguez, Perceval Faramaz"
__copyright__ = "Copyright 2024"
__license__ = "MIT"
__version__ = "1.0.0"

from .utils import get_if_exists
import sys


class Configuration:

    _single_instance = None

    @classmethod
    def get_instance(cls):
        if not isinstance(cls._single_instance, Configuration):
            cls._single_instance = Configuration()
        return cls._single_instance

    def __init__(self):
        self.__dict__ = {
            "app_details": {
                "name": __name__,
                "author": __author__,
                "copyright": __copyright__,
                "license": __license__,
                "version": __version__
            },
            "database_path": 'sqlite:///database.db'
        }

    def add_element(self, key, value):
        self.__dict__[key] = value

    def get_element(self, key, default=None):
        return get_if_exists(self.__dict__, key, default)

    def __getitem__(self, key):
        return self.get_element(key)

    def __str__(self):
        return self.__dict__.__str__()
