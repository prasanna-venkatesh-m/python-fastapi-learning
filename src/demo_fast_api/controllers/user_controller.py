from fastapi import APIRouter, status

from demo_fast_api.dto.user_dto import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
)
from demo_fast_api.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

user_service = UserService()


@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_users():
    return user_service.get_users()


@router.get(
    "/{user_id}",
    response_model=UserResponse | None,
)
def get_user(user_id: int):
    return user_service.get_user_by_id(user_id)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: CreateUserRequest):
    return user_service.create_user(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    user: UpdateUserRequest,
):
    return user_service.update_user(user_id, user)


@router.delete("/{user_id}")
def delete_user(user_id: int):
    return user_service.delete_user(user_id)