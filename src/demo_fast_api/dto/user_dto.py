from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    email: str


class UpdateUserRequest(BaseModel):
    name: str | None = None
    email: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str