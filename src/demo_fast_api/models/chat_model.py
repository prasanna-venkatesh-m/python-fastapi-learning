from datetime import datetime, timezone
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class Chat(BaseModel):
    chat_id: UUID = Field(default_factory=uuid4)
    summary: str
    createdBy: str
    createdOn: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updatedOn: datetime | None = None
    isActive: bool = True
