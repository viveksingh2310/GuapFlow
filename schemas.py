from pydantic import BaseModel
from datetime import date, time,datetime
from typing import List

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

class AccountCreate(BaseModel):
      accNo:int
      name:str
      type:str
      kycNo:str
      phone:int
      balance:float
      outStBalance:float
      otherExpense:float

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

class BankCreate(BaseModel):
     bankID:int
     branches:List[str]

class BranchCreate(BaseModel):
    branchId:int #pk
    name:str
    address:str
    ifscCode:str
    branchType:str

class TransactionCreate(BaseModel):
     id:str #pk
     senderId:int
     receiver:int
     timestamp:datetime
     isSuccess:bool
     onRevert:bool
     amount:float