from fastapi import APIRouter, Depends
from demo_fast_api.services.auth_service import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.get('/getaccesstoken')
async def get_access_token(email: str, password: str, authService : AuthService = Depends(AuthService)):
    return await authService.get_access_token(email, password)