from pydantic import BaseModel, Field

class QueryResponse(BaseModel):
    success: bool
    question: str
    sql: str
    row_count: int
    results: list


class ErrorResponse(BaseModel):
    success: bool
    question: str
    error: str