from demo_fast_api.database.mongodb import chat_collection
from demo_fast_api.models.chat_model import Chat


class ChatRepository:
    async def create_chat(self, chat: Chat) -> Chat:

        await chat_collection.insert_one(
            chat.model_dump()
        )

        return chat
