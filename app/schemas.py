from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
  username: str
  email: EmailStr
  birthdate: Optional[date] = None

class CreateUser(UserBase):
  password: str
  
class UpdateUser(UserBase):
  username: Optional[str] = None
  email: Optional[str] = None
  password: Optional[str] = None
  birthdate: Optional[date] = None
  
class UserResponse(UserBase):
  id: int
  class Config:
    from_attributes = True
    
class Token(BaseModel):
  access_token: str
  token_type: str
