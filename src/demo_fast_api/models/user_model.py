from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime

class User(BaseModel):
    id: UUID
    name: str
    email: str
    password : str
    role : str
    createdOn : datetime
    modifiedOn : datetime | None = None
    createdBy : str
    modifiedBy: str | None = None
    isActive : bool
