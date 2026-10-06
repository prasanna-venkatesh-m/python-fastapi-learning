from demo_fast_api.repository.user_repository import UserRepository
from demo_fast_api.dto.user_dto import CreateUserRequest, UpdateUserRequest, UserResponse
from demo_fast_api.models.user_model import User
import uuid
from datetime import datetime, timezone
from uuid import UUID

class UserService:
    def __init__(self):
        self.userRepository = UserRepository()

    async def get_users(self) -> list[UserResponse]:
        users =await self.userRepository.get_all_users()
        return [
            UserResponse(
                id = user.id,
                name = user.name,
                email = user.email,
                role = user.role,
                isActive= user.isActive
            )
            for user in users
        ]
    
    async def get_user_by_id(self, userId : UUID) -> UserResponse | None:
        user = await self.userRepository.get_user_by_id(userId)

        if user is None:
            return None

        return UserResponse(
            id = user.id,
            name = user.name,
            email = user.email,
            role = user.role,
            isActive= user.isActive
        )

    async def create_user(self, userData : CreateUserRequest) -> UserResponse | None:
        user = User(
            id = uuid.uuid4(),
            name = userData.name,
            email= userData.email,
            password=userData.password,
            role=userData.role,
            createdBy=userData.createdBy,
            createdOn= datetime.now(timezone.utc),
            isActive=True
        )

        created_user = await self.userRepository.create_user(user)
        return UserResponse(
            id = created_user.id,
            name = created_user.name,
            email = created_user.email,
            role = created_user.role,
            isActive= created_user.isActive
        )

    async def update_user(self, userId: UUID, update_data: UpdateUserRequest, updatedBy : str) -> UserResponse | None:
        user = UpdateUserRequest(
            id = userId,
            name = update_data.name,
            email = update_data.email,
            role = update_data.role
        )
        updated_user = await self.userRepository.update_user(userId, user, updatedBy)

        if updated_user is None:
            return None

        return UserResponse(
            id = updated_user.id,
            name = updated_user.name,
            email = updated_user.email,
            role = updated_user.role,
            isActive= updated_user.isActive
        ) 

    async def delete_user(self, userId: UUID) -> bool:
        return await self.userRepository.delete_user(userId)