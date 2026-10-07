from demo_fast_api.dto.chats.chat_completion_dto import ChatCompletionDto
from demo_fast_api.dto.chats.chat_response_dto import ChatResponseDto
from uuid import UUID
from demo_fast_api.services.file_service import FileService
from demo_fast_api.llms.llm_client import LLMClient
from demo_fast_api.services.prompt_service import PromptService
from demo_fast_api.repository.chat_repository import ChatRepository
from demo_fast_api.models.chat_model import Chat
from dotenv import load_dotenv
import os

load_dotenv()

class ChatService:
    def __init__(self):
        self.file_service = FileService()
        self.llm_client = LLMClient()
        self.prompt_service = PromptService()
        self.chat_repo = ChatRepository()

    async def chat_completion(self, query: ChatCompletionDto, userData : dict, reqId : UUID) -> ChatResponseDto:
        chat_id = None
        if query.chat_id is None :
            chat : Chat = await self.chat_repo.create_chat(Chat(createdBy=userData["userId"], summary=query.user_query))
            chat_id = chat.chat_id

        chunks = await self.file_service.search_vectors(query.user_query) 
        context = "\n\n".join(
            chunk["metadata"]["text"]
            for chunk in chunks
        )
        system_prompt = self.prompt_service.get_chat_prompt(os.getenv("CHAT_PROMPT_VERSION"))

        response = await self.llm_client.generate(
            model = "openai/gpt-oss-120b",
            system_prompt=system_prompt,
            user_query=query.user_query,
            context=context,
            histories=[]
        )

        return ChatResponseDto(
            chat_id=chat_id,
            chat_response=response.choices[0].message.content
        )