import sqlite3
from src.helper_functions import from_project_root
from src.logger.ownlogger import log


class ConnectionMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Connection(metaclass=ConnectionMeta):
    connection = sqlite3.connect(from_project_root('/data/campaign.db'))
    cursor = connection.cursor()
