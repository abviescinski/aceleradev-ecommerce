from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.repositories.user_repository import UserRespository
from app.services.auth_service import create_token
import bcrypt

router = APIRouter()

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


@router.get('/')
def index(token: str = Depends(oauth_scheme)):
    return {'hello': True}


@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), user_repository: UserRespository = Depends()):
    user = user_repository.find_by_email(form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User not found with this username.')
    if not bcrypt.checkpw(form_data.password.encode('utf8'), user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='The password id invalid.')
    return {'access_token': create_token({'id': user.id}), 'token_type': 'bearer'}
