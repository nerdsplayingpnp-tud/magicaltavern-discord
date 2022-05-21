import sqlite3
from src.helper_functions import from_project_root
from src.logger.ownlogger import log

conn = sqlite3.connect(from_project_root('/data/campaign.db'))
cursor = conn.cursor()


def db_init() -> None:
    try:
        cursor.execute("""CREATE TABLE campaigns (
            name text,
            minp integer,
            maxp integer
        )""")
        conn.commit()
        log('Table "campaigns" created.')
    except sqlite3.OperationalError:
        log('Table "campaigns" already exists. Not creating table.')
    return
