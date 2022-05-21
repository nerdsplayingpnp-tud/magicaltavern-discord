import sqlite3
from src.helper_functions import from_project_root
from src.logger.ownlogger import log
from src.sqlite.database_handler import Connection as Handler

conn = Handler.create_connection()
cursor = conn.cursor()  # should probably be done differently


def db_init() -> None:
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS enrollments (
            id integer PRIMARY KEY
            
        );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS campaigns (
            id integer PRIMARY KEY,
            name text NOT NULL,
            players_min integer NOT NULL,
            players_max integer NOT NULL,
            open integer NOT NULL DEFAULT 1,
            date_created text NOT NULL
        );""")
        conn.commit()
        conn.close()
        log('Table "campaigns" exists.')
    except sqlite3.OperationalError:
        log('Table "campaigns" already exists. Not creating table.')
    return
