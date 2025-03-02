from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    """Base class for custom exceptions with formatted response"""

    def __init__(self, status_code: int, detail: str, headers=None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


# --- Authentication Errors ---
CREDENTIALS_EXCEPTION = CustomHTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

INACTIVE_USER_EXCEPTION = CustomHTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
)

INSUFFICIENT_PERMISSION_EXCEPTION = CustomHTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
)

# --- Generic Errors ---
NOT_FOUND_EXCEPTION = lambda entity: CustomHTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail=f"{entity} not found"
)

BAD_REQUEST_EXCEPTION = lambda message: CustomHTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail=message
)

INTERNAL_SERVER_EXCEPTION = CustomHTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
)
