# query_engine/services/query_service.py

from query_engine.services.sql_generator import SQLGenerator
from query_engine.services.sql_validator import (
    SQLValidator,
    SQLValidationError,
)
from query_engine.services.query_executor import QueryExecutor
from query_engine.services.response_formatter import ResponseFormatter


class QueryService:

    def __init__(self):
        self.generator = SQLGenerator()

    def run(self, question: str):

        try:

            # Step 1: Generate SQL
            sql = self.generator.generate_sql(question)

            # Step 2: Validate SQL
            validated_sql = SQLValidator.validate(sql)

            # Step 3: Execute SQL
            results = QueryExecutor.execute(validated_sql)

            # Step 4: Format Results
            results = ResponseFormatter.format(results)

            return {
                "success": True,
                "question": question,
                "sql": validated_sql,
                "row_count": len(results),
                "results": results,
            }

        except SQLValidationError as e:

            return {
                "success": False,
                "question": question,
                "error": f"SQL validation failed: {str(e)}",
            }

        except RuntimeError as e:

            return {
                "success": False,
                "question": question,
                "error": str(e),
            }

        except Exception:

            return {
                "success": False,
                "question": question,
                "error": "Unexpected server error.",
            }