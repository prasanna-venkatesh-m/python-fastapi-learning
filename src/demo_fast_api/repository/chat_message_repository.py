from demo_fast_api.models.chat_message_model import ChatMessage
from demo_fast_api.database.mongodb import chat_message_collection
from uuid import UUID
from demo_fast_api.models.chat_message_model import ChatMessage

class ChatMessageRepository:
    async def create_chat_message(self, msg : ChatMessage) -> ChatMessage :
        return await chat_message_collection.insert_one(
            msg.model_dump()
        )

    async def get_chat_histories(self, chat_id: UUID) -> list[ChatMessage]:
        chats_msgs = []

        cursor = chat_message_collection.find({
            "chat_id": chat_id
        })

        async for document in cursor:
            document.pop("_id", None)
            chats_msgs.append(ChatMessage(**document))

        return chats_msgs