from pydantic import BaseModel
from datetime import datetime, timezone
from uuid import UUID

class ChatMessage(BaseModel):
    id : UUID
    chat_id : UUID
    request_id : UUID
    role : str
    content : str
    is_output_generated : bool
    createdBy : str
    createdOn : datetime = datetime.now(timezone.utc)
    updatedOn : datetime | None = None
    isActive : bool = True