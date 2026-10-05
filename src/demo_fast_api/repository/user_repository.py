from demo_fast_api.database.mongodb import users_collection
from demo_fast_api.models.user_model import User


class UserRepository:

    async def get_all_users(self) -> list[User]:

        users = []

        cursor = users_collection.find()

        async for document in cursor:
            document.pop("_id", None)
            users.append(User(**document))

        return users

    async def get_user_by_id(self, user_id: int) -> User | None:

        document = await users_collection.find_one(
            {"id": user_id}
        )

        if document is None:
            return None

        document.pop("_id", None)

        return User(**document)

    async def create_user(self, user: User) -> User:

        await users_collection.insert_one(
            user.model_dump()
        )

        return user

    async def update_user(
        self,
        user_id: int,
        update_user: User,
    ) -> User | None:

        result = await users_collection.update_one(
            {"id": user_id},
            {
                "$set": {
                    "name": update_user.name,
                    "email": update_user.email,
                }
            }
        )

        if result.matched_count == 0:
            return None

        return await self.get_user_by_id(user_id)

    async def delete_user(self, user_id: int) -> bool:

        result = await users_collection.delete_one(
            {"id": user_id}
        )

        return result.deleted_count > 0
