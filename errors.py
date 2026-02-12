from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Optional


class ErrorCode:
    """API Error Codes"""
    LIMIT_EXCEEDED = "LIMIT_EXCEEDED"
    GOVERNANCE_VIOLATION = "GOVERNANCE_VIOLATION"
    INVALID_INPUT = "INVALID_INPUT"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class APIException(Exception):
    """Structured exception for API errors"""
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: Optional[dict] = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers for the FastAPI app"""
    
    @app.exception_handler(APIException)
    async def api_exception_handler(request, exc: APIException):
        response = {
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
        if exc.details:
            response["error"]["details"] = exc.details
        
        return JSONResponse(
            status_code=exc.status_code,
            content=response
        )
