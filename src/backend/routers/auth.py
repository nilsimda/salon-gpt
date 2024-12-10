from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from backend.config.auth import ENABLED_AUTH_STRATEGY_MAPPING
from backend.config.routers import RouterName
from backend.crud import blacklist as blacklist_crud
from backend.database_models import Blacklist
from backend.database_models.database import DBSessionDep
from backend.schemas.auth import JWTResponse, ListAuthStrategy, Login, Logout
from backend.services.auth.jwt import JWTService
from backend.services.auth.request_validators import validate_authorization
from backend.services.auth.utils import (
    get_or_create_user,
    is_enabled_authentication_strategy,
)

router = APIRouter(prefix="/v1")
router.name = RouterName.AUTH


@router.get("/auth_strategies", response_model=list[ListAuthStrategy])
def get_strategies() -> list[ListAuthStrategy]:
    """
    Retrieves the currently enabled list of Authentication strategies.

    Args:
        ctx (Context): Context object.
    Returns:
        List[dict]: List of dictionaries containing the enabled auth strategy names.
    """
    strategies = []
    for strategy_name, strategy_instance in ENABLED_AUTH_STRATEGY_MAPPING.items():
        strategies.append(
            {
                "strategy": strategy_name,
                "client_id": (
                    strategy_instance.get_client_id()
                    if hasattr(strategy_instance, "get_client_id")
                    else None
                ),
                "authorization_endpoint": (
                    strategy_instance.get_authorization_endpoint()
                    if hasattr(strategy_instance, "get_authorization_endpoint")
                    else None
                ),
                "pkce_enabled": (
                    strategy_instance.get_pkce_enabled()
                    if hasattr(strategy_instance, "get_pkce_enabled")
                    else False
                ),
            }
        )

    return strategies


@router.post("/login", response_model=Union[JWTResponse, None])
async def login(login: Login, session: DBSessionDep):
    """
    Logs user in, performing basic email/password auth.
    Verifies their credentials, retrieves the user and returns a JWT token.

    Args:
        login (Login): Login payload.
        session (DBSessionDep): Database session.
        ctx (Context): Context object.

    Returns:
        dict: JWT token on Basic auth success

    Raises:
        HTTPException: If the strategy or payload are invalid, or if the login fails.
    """
    strategy_name = login.strategy
    payload = login.payload

    if not is_enabled_authentication_strategy(strategy_name):
        print(
            f"[Auth] Error logging in: Invalid authentication strategy {strategy_name}"
        )
        raise HTTPException(
            status_code=422, detail=f"Invalid Authentication strategy: {strategy_name}."
        )

    # Check that the payload required is given
    strategy = ENABLED_AUTH_STRATEGY_MAPPING[strategy_name]
    strategy_payload = strategy.get_required_payload()
    if not set(strategy_payload).issubset(payload.keys()):
        missing_keys = [key for key in strategy_payload if key not in payload.keys()]
        raise HTTPException(
            status_code=422,
            detail=f"Missing the following keys in the payload: {missing_keys}.",
        )

    user = strategy.login(session, payload)
    if not user:
        raise HTTPException(
            status_code=401,
            detail=f"Error performing {strategy_name} authentication with payload: {payload}.",
        )

    token = JWTService().create_and_encode_jwt(user)

    return {"token": token}


@router.post("/{strategy}/auth", response_model=JWTResponse)
async def authorize(
    strategy: str,
    request: Request,
    session: DBSessionDep,
    code: str = None,
):
    """
    Callback authorization endpoint used for OAuth providers after authenticating on the provider's login screen.

    Args:
        strategy (str): Current strategy name.
        request (Request): Current Request object.
        session (Session): DB session.
        code (str): OAuth code.
        ctx (Context): Context object.

    Returns:
        dict: Containing "token" key, on success.

    Raises:
        HTTPException: If authentication fails, or strategy is invalid.
    """

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Error calling /auth with invalid code query parameter.",
        )

    strategy_name = None
    for enabled_strategy_name in ENABLED_AUTH_STRATEGY_MAPPING.keys():
        if enabled_strategy_name.lower() == strategy.lower():
            strategy_name = enabled_strategy_name

    if not strategy_name:
        raise HTTPException(
            status_code=400,
            detail=f"Error calling /auth with invalid strategy name: {strategy_name}.",
        )

    if not is_enabled_authentication_strategy(strategy_name):
        raise HTTPException(
            status_code=404, detail=f"Invalid Authentication strategy: {strategy_name}."
        )

    strategy = ENABLED_AUTH_STRATEGY_MAPPING[strategy_name]

    try:
        userinfo = await strategy.authorize(request)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not fetch access token from provider, failed with error: {str(e)}",
        )

    if not userinfo:
        raise HTTPException(
            status_code=401, detail="Could not get user from auth token."
        )

    # Get or create user, then set session user
    user = get_or_create_user(session, userinfo)

    token = JWTService().create_and_encode_jwt(user)

    return {"token": token}


@router.get("/logout", response_model=Logout)
async def logout(
    request: Request,
    session: DBSessionDep,
    token: dict | None = Depends(validate_authorization),
):
    """
    Logs out the current user, adding the given JWT token to the blacklist.

    Args:
        request (Request): current Request object.
        session (DBSessionDep): Database session.
        token (dict): JWT token payload.
        ctx (Context): Context object.

    Returns:
        dict: Empty on success
    """
    if token is not None:
        db_blacklist = Blacklist(token_id=token["jti"])
        blacklist_crud.create_blacklist(session, db_blacklist)

    return {}
