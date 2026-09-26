from demo_fast_api.utils.jwt_helper import create_access_token
from fastapi import HTTPException

class AuthService:

    def get_access_token(self, username: str, password: str)-> str | None:
        if username=='1' and password=='1':
            return create_access_token(userId=username, role='ADMIN', userName='Admin User', department='IT', email='itadmin@gmail.com')
        elif username=='2' and password=='2':
            return create_access_token(userId=username, role='USER', userName='Normal User', department='IT', email='ituser@gmail.com')

        raise HTTPException(401, "Invalid Credentials")