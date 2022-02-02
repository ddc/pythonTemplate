# -*- coding: utf-8 -*-
from sqlalchemy.engine import create_engine
from modules import utils, messages


class OracleDB:
    def __init__(self, **kwargs):
        self.batch_size = kwargs.get("batch_size", 10000)
        self.log = kwargs.get("log")
        self.host = kwargs.get("host")
        self.port = int(kwargs.get("port"))
        self.servicename = kwargs.get("servicename")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.tablename = kwargs.get("tablename").upper()


    def create_engine(self):
        dialect = "oracle"
        sql_driver = "cx_oracle"

        tns = f"""
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
            engine_path_win_auth = f"{dialect}+{sql_driver}://{self.username}:{self.password}@{tns}"
            engine = create_engine(engine_path_win_auth,
                                   max_identifier_length=128).execution_options(isolation_level="AUTOCOMMIT")
            return engine
        except Exception as e:
            self.log.error(f"{messages.DB_CONN_ERROR}:[{utils.get_exception(e)}]: "
                           f"(host={self.host}, port={self.port}, "
                           f"servicename={self.servicename}, username={self.username})")
            return None


    def insert(self, table, values: dict):
        self.log.debug(f"[ORA]:[insert]:{table}:{values}")
        engine = self.create_engine()
        if engine is not None:
            try:
                with engine.connect() as connection:
                    connection.execute(table.insert(), values)
            except Exception as e:
                self.log.error(utils.get_exception(e))
