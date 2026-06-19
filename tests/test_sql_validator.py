from query_engine.services.sql_validator import SQLValidator

sql = """
DROP TABLE transactions;
"""

print(SQLValidator.validate(sql))