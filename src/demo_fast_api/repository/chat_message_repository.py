from demo_fast_api.models.chat_message_model import ChatMessage
from demo_fast_api.database.mongodb import chat_message_collection

class ChatMessageRepository:
    async def create_chat_message(self, msg : ChatMessage) -> ChatMessage :
        return await chat_message_collection.insert_one(
            msg.model_dump()
        )