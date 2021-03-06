from fastapi import APIRouter, Depends
from app.models.models import User
from app.api.user.schemas import UserSchema
from app.repositories.user_repository import UserRepository
import bcrypt

router = APIRouter()


@router.post('/')
def create(user: UserSchema, repository: UserRepository = Depends()):
    user.password = bcrypt.hashpw(
        user.password.encode('utf8'), bcrypt.gensalt())
    repository.create(User(**user.dict()))
