import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import ExpiredSignatureError


from app.repositories.user_repository import UserRepository
from app.models.models import User

JWT_SECRET = 'SECRET'
ALGORITHM = 'HS256'


oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def create_token(data: dict, expire_delta=None):
    payload = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)

    payload.update({'exp': expire})
    return jwt.encode(payload, JWT_SECRET, ALGORITHM)


def authenticate(form_data: OAuth2PasswordRequestForm = Depends(), user_repository: UserRepository = Depends()):
    user = user_repository.find_by_email(form_data.username)
    if not user:
        return False
    if not bcrypt.checkpw(form_data.password.encode('utf8'), user.password):
        return False
    return create_token({'id': user.id})


def get_user(token: str = Depends(oauth_scheme), user_repository: UserRepository = Depends()):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=ALGORITHM)
        user = user_repository.get_by_id(payload['id'])
        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='This token has expired.')


def only_admin(user: User = Depends(get_user)):
    if not user.role == 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Allowed only for admin.')
