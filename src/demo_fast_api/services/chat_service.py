from demo_fast_api.dto.chats.chat_completion_dto import ChatCompletionDto
from demo_fast_api.dto.chats.chat_response_dto import ChatResponseDto
from uuid import UUID
from demo_fast_api.services.file_service import FileService
from demo_fast_api.llms.llm_client import LLMClient


class ChatService:
    def __init__(self):
        self.file_service = FileService()
        self.llm_client = LLMClient()

    async def chat_completion(self, query: ChatCompletionDto, userData : dict, reqId : UUID) -> ChatResponseDto:
        chunks = await self.file_service.search_vectors(query.user_query)
        context = "\n\n".join(
            chunk["metadata"]["text"]
            for chunk in chunks
        )
        system_prompt = """
        You are a helpful assistant.

        Answer the user's question using the provided context.
        If the answer cannot be found in the context,
        say that you don't have enough information.
        """

        response = await self.llm_client.generate(
            model = "openai/gpt-oss-120b",
            system_prompt=system_prompt,
            user_query=query.user_query,
            context=context,
            histories=[]
        )

        return ChatResponseDto(
            chat_id=query.chat_id,
            chat_response=response.choices[0].message.content,
            attachments=["test"],
            sources=["vector"]
        )