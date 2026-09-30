import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer()
SECRET_KEY='my_seceret_key'
ALGORITHM='HS256'

def authenticate(authorization : HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = authorization.credentials
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
