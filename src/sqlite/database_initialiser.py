import sqlite3
from src.helper_functions import from_project_root
from src.logger.ownlogger import log

conn = sqlite3.connect(from_project_root('/data/campaign.db'))
cursor = conn.cursor()


def db_init() -> None:
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS campaigns (
            id integer PRIMARY KEY,
            name text NOT NULL,
            players_min integer NOT NULL,
            players_max integer NOT NULL,
            open integer NOT NULL DEFAULT 1,
            date_created text NOT NULL
        )""")
        conn.commit()
        conn.close()
        log('Table "campaigns" exists.')
    except sqlite3.OperationalError:
        log('Table "campaigns" already exists. Not creating table.')
    return
