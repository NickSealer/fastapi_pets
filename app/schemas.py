from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
  username: str
  email: EmailStr
  birthdate: Optional[date] = None

class CreateUser(UserBase):
  password: str
  
class UserResponse(UserBase):
  id: int
  class Config:
    from_attributes = True