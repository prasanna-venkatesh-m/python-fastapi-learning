from pydantic import BaseModel
from uuid import UUID

class ChatResponseDto(BaseModel):
    chat_id : UUID
    chat_response : str
    sources : list[str] | None = None
    attachments : list[str] | None = None