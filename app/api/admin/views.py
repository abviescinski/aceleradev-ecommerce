from typing import List
from fastapi import APIRouter, Depends, status
from app.api.admin.schemas import AdminSchema, ShowAdminSchema
from app.repositories.user_repository import UserRepository
from app.services.auth_service import only_admin
from app.services.user_service import UserService

router = APIRouter(dependencies=[Depends(only_admin)])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(admin_schema: AdminSchema, service: UserService = Depends()):
    service.create_admin(admin_schema)


@router.get('/', response_model=List[ShowAdminSchema])
def index(repository: UserRepository = Depends()):
    return repository.get_admins()


@router.put('/{id}')
def update(id: int, admin_schema: AdminSchema, service: UserService = Depends()):
    service.update_admin(id, admin_schema)


@router.get('/{id}', response_model=ShowAdminSchema)
def show(id: int, repository: UserRepository = Depends()):
    return repository.get_admin_by_id(id)


@router.delete('/{id}')
def delete(id: int, repository: UserRepository = Depends()):
    repository.delete_admin(id)
