

from pydantic import BaseModel
from datetime import date, time,datetime
from typing import List,Optional

class CustomerCreate(BaseModel):
    fname: str
    lname: str
    phone: str
    email: str
    address: str
    aadharNo: str
    dob: date
    nomeneeId: str
    joiningyear: date

class CustomerUpdate(BaseModel):
    fname: Optional[str] = None
    lname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    aadharNo: Optional[str] = None
    dob: Optional[date] = None
    joiningyear: Optional[date] = None
    nomeneeId: Optional[str] = None

class AccountCreate(BaseModel):
      accNo:int
      name:str
      type:str
      kycNo:str
      phone:int
      balance:float
      outStBalance:float
      otherExpense:float
      branchId:int

class AccountUpdate(BaseModel):
      accNo:Optional[int]=None
      name:Optional[str] = None
      type:Optional[str] = None
      kycNo:Optional[str] = None
      phone:Optional[int] = None
      balance:Optional[float] = None
      outStBalance:Optional[float] = None
      otherExpense:Optional[float] = None
      branchId:int

class LoanCreate(BaseModel):
    loanId:int
    accNo:int
    type:str
    amount:float
    roi:float
    repaymentDate:date
    issueDate:date
    gracePeriod:date
    collateralList:List[str]

class LoanUpdate(BaseModel):
    loanId:Optional[int] = None
    accNo:Optional[int] = None
    type:Optional[str] = None
    amount:Optional[float] = None
    roi:Optional[float] = None
    repaymentDate:Optional[date] = None
    issueDate:Optional[date] = None
    gracePeriod:Optional[date] = None
    collateralList:Optional[List[str]] = None

class BankCreate(BaseModel):
     bankID:int
     branches:List[str]

class BranchCreate(BaseModel):
    branchId:int #pk
    name:str
    address:str
    ifscCode:str
    branchType:str

class BranchUpdate(BaseModel):
     branchId:Optional[int]=None
     name:Optional[str]=None
     ifsccode:Optional[str]=None
     branchType:Optional[str]=None
     
class TransactionCreate(BaseModel):
     id:str #pk
     senderId:int
     receiver:int
     timestamp:datetime
     isSuccess:bool
     onRevert:bool
     amount:float
     
class TransactionUpdate(BaseModel):
     id:Optional[str]=None
     senderId:Optional[int]=None
     receiver:Optional[int]=None
     timestamp:Optional[datetime]=None
     isSuccess:Optional[bool]=None
     onRevert:Optional[bool]=None
     amount:Optional[float]=None

# --- NEW SCHEMAS FOR AUTHENTICATION ---
# (This is the part that was missing and causing the error)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_admin: Optional[bool] = False

class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        from_attributes = True # Allows Pydantic to read from SQLAlchemy objects

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None