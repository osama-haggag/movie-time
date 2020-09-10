import sqlite3
from functools import wraps

import pandas as pd

from flask_server import settings


class DatabaseError(Exception):
    pass


def get_database_connection(database_path=settings.DATABASE_PATH):
    connection = sqlite3.connect(database_path)
    return connection


def execute_query(db_connection, query):
    df = pd.read_sql(query, db_connection)
    return df


def catch_database_error(func, logger):
    @wraps(func)
    def db_interaction(*args, **kwargs):
        try:
            yield from func(*args, **kwargs)
        except Exception:
            logger.exception("DB interaction failed: ")
    return db_interaction
