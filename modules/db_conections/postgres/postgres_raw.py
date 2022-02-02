# -*- coding: utf-8 -*-
import asyncpg


class DBPostgreSQL:
    def __init__(self, **kwargs):
        self.log = kwargs.get("log")
        self.host = kwargs.get("host")
        self.port = kwargs.get("port")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.database = kwargs.get("database")


    async def create_connection(self):
        try:
            conn = await self._get_connection()
        except asyncpg.InvalidCatalogNameError:
            await self.create_database(self.database)
            conn = await self._get_connection()
        except Exception as e:
            conn = None
            self.log.error(f"PostgreSQL:({e.args})")
            # self.log.exception("PostgreSQL", exc_info=e)
            # raise asyncpg.ConnectionFailureError(e)
        return conn


    async def execute(self, sql: str):
        conn = await self.create_connection()
        if conn is not None:
            try:
                await conn.execute(sql)
            except Exception as e:
                self.log.exception("PostgreSQL", exc_info=e)
                self.log.error(f"Sql:({sql})")
                raise asyncpg.InvalidTransactionStateError(e)
            finally:
                await conn.close()


    async def select(self, sql: str):
        final_data = {}
        conn = await self.create_connection()
        if conn is not None:
            try:
                result_set = await conn.fetch(sql)
                for line_number, data in enumerate(result_set):
                    final_data[line_number] = dict(data)
            except Exception as e:
                self.log.exception("PostgreSQL", exc_info=e)
                self.log.error(f"Sql:({sql})")
            finally:
                await conn.close()
        return final_data


    async def create_database(self, database: str):
        conn = await self._get_connection(database=False)
        sql = f"CREATE DATABASE \"{database}\""
        if conn is not None:
            try:
                await conn.execute(sql)
                msg = f"Database: {database} created"
                self.log.info(msg)
            except Exception as e:
                self.log.exception("PostgreSQL", exc_info=e)
                self.log.error(f"Sql:({sql})")
            finally:
                await conn.close()


    async def _get_connection(self, database=True):
        if database:
            conn = await asyncpg.connect(user=self.username,
                                         password=self.password,
                                         database=self.database,
                                         port=self.port,
                                         host=self.host)
        else:
            conn = await asyncpg.connect(user=self.username,
                                         password=self.password,
                                         port=self.port,
                                         host=self.host)
        return conn
