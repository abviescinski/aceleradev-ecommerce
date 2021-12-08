from pydantic import BaseModel


class AdminSchema(BaseModel):
    role: str = "admin"
    display_name: str
    email: str
    password: str

class ShowAdminSchema(AdminSchema):
    id: int

    class Config:
        orm_mode = True