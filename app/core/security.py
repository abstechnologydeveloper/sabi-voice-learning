from fastapi import Header, HTTPException, status

from app.core.config import get_settings


def require_api_key(authorization: str | None = Header(default=None)) -> None:
    settings = get_settings()
    allowed = settings.allowed_api_keys

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sabi Voice API keys are not configured.",
        )

    prefix = "Bearer "
    token = ""
    if authorization and authorization.startswith(prefix):
        token = authorization[len(prefix) :].strip()
    if token not in allowed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Sabi Voice API key.",
        )
