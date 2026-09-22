from fastapi import APIRouter, status, Depends
from demo_fast_api.dto.user_dto import (CreateUserRequest,UpdateUserRequest,UserResponse)
from demo_fast_api.services.user_service import UserService
from demo_fast_api.utils.dependencies import authenticate, authorize

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(authenticate)]
)

user_service = UserService()

@router.get("/",response_model=list[UserResponse])
def get_users():
    return user_service.get_users()

@router.get("/{user_id}",response_model=UserResponse | None, dependencies=[Depends(authorize(["ADMIN"]))])
def get_user(user_id: int):
    return user_service.get_user_by_id(user_id)

@router.get("/profile", status_code=status.HTTP_201_CREATED)
def get_my_profile(payload : dict = Depends(authenticate)):
    return user_service.get_user_by_id(payload.get("userId"))

@router.post("/",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUserRequest):
    return user_service.create_user(user)


@router.put("/{user_id}",response_model=UserResponse,)
def update_user(user_id: int,user: UpdateUserRequest):
    return user_service.update_user(user_id, user)


@router.delete("/{user_id}",status_code=status.HTTP_200_OK, dependencies=[Depends(authorize(["ADMIN"]))])
def delete_user(user_id: int):
    return user_service.delete_user(user_id)