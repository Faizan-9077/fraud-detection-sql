from query_engine.services.sql_generator import SQLGenerator


generator = SQLGenerator()

sql = generator.generate_sql(
    "Show possible account takeover cases."
)

print(sql)