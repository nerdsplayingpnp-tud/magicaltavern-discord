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

    @staticmethod
    def create_connection() -> sqlite3.Connection:
        """
        Used to create the connection to the campaign.db file.
        @return: The connection object
        """
        conn = None
        try:
            conn = sqlite3.connect(from_project_root('/data/campaign.db'))
            return conn
        except sqlite3.OperationalError as e:
            log(str(e), "red")
        return conn

    @staticmethod
    def create_table(conn: sqlite3.Connection, create_table_statement: str) -> None:
        """
        Create a table with a given connection.
        @param conn: Connection to a database
        @param create_table_statement: An sqlite3 create_table_statement.
        @return: None
        """
        try:
            c = conn.cursor()
            c.execute(create_table_statement)
            conn.commit()
        except sqlite3.OperationalError as e:
            log(str(e), "red")
