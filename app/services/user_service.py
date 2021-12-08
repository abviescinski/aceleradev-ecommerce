
import bcrypt
from typing import Union
from fastapi import Depends, HTTPException, status

from app.api.user.schemas import UserSchema
from app.api.admin.schemas import AdminSchema
from app.db.db import get_db
from app.models.models import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository

    def create_admin(self, admin: Union[UserSchema, AdminSchema]):
        if self.user_repository.find_by_email(admin.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already on use.")
        admin.password = bcrypt.hashpw(
            admin.password.encode('utf8'), bcrypt.gensalt())
        self.user_repository.create(User(**admin.dict()))

    def update_admin(self, id: int, admin: Union[UserSchema, AdminSchema]):
        query = self.user_repository.find_by_email(admin.email)
        if query.id != id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already on use")
        admin.password = bcrypt.hashpw(
            admin.password.encode('utf8'), bcrypt.gensalt())
        self.user_repository.update(id, admin.dict())
