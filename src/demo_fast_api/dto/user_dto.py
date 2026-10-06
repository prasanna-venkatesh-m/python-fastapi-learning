from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime

class CreateUserRequest(BaseModel):
    id: UUID
    name: str
    email: str
    password : str
    role : str
    createdBy : str


class UpdateUserRequest(BaseModel):
    id: UUID
    name: str
    email: str
    role : str


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role : str
    createdOn : datetime| None = None
    modifiedOn : datetime | None = None
    createdBy : str| None = None
    modifiedBy: str | None = None
    isActive : bool