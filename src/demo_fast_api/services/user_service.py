from demo_fast_api.repository.user_repository import UserRepository
from demo_fast_api.dto.user_dto import CreateUserRequest, UpdateUserRequest, UserResponse
from demo_fast_api.models.user_model import User

class UserService:
    def __init__(self):
        self.userRepository = UserRepository()

    def get_users(self) -> list[UserResponse]:
        users = self.userRepository.get_all_users()
        return [
            UserResponse(
                id = user.id,
                name = user.name,
                email = user.email
            )
            for user in users
        ]
    
    def get_user_by_id(self, userId : int) -> UserResponse | None:
        user = self.userRepository.get_user_by_id(userId)

        if user is None:
            return None

        return UserResponse(
            id = user.id,
            name = user.name,
            email = user.email
        )

    def create_user(self, userData : CreateUserRequest) -> UserResponse | None:
        all_users = self.userRepository.get_all_users()
        user = User(
            id = len(all_users)+1,
            name = userData.name,
            email= userData.email
        )

        created_user = self.userRepository.create_user(user)
        return UserResponse(
            id = created_user.id,
            name = created_user.name,
            email = created_user.email
        )

    def update_user(self, userId: int, update_data: UpdateUserRequest) -> UserResponse | None:
        user = User(
            id = 1,
            name = update_data.name,
            email= update_data.email
        )
        updated_user = self.userRepository.update_user(userId, user)

        if updated_user is None:
            return None

        return UserResponse(
            id = updated_user.id,
            name = updated_user.name,
            email = updated_user.email
        ) 

    def delete_user(self, userId: int) -> bool:
        return self.userRepository.delete_user(userId)