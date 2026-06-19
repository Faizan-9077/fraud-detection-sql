from decimal import Decimal
from datetime import datetime


class ResponseFormatter:

    @staticmethod
    def format(results):

        formatted = []

        for row in results:

            clean_row = {}

            for key, value in row.items():

                if isinstance(value, Decimal):
                    clean_row[key] = float(value)

                elif isinstance(value, datetime):
                    clean_row[key] = value.isoformat()

                else:
                    clean_row[key] = value

            formatted.append(clean_row)

        return formatted