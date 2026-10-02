from pydantic import BaseModel
from uuid import UUID

class ChatCompletionDto(BaseModel):
    chat_id : UUID
    user_query : str 