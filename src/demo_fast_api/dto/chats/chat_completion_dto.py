from pydantic import BaseModel
from uuid import UUID

class ChatCompletionDto(BaseModel):
    chat_id : UUID | None = None
    user_query : str 