import jwt
from datetime import timezone, timedelta, datetime
import os
from dotenv import load_dotenv
load_dotenv()

def create_access_token(userId: str, role: str, userName: str, department: str, email: str):
    payload = {
        "userId": userId,
        "userName": userName,
        "role": role,
        "department": department,
        "email": email,
        "exp": datetime.now(timezone.utc)+timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRY_IN_MINUTES")))
    }

    return jwt.encode(payload=payload,key=os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
