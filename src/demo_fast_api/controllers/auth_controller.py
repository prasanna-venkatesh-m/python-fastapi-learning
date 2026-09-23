from fastapi import APIRouter, Depends
from demo_fast_api.services.auth_service import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.get('/getaccesstoken')
def get_access_token(username: str, password: str, authService : AuthService = Depends(AuthService)):
    return authService.get_access_token(username, password)