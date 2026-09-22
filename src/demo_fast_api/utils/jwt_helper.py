import jwt
from datetime import timezone, timedelta, datetime

SECRET_KEY='my_seceret_key'
ACCESS_TOKEN_EXPIRY_IN_MINUTES=5
ALGORITHM='HS256'

def create_access_token(userId: str, role: str, userName: str, department: str, email: str):
    payload = {
        "userId": userId,
        "userName": userName,
        "role": role,
        "department": department,
        "email": email,
        "exp": datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRY_IN_MINUTES)
    }

    return jwt.encode(payload=payload,key=SECRET_KEY, algorithm=ALGORITHM)
