# -*- coding: utf-8 -*-
import sys
from sqlalchemy import event
from sqlalchemy.engine import create_engine
from modules import utils, messages, constants


class SQLiteDB:
    def __init__(self, **kwargs):
        self.log = kwargs.get("log")
        self.batch_size = kwargs.get("batch_size", 10000)
        self.db_file = kwargs.get("sqlite_file", constants.SQLITE_FILE)

    def create_engine(self):
        try:
            engine = create_engine(f"sqlite:///{self.db_file}", echo=False).\
                execution_options(stream_results=False,
                                  isolation_level="AUTOCOMMIT")

            @event.listens_for(engine, "before_cursor_execute")
            def receive_before_cursor_execute(conn,
                                              cursor,
                                              statement,
                                              params,
                                              context,
                                              executemany):
                cursor.arraysize = self.batch_size
            return engine
        except Exception as e:
            self.log.error(
                f"[{utils.get_exception(e)}]:{messages.DB_CONN_CREATE_ERROR}"
            )
            return None

    def execute(self, query):
        self.log.debug(f"[SQLite]:[Execute]:{query}")
        engine = self.create_engine()
        if engine is not None:
            with engine.connect() as connection:
                try:
                    connection.execute(query)
                    return True
                except Exception as e:
                    self.log.error(utils.get_exception(e))
        return False

    def select(self, query):
        self.log.debug(f"[SQLite]:[Select]:{query}")
        final_data = []
        engine = self.create_engine()
        if engine is not None:
            with engine.connect() as connection:
                try:
                    if query is not None:
                        rows = connection.execute(query)
                        column_names = tuple(map(
                            lambda x: x[0], rows.cursor.description
                        ))
                        all_data = tuple(x for x in rows)
                        for data in all_data:
                            final_data.append(dict(zip(column_names, data)))
                except Exception as e:
                    if hasattr(self, "log") and self.log is not None:
                        self.log.warning(utils.get_exception(e))
                    else:
                        sys.stderr.write(utils.get_exception(e))
                    final_data = []
        return final_data if len(final_data) > 0 else []
