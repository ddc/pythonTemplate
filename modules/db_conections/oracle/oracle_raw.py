# -*- coding: utf-8 -*-
import sys
import cx_Oracle
from modules import utils, messages


class OracleDB:
    def __init__(self, **kwargs):
        self.batch_size = kwargs.get("batch_size", 10000)
        self.log = kwargs.get("log")
        self.host = kwargs.get("host")
        self.port = kwargs.get("port")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.servicename = kwargs.get("servicename")


    def create_connection(self):
        dsn = f"""
            (DESCRIPTION=
                (ADDRESS=
                    (PROTOCOL=TCP)
                    (HOST={self.host})
                    (PORT={self.port}))
                (CONNECT_DATA=
                    (SERVER=DEDICATED)
                    (SERVICE_NAME={self.servicename})
                    (FAILOVER_MODE=
                        (TYPE=select)
                        (METHOD=basic))))"""

        try:
            connection = cx_Oracle.connect(self.username, self.password, dsn, encoding="UTF-8")
            return connection
        except Exception as e:
            if hasattr(e, "args"):
                if len(e.args) > 0:
                    self.log.error(f"[ORA]:{messages.DB_CONN_ERROR}:"
                                   f"(host={self.host}, port={self.port}, servicename={self.servicename}):"
                                   f"{e.args[0]}")
            else:
                self.log.error(f"[ORA]:{utils.get_exception(e)}")
            sys.exit(1)


    def execute(self, query):
        with self.create_connection() as connection:
            if connection is not None:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute(query.replace(";", ""))
                    except cx_Oracle.DatabaseError as e:
                        if "ORA-00955" not in str(e):
                            return self.log.error(f"[ORA]:{utils.get_exception(e)}")
                    except Exception as e:
                        return self.log.error(f"[ORA]:{utils.get_exception(e)}")
                    connection.commit()


    def select(self, query):
        final_data = None
        with self.create_connection() as connection:
            if connection is not None:
                with connection.cursor() as cursor:
                    try:
                        if query is not None:
                            final_data = {}
                            results = cursor.execute(query)
                            while True:
                                rows = results.fetchmany(self.batch_size)
                                column_names = list(map(lambda x: x[0], cursor.description))
                                for line_number, data in enumerate(rows):
                                    final_data[line_number] = {}
                                    for column_number, value in enumerate(data):
                                        final_data[line_number][column_names[column_number]] = value
                                if len(final_data) == 0:
                                    final_data = None
                                if not rows:
                                    break
                    except Exception as e:
                        self.log.warning(f"[ORA]:{utils.get_exception(e)}")
                        final_data = None
            return final_data
