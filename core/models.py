from pydantic import BaseModel, Field, EmailStr
from typing import Literal

class BaseResponse(BaseModel):
    message: str = Field(default=None)
    data: dict = Field(default=None)

class ContainerNetworks(BaseModel):
    props:dict

class ContainerTemplate(BaseModel):
    dist: str
    release: str
    arch: str

class Container(BaseModel):
    name:str
    template:ContainerTemplate
    networks:ContainerNetworks

class CreateContainer(BaseModel):
    name:str = Field(default=None)
    template:ContainerTemplate = Field(default=None)

class UserType(BaseModel):
    type:Literal["admin","user"] = Field(default="user")

class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_type: UserType

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserRegister(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    name: str = Field(max_length=40)
    user_type: UserType 

class UserUpdate(UserBase):
    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)
