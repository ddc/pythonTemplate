# -*- coding: utf-8 -*-
import sys
import logging.handlers
from modules import utils, messages
from pymongo import MongoClient, DESCENDING, ASCENDING


class MongoUtils:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.log = kwargs.get("log")
        self.debug = kwargs.get("debug")
        self.host = kwargs.get("host")
        self.port = kwargs.get("port")
        self.user = kwargs.get("user")
        self.password = kwargs.get("password")
        self.schema = kwargs.get("schema")
        self.collections = kwargs.get("collections")
        self.authsource = kwargs.get("authsource", None)
        self.batch_size = kwargs.get("batch_size", 0)
        self.limit = kwargs.get("limit", 0)
        logging.getLogger("pymongo").setLevel(logging.DEBUG) if self.debug \
            else logging.getLogger("pymongo").setLevel(logging.ERROR)
        self.init_log_msg = "[MONGODB]:[{}]:[{}:{}]".format(self.id,
                                                            self.host,
                                                            self.port)


    def get_db_connection(self):
        self.log.debug(f"{self.init_log_msg}:{messages.DB_CONN_STARTING}")
        error_msg = f"{self.init_log_msg}:[{messages.ERROR_ABORT}]:{messages.DB_CONN_ERROR}:"
        mongo_client = None

        try:
            conn_string = self._get_connection_string()
            mongo_client = MongoClient(conn_string)
        except Exception as e:
            mongo_client.close() if mongo_client else None
            self.log.error(f"{error_msg}:{utils.get_exception(e)}")
            sys.exit(1)

        if self.collections is not None and len(self.collections) > 0:
            try:
                self.log.debug(f"{self.init_log_msg}:{messages.DB_CONN_CHECKING}")
                for col in self.collections:
                    with mongo_client[self.schema][col].find({"_id": 1}) as cursor:
                        for _ in cursor: break
            except Exception as e:
                from pymongo.errors import OperationFailure
                if isinstance(e, OperationFailure) and hasattr(e, "code") and e.code == 13:
                    error_msg += f":{messages.PERMISSION_DENIED}"
                error_msg += f":{utils.get_exception(e)}"
                self.log.error(error_msg)
                sys.exit(1)

        self.log.debug(f"{self.init_log_msg}:{messages.DB_CONN_SUCCESS}")
        return mongo_client


    def get_cursor(self, connection, query, collection, sort_column=None, sort_direction=None):
        col = connection[self.schema][collection]
        if sort_column is not None and sort_direction is not None:
            sort_direction = DESCENDING if sort_direction.lower() in ["descending", "desc"] else ASCENDING
            col.create_index([(sort_column, sort_direction)])
        cursor = col.find(query, batch_size=self.batch_size, limit=self.limit)
        cursor.batch_size(self.batch_size)
        return cursor


    def _get_connection_string(self):
        import re
        if self.user is not None and self.password is not None and len(self.user) > 0 and len(self.password) > 0:
            conn_string = f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.schema}"
        else:
            conn_string = f"mongodb://{self.host}:{self.port}/{self.schema}"
        if self.authsource is not None and len(self.authsource) > 0:
            conn_string += f"?authSource={self.authsource}"
        hidden_conn = conn_string
        if self.password is not None and len(self.password) > 0:
            hidden_conn = re.sub(self.password, messages.PASSWORD_HIDDEN_MSG, conn_string, flags=re.DOTALL)
        self.log.debug(f"{self.init_log_msg}:{messages.DB_CONN_STRING}: {hidden_conn}")
        return conn_string
