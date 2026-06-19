# query_engine/services/query_executor.py

import psycopg2
from psycopg2.extras import RealDictCursor

from database.db_config import DB_CONFIG


class QueryExecutor:

    @staticmethod
    def execute(sql: str):

        connection = None

        try:

            connection = psycopg2.connect(**DB_CONFIG)

            with connection.cursor(
                cursor_factory=RealDictCursor
            ) as cursor:

                cursor.execute(sql)

                results = cursor.fetchall()

                return [dict(row) for row in results]

        except psycopg2.Error as e:

            raise RuntimeError(
                f"Database execution failed."
            ) from e

        finally:

            if connection:
                connection.close()