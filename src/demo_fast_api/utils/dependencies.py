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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token Expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

def authorize(allowed_roles : list[str]):
    def dependecy(payload : dict = Depends(authenticate)):
        if(payload.get("role") not in allowed_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return payload
    return dependecy