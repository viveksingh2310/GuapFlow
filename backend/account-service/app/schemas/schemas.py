from typing import Optional
from pydantic import BaseModel, EmailStr, Field,model_validator
from datetime import date
from uuid import UUID

class AccountBase(BaseModel):
    id:UUID
    user_id:UUID
    acc_no:str
    name:str 
    age:int   
    phone:str
    email:EmailStr
    dob:date
    pin:str #hashed
    amount: int = Field(default=0, ge=0)
    other_charges: int = Field(default=0, ge=0)
    opening_date: date = Field(default_factory=date.today)
    ifsc_code:str
    isDigital:bool=False
    pan_no:str
    aadhar_no:str
    type: str = "default"

class AccountCreate(BaseModel):
    acc_no:str
    name:str
    phone:str
    email:EmailStr
    dob:date
    pin:str
    age: Optional[int] = None
    amount:int
    ifsc_code:str
    isDigital:bool=False
    pan_no:str
    aadhar_no:str
    type:str="default" #if not given

    @model_validator(mode='after')
    def calculate_age_from_dob(self):
        if self.dob:
            today = date.today()
            calculated_age = today.year - self.dob.year - (
                (today.month, today.day) < (self.dob.month, self.dob.day)
            )
            self.age = calculated_age     
        return self
    
class AccountResponse(AccountBase):
    isActive:bool="True"
    
class AccountLogin(BaseModel):
    email:EmailStr
    pin:str

class AccNoResponse(BaseModel):
    user_id:UUID
    acc_no:str
    amount:int
class AccountTransactionDetail(BaseModel):
    sender_acc:str
    receiver_acc:str
    amount:int

class UpdateAccountByUser(BaseModel):
    name:Optional[str]=None    
    phone:Optional[str]=None   
    email:Optional[EmailStr]=None
    dob:Optional[date]=None
    pin:Optional[str]=None  #verification needed while updation
    isDigital:Optional[bool]=False
    pan_no:Optional[str]=None
    aadhar_no:Optional[str]=None
    @model_validator(mode='after')
    def calculate_age_from_dob(self):
        if self.dob:
            today = date.today()
            calculated_age = today.year - self.dob.year - (
                (today.month, today.day) < (self.dob.month, self.dob.day)
            )
            self.age = calculated_age     
        return self
    
class UpdateAccountByAdmin(BaseModel):
    acc_no:Optional[str]=None
    amount: Optional[int]=None
    other_charges: Optional[int]=None
    opening_date:Optional[date]=None
    ifsc_code:Optional[str]=None
    type: Optional[str]=None

class CurrentUser(BaseModel):
    user_id: UUID
    role: str