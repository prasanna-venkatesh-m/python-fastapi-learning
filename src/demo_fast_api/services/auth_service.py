from demo_fast_api.utils.jwt_helper import create_access_token
from fastapi import HTTPException
from demo_fast_api.services.user_service import UserService

class AuthService:

    def __init__(self):
        self.user_service = UserService()

    async def get_access_token(self, email: str, password: str)-> str | None:
        user = await self.user_service.get_user_by_email(email)
        if user.email == email and password == user.password :
            return create_access_token(userId=str(user.id), role=user.role, userName=user.name, email=user.email)

        raise HTTPException(401, "Invalid Credentials")