from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str
