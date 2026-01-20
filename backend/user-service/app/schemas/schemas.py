from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date
from uuid import UUID

# Request schema (input)
class UserBase(BaseModel):
    fname:str
    lname:str
    email: EmailStr
    dob:date
    phone:str
    password:str
    isAdmin:bool

class UserCreate(BaseModel):
    email:str
    password:str
    
# Response schema (output)
class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    fname:str
    lname:str
    dob:date
    phone:str
    isAdmin:bool
    is_active: bool
    class Config:
        from_attributes = True

class UserAuthResponse(BaseModel):
    id: UUID
    email: EmailStr
    fname:str
    lname:str
    dob:date
    phone:str
    is_active: bool
    access_token: str
    token_type: str = "bearer"
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    fname: Optional[str] = None
    lname: Optional[str] = None
    dob: Optional[date] = None
    
class UserUpdateAdmin(BaseModel):
    id:UUID #must for identification
    email:Optional[EmailStr]=None
    phone: Optional[str]=None
    isAdmin:Optional[bool]=None
    password:Optional[str]=None