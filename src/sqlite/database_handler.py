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
    def create_cursor(conn: sqlite3.Connection) -> sqlite3.Cursor:
        """
        Creates a cursor from a given connection.
        @param conn: An sqlite3 Connection object
        """
        return conn.cursor()

    @staticmethod
    def create_table(conn: sqlite3.Connection, create_table_statement: str, verbose: bool = False) -> None:
        """
        Create a table with a given connection.
        @param verbose: Whether a successful database entry should be logged or not.
        @param conn: Connection to a database
        @param create_table_statement: An sqlite3 create_table_statement.
        @return: None
        """
        try:
            c = Connection.create_cursor(conn)
            c.execute(create_table_statement)
            conn.commit()
            conn.close()
            if verbose:
                log(str(create_table_statement + " was succesfully executed."))
        except sqlite3.OperationalError as e:
            log(str(e), "red")

    @staticmethod
    def execute_queery(conn: sqlite3.Connection, create_table_statement: str, verbose: bool = False) -> None:
        """
        A littol easteregg c: 🏳‍🌈
        """
        Connection.create_table(conn, create_table_statement, verbose)

    @staticmethod
    def insert_into_campaigns(conn: sqlite3.Connection, name: str, players_min: int, players_max: int,
                              date_created: str, enrollments) -> int:
        """
        Insert data into a given table.
        @param enrollments: TODO Write Docstring
        @param date_created:
        @param players_max:
        @param players_min:
        @param name:
        @param conn: Connection to a database
        """
        ins = f"""INSERT INTO campaigns(name, players_min, players_max, date_created, enrollments) VALUES(?,?,?,?,?)"""
        cursor = Connection.create_cursor(conn)
        try:
            values = [name, players_min, players_max, date_created, enrollments]
            cursor.execute(ins, values)
            conn.commit()
            return cursor.lastrowid
        except sqlite3.OperationalError as e:
            log(str(e), "red")
