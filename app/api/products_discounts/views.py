from fastapi import APIRouter

router = APIRouter()


@router.post('/')
def create():
    ...


@router.get('/')
def index():
    ...


@router.put('/{id}')
def update(id: int):
    ...


@router.get('/{id}')
def show(id: int):
    ...
