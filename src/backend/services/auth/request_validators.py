import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from starlette import status

from backend.database_models import Blacklist, get_session
from backend.services.auth.jwt import JWTService


def validate_authorization(
    request: Request, session: Session = Depends(get_session)
) -> dict:
    """
    Validate that the request has the `Authorization` header, used for requests
    that require authentication.

    Args:
        request (Request): The request to validate

    Raises:
        HTTPException: If no `Authorization` header.

    Returns:
        dict: Decoded payload.
    """

    authorization = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization: Bearer <token> required in request headers.",
        )

    try:
        scheme, token = authorization.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Authorization: Bearer <token> required in request headers.",
        )

    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Authorization: Bearer <token> required in request headers.",
        )

    decoded = JWTService().decode_jwt(token)

    if not decoded or "context" not in decoded:
        raise HTTPException(
            status_code=401, detail="Bearer token is invalid or expired."
        )

    blacklist = (
        session.query(Blacklist).filter(Blacklist.token_id == decoded["jti"]).first()
    )

    # Token was blacklisted
    if blacklist is not None:
        raise HTTPException(status_code=401, detail="Bearer token is blacklisted.")

    return decoded


class BasicAuthValidation:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __call__(
        self,
        credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())],
    ) -> None:
        if not self.username or not self.password:
            raise HTTPException(
                status_code=500,
                detail="username or password is not configured",
                headers={"WWW-Authenticate": "Basic"},
            )
        is_correct_username = self._compare_secret(credentials.username, self.username)
        is_correct_password = self._compare_secret(credentials.password, self.password)

        if not (is_correct_username and is_correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )

    def _compare_secret(self, actual: str, expected: str) -> bool:
        return secrets.compare_digest(actual.encode("utf8"), expected.encode("utf8"))
