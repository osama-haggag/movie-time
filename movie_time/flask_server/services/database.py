import sqlite3
import pandas as pd


class DatabaseError(Exception):
    pass


class DatabaseManager:
    def __init__(self):
        self.db_connection = None
        self.db_path = None

    def query_as_df(self, query):
        df = pd.read_sql(query, self.db_connection)
        return df

    def init_app(self, app):
        self.db_path = app.config['DATABASE_PATH']
        self.db_connection = sqlite3.connect(self.db_path)


DB_MANAGER = DatabaseManager()
