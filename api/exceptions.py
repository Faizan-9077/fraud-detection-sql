class QueryGenerationError(Exception):
    """Raised when SQL generation fails."""
    pass


class DatabaseExecutionError(Exception):
    """Raised when database execution fails."""
    pass