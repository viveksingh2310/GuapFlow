from sqlalchemy import Column, Integer,Date,DateTime,Float,String,BigInteger, Boolean
from sqlalchemy.types import ARRAY
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Customer(Base):
    __tablename__="Customer"
    id=Column(Integer, primary_key=True, autoincrement=True)
    fname=Column(String)
    lname=Column(String)
    phone=Column(String) #common bw account table 
    email=Column(String)
    address=Column(String)
    aadharNo=Column(String)
    dob=Column(Date)
    joiningyear=Column(Date)
    nomeneeId=Column(String)

class Account(Base):
    __tablename__="Account"
    accNo=Column(BigInteger,primary_key=True)
    name=Column(String) #cust name
    type=Column(String)
    kycNo=Column(String) #no dependency
    phone=Column(BigInteger) #common bw customer table 
    balance=Column(Float)
    outStBalance=Column(Float)
    otherExpense=Column(Float)

class Loan(Base):
    __tablename__="Loan"
    loanId=Column(BigInteger,primary_key=True) #max 7 digits
    accNo=Column(BigInteger) #mapped
    type=Column(String)
    amount=Column(Float)
    roi=Column(Float)
    repaymentDate=Column(Date)
    issueDate=Column(Date)
    gracePeriod=Column(Date)
    collateralList=Column(ARRAY(String))

class Bank(Base):
    __tablename__="Bank"
    bankID=Column(BigInteger, primary_key=True)
    branches=Column(ARRAY(String))

class Branch(Base):
    __tablename__="Branch"
    branchId=Column(BigInteger,primary_key=True) #or branch code
    name=Column(String) #name of the branch
    address=Column(String)
    ifscCode=Column(String)
    branchType=Column(String)

class Transaction(Base):
    __tablename__="Transaction"
    id=Column(String,primary_key=True)
    senderId=Column(BigInteger) # acc no
    receiver=Column(BigInteger) #acc no
    timestamp=Column(DateTime)
    isSuccess=Column(Boolean)
    onRevert=Column(Boolean)
    amount=Column(Float)