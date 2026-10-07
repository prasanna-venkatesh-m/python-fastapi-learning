from pydantic import BaseModel, Field
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Any

class ChatMessage(BaseModel):
    chat_id : UUID
    request_id: UUID = Field(default_factory=uuid4)
    role : str
    content : str
    context : Any | None = None
    is_output_generated : bool = False
    createdBy : str
    createdOn : datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updatedOn : datetime | None = None
    isActive : bool = True