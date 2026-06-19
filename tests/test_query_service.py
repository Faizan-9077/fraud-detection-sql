from query_engine.services.query_service import QueryService

service = QueryService()

response = service.run(
    "Show transactions above 5 lakh between 11 PM and 4 AM"
)

print(response["sql"])
print(response["row_count"])

if response["results"]:
    print(response["results"][0])