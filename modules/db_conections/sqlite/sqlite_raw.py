# -*- encoding: utf-8 -*-
import sqlite3
from modules import utils, constants


class SQLiteDB:
    def __init__(self, **kwargs):
        self.log = kwargs.get("log")
        self.db_file = kwargs.get("sqlite_file", constants.SQLITE_FILE)


    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
        except Exception as e:
            conn = None
            self.log.error(f"[SQLite3]:{utils.get_exception(e)}")
        return conn


    def execute(self, sql):
        conn = self.create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                sql = f"""PRAGMA foreign_keys = ON;
                      BEGIN TRANSACTION;
                      {sql}
                      COMMIT TRANSACTION;\n"""
                c.executescript(sql)
            except Exception as e:
                self.log.error(f"[SQLite3]:{utils.get_exception(e)}")
            conn.commit()
            conn.close()


    def select(self, sql):
        final_data = {}
        conn = self.create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute(sql)
                result_set = c.fetchall()
                column_names = list(map(lambda x: x[0], c.description))
                for line_number, data in enumerate(result_set):
                    final_data[line_number] = {}
                    for column_number, value in enumerate(data):
                        if isinstance(value, str) and value is not None and len(value) == 0:
                            value = None
                        final_data[line_number][column_names[column_number]] = value
            except Exception as e:
                self.log.error(f"[SQLite3]:{utils.get_exception(e)}")
            conn.commit()
            conn.close()
        return final_data
