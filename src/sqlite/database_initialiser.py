from src.sqlite.database_handler import Connection as Handler

conn = Handler.create_connection()
cursor = Handler.create_cursor(conn)  # should probably be done differently


def db_init() -> None:
    Handler.execute_query(Handler.create_connection(), """CREATE TABLE IF NOT EXISTS enrollments (
        id integer PRIMARY KEY
        
    );""", True)
    Handler.execute_query(Handler.create_connection(), """CREATE TABLE IF NOT EXISTS campaigns (
        id integer PRIMARY KEY,
        name text NOT NULL,
        players_min integer NOT NULL,
        players_max integer NOT NULL,
        open integer NOT NULL DEFAULT 1,
        date_created text NOT NULL,
        enrollmentid INTEGER NOT NULL, 
        FOREIGN KEY(enrollmentid) REFERENCES enrollments(id)
    );""", True)
    return
