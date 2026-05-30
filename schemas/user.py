from core.security import hash_password
from pydantic import BaseModel,EmailStr,Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email:EmailStr
    password:str
    