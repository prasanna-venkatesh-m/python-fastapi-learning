from demo_fast_api.dto.chats.chat_completion_dto import ChatCompletionDto
from demo_fast_api.dto.chats.chat_response_dto import ChatResponseDto
from uuid import UUID


class ChatService:
    def __init__(self):
        pass

    async def chat_completion(self, query: ChatCompletionDto, userData : dict, reqId : UUID) -> ChatResponseDto:
        return ChatResponseDto(
            chat_id=query.chat_id,
            chat_response="Good to go",
            attachments=["test"],
            sources=["vector"]
        )