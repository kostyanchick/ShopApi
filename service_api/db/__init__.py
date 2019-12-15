from http import HTTPStatus

import psycopg2
import psycopg2.extras
from psycopg2.errors import UniqueViolation

from .maindb import set_up_tables, drop_all_tables


class PGConnection:
    """Handles the main connection to the database"""

    def __init__(self, pg_url):

        try:
            self.conn = psycopg2.connect(pg_url)
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except Exception as ex:
            print(ex)

    def _execute_query(self, query, params=None, success_status=HTTPStatus.OK.value):
        try:
            self.cur.execute(query, params)
            self.conn.commit()
        except psycopg2.OperationalError as ex:
            self.conn.rollback()
            return str(ex), HTTPStatus.SERVICE_UNAVAILABLE.value
        except UniqueViolation as ex:
            self.conn.rollback()
            return str(ex), HTTPStatus.CONFLICT.value
        return self.cur, success_status

    def create_all_tables(self):
        """Executes query creating all tables"""
        tables_to_create = set_up_tables()
        for query in tables_to_create:
            self.cur.execute(query)
        self.conn.commit()

    def drop_all_tables(self):
        """Executes query deleting all tables"""
        tables_to_delete = drop_all_tables()
        for query in tables_to_delete:
            self.cur.execute(query)
        self.conn.commit()

    def save_income_data(self, query, params=None):
        """Executes given query"""
        result, status = self._execute_query(query, params, success_status=HTTPStatus.CREATED.value)
        if status == HTTPStatus.CREATED.value:
            result = self.cur.fetchall()

        return result, status

    def fetch_one_row(self, query, params=None):
        """Retrieves single row by given query"""
        result, status = self._execute_query(query, params)
        if status == HTTPStatus.OK.value:
            result = self.cur.fetchone()

        return result, status

    def fetch_all(self, query, params=None):
        """Retrieves all results for query"""
        result, status = self._execute_query(query, params)
        if status == HTTPStatus.OK.value:
            result = self.cur.fetchall() or []

        return result, status
