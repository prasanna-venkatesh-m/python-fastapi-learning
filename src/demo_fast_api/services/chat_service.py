from demo_fast_api.dto.chats.chat_completion_dto import ChatCompletionDto
from demo_fast_api.dto.chats.chat_response_dto import ChatResponseDto
from uuid import UUID
from demo_fast_api.services.file_service import FileService


class ChatService:
    def __init__(self):
        self.file_service = FileService()

    async def chat_completion(self, query: ChatCompletionDto, userData : dict, reqId : UUID) -> ChatResponseDto:
        chunks = await self.file_service.search_vectors(query.user_query)
        return ChatResponseDto(
            chat_id=query.chat_id,
            chat_response="Good to go",
            attachments=["test"],
            sources=["vector"]
        )