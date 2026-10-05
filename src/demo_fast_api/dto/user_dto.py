from pydantic import BaseModel
from uuid import UUID

class CreateUserRequest(BaseModel):
    name: str
    email: str


class UpdateUserRequest(BaseModel):
    name: str | None = None
    email: str | None = None


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str