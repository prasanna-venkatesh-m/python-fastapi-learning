from demo_fast_api.models.user_model import User


class UserRepository:

    def __init__(self):
        self.users: list[User] = []

    def get_all_users(self) -> list[User]:
        return self.users

    def get_user_by_id(self, user_id: int) -> User | None:
        for user in self.users:
            if user.id == user_id:
                return user

        return None

    def create_user(self, user: User) -> User:
        self.users.append(user)
        return user

    def update_user(
        self,
        user_id: int,
        update_user: User,
    ) -> User | None:

        existing_user = self.get_user_by_id(user_id)

        if existing_user is None:
            return None

        existing_user.name = update_user.name
        existing_user.email = update_user.email

        return existing_user

    def delete_user(self, user_id: int) -> bool:

        existing_user = self.get_user_by_id(user_id)

        if existing_user is None:
            return False

        self.users.remove(existing_user)

        return True