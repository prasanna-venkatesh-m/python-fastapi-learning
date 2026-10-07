from demo_fast_api.repository.chat_message_repository import ChatMessageRepository
from demo_fast_api.models.chat_message_model import ChatMessage
from uuid import UUID

class ChatMessageService:
    def __init__(self):
        self.chat_msg_repo = ChatMessageRepository()

    async def create_user_message(self, chat_id : UUID, req_id : UUID, content : str, createdBy : str) -> ChatMessage:
        return await self.chat_msg_repo.create_chat_message(ChatMessage(
            chat_id=chat_id,
            request_id= req_id,
            role="user",
            content=content,
            createdBy=createdBy
        ))

    async def create_agent_message(self, chat_id : UUID, req_id : UUID, content : str,context: str, createdBy : str) -> ChatMessage:
        return await self.chat_msg_repo.create_chat_message(ChatMessage(
            chat_id=chat_id,
            request_id= req_id,
            role="assistant",
            content=content,
            context=context,
            is_output_generated=True,
            createdBy=createdBy
        ))

    async def get_chat_histories(self, chat_id : UUID) :
        msg_histories =  await self.chat_msg_repo.get_chat_histories(chat_id=chat_id)
        return [
            {
                "role" : history.role,
                "content" : history.content
            }
            for history in msg_histories
        ]