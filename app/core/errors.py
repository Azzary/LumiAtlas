from fastapi import HTTPException


def bad_request(msg: str) -> HTTPException:
    return HTTPException(status_code=400, detail=msg)


def upstream_error(msg: str, status_code: int = 502) -> HTTPException:
    return HTTPException(status_code=status_code, detail=msg)
