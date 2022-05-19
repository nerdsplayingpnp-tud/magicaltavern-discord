import sqlite3
import sqlite3 as db
from src.helper_functions import from_project_root
from src.logger.ownlogger import log

conn = db.connect(from_project_root('/data/campaign.db'))
cursor = conn.cursor()

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
