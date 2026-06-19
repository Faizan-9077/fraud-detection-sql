from query_engine.services.query_executor import QueryExecutor


sql = """
SELECT *
FROM vw_transaction_core
LIMIT 5;
"""

rows = QueryExecutor.execute(sql)

print(rows)
print(type(rows))