from fastapi.responses import JSONResponse


def create_error_response(message: str, status: int, detail=None) -> JSONResponse:
    """Creating JSON error response"""
    content = {
        "message": message,
        "status": status,
    }
    if detail:
        content["detail"] = detail
    return JSONResponse(content=content, status_code=status)
