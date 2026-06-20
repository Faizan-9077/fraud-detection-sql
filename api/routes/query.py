from fastapi import APIRouter

from api.schemas.query_request import QueryRequest
from query_engine.services.query_service import QueryService

router = APIRouter()

service = QueryService()


@router.post("/query")
async def query(request: QueryRequest):

    return service.run(request.question)