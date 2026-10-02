from fastapi import APIRouter, Depends
from demo_fast_api.dto.chats.chat_completion_dto import ChatCompletionDto
from demo_fast_api.dto.chats.chat_response_dto import ChatResponseDto
from demo_fast_api.utils.dependencies import authenticate, authorize
from demo_fast_api.services.chat_service import ChatService

router = APIRouter(
    prefix='/chat',
    tags=['Chat'],
    dependencies=[Depends(authenticate)]
)

@router.post(path='/chat-completion', response_model=ChatResponseDto)
async def get_chat_completion(
    query : ChatCompletionDto,
    chat_service : ChatService = Depends(ChatService),
    userData : dict = Depends(authenticate)):
    return await chat_service.chat_completion(query, userData)