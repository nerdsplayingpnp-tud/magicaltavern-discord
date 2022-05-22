from src.sqlite.database_handler import Connection as Handler


def db_init() -> None:
    # Handler.execute_query(Handler.create_connection(), """CREATE TABLE IF NOT EXISTS enrollments (
    #     id integer PRIMARY KEY,
    #     data blob
        
    # );""", True)
    Handler.create_table(Handler.create_connection(), """CREATE TABLE IF NOT EXISTS campaigns (
        id integer PRIMARY KEY,
        name text NOT NULL,
        players_min integer NOT NULL,
        players_max integer NOT NULL,
        open integer NOT NULL DEFAULT 1,
        date_created text NOT NULL,
        enrollments blob
    );""", True)
    return
