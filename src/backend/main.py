from alembic.command import upgrade
from alembic.config import Config
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from backend.config.auth import (
    get_auth_strategy_endpoints,
    is_authentication_enabled,
    verify_migrate_token,
)
from backend.config.routers import ROUTER_DEPENDENCIES
from backend.config.settings import Settings
from backend.routers.auth import router as auth_router
from backend.routers.chat import router as chat_router
from backend.routers.conversation import router as conversation_router
from backend.routers.study import router as study_router
from backend.routers.user import router as user_router

load_dotenv()

# CORS Origins
ORIGINS = ["*"]


def create_app():
    app = FastAPI()

    routers = [
        auth_router,
        chat_router,
        user_router,
        conversation_router,
        study_router,
    ]

    # Dynamically set router dependencies
    # These values must be set in config/routers.py
    dependencies_type = "default"
    if is_authentication_enabled():
        # Required to save temporary OAuth state in session
        auth_secret = Settings().auth.secret_key
        assert auth_secret, "Auth secret key must be set in .env"
        app.add_middleware(SessionMiddleware, secret_key=auth_secret)
        dependencies_type = "auth"
    for router in routers:
        if getattr(router, "name", "") in ROUTER_DEPENDENCIES.keys():
            router_name = router.name
            dependencies = ROUTER_DEPENDENCIES[router_name][dependencies_type]
            app.include_router(router, dependencies=dependencies)
        else:
            app.include_router(router)

    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": (
                f"Failed method {request.method} at URL {request.url}."
                f" Exception message is {exc!r}."
            )
        },
    )


@app.on_event("startup")
async def startup_event():
    """
    Retrieves all the Auth provider endpoints if authentication is enabled.
    """
    if is_authentication_enabled():
        await get_auth_strategy_endpoints()


@app.get("/health")
async def health():
    """
    Health check for backend APIs
    """
    return {"status": "OK"}


@app.post("/migrate", dependencies=[Depends(verify_migrate_token)])
async def apply_migrations():
    """
    Applies Alembic migrations - useful for serverless applications
    """
    try:
        alembic_cfg = Config("src/backend/alembic.ini")
        upgrade(alembic_cfg, "head")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error while applying Alembic migrations: {str(e)}"
        )

    return {"status": "Migration successful"}
