# query_engine/services/query_service.py

from query_engine.services.sql_generator import SQLGenerator
from query_engine.services.sql_validator import SQLValidator
from query_engine.services.query_executor import QueryExecutor
from query_engine.services.response_formatter import ResponseFormatter


class QueryService:

    def __init__(self):
        self.generator = SQLGenerator()

    def run(self, question: str):

        sql = self.generator.generate_sql(question)

        validated_sql = SQLValidator.validate(sql)

        results = QueryExecutor.execute(validated_sql)

        results = ResponseFormatter.format(results)

        return {
            "success": True,
            "question": question,
            "sql": validated_sql,
            "row_count": len(results),
            "results": results,
        }