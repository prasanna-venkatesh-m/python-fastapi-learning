from fastapi import APIRouter
from demo_fast_api.services.auth_service import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

authService = AuthService()

@router.get('/getaccesstoken')
def get_access_token(username: str, password: str):
    return authService.get_access_token(username, password)