from fastapi import APIRouter, HTTPException, Request

from backend.config.routers import RouterName
from backend.crud import user as user_crud
from backend.database_models import User as UserModel
from backend.database_models.database import DBSessionDep
from backend.schemas.user import CreateUser, DeleteUser, UpdateUser, User
from backend.schemas.user import User as UserSchema

router = APIRouter(prefix="/v1/users")
router.name = RouterName.USER  # type: ignore


@router.post("", response_model=UserSchema)
async def create_user(
    user: CreateUser,
    session: DBSessionDep,
) -> UserModel:
    """
    Create a new user.

    Args:
        user (CreateUser): User data to be created.
        session (DBSessionDep): Database session.

    Returns:
        User: Created user.
    """
    db_user = UserModel(**user.model_dump(exclude_none=True))
    db_user = user_crud.create_user(session, db_user)

    return db_user


@router.get("", response_model=list[User])
async def list_users(
    *,
    offset: int = 0,
    limit: int = 100,
    session: DBSessionDep,
) -> list[UserModel]:
    """
    List all users.

    Args:
        offset (int): Offset to start the list.
        limit (int): Limit of users to be listed.
        session (DBSessionDep): Database session.
          (Context): Context object.

    Returns:
        list[User]: List of users.
    """
    return user_crud.get_users(session, offset=offset, limit=limit)


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    session: DBSessionDep,
) -> UserModel:
    """
    Get a user by ID.

    Args:
        user_id (str): User ID.
        session (DBSessionDep): Database session.
          (Context): Context object.

    Returns:
        User: User with the given ID.

    Raises:
        HTTPException: If the user with the given ID is not found.
    """

    user = user_crud.get_user(session, user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with ID: {user_id} not found."
        )

    UserSchema.model_validate(user)
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    new_user: UpdateUser,
    session: DBSessionDep,
    request: Request,
) -> UserModel:
    """
    Update a user by ID.

    Args:
        user_id (str): User ID.
        new_user (UpdateUser): New user data.
        session (DBSessionDep): Database session.
        request (Request): Request object.
          (Context): Context object

    Returns:
        User: Updated user.

    Raises:
        HTTPException: If the user with the given ID is not found.
    """
    user = user_crud.get_user(session, user_id)

    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with ID: {user_id} not found."
        )

    user = user_crud.update_user(session, user, new_user)
    UserSchema.model_validate(user)

    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    session: DBSessionDep,
) -> DeleteUser:
    """ "
    Delete a user by ID.

    Args:
        user_id (str): User ID.
        session (DBSessionDep): Database session.
          (Context): Context object.

    Returns:
        DeleteUser: Empty response.

    Raises:
        HTTPException: If the user with the given ID is not found.
    """
    user = user_crud.get_user(session, user_id)

    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with ID: {user_id} not found."
        )

    UserSchema.model_validate(user)
    user_crud.delete_user(session, user_id)

    return DeleteUser()
