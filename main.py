from fastapi import FastAPI, HTTPException, Depends, status
from datetime import date
from pydantic import BaseModel
from typing import Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
import database_models
import schemas

#START UP COMMAND =>  py -m uvicorn main:app --reload
#db confg
database_url="postgresql+psycopg2://postgres:vivek@localhost:5432/guapflow"
engine= create_engine(database_url)
SessionLocal =sessionmaker(autoflush=False, autocommit=False,bind=engine)
database_models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Simple Banking API",
    description="A basic API for banking operations",
    version="0.1.0",
)

@app.get('/isDBconnected')
def isDBconnected():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/createCustomer', status_code=status.HTTP_201_CREATED)
def create_user(customer_data: schemas.CustomerCreate, db: Session = Depends(isDBconnected)):
    db_customer = db.query(database_models.Customer).filter(database_models.Customer.email == customer_data.email).first()
    if db_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    new_customer = database_models.Customer(**customer_data.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)  # Get the new ID from the DB
    return {"status": "success", "customer_id": new_customer.id, "data": customer_data}

@app.post("/createAccount")
def createAccount(account_data:schemas.AccountCreate,db: Session=Depends(isDBconnected)):
    db_account=db.query(database_models.Account).filter(database_models.Account.phone==account_data.phone).first()
    if db_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account already exist"
        )
    new_account=database_models.Account(**account_data.model_dump())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return {"status":"success","account_id":new_account.accNo,"data":account_data} #id=accNo

@app.post("/createLoan")
def createLoan(loan_data:schemas.LoanCreate,db:Session=Depends(isDBconnected)):
    db_loan=db.query(database_models.Loan).filter(database_models.Loan.accNo==loan_data.accNo).first()
    if db_loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan already assigned to the account no"
        )
    new_loan=database_models.Loan(**loan_data.model_dump())
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return {"status":"success","loanId":new_loan.loanId,"data":new_loan}

@app.post("/createBank")
def createBank(bank_data:schemas.BankCreate,db:Session=Depends(isDBconnected)):
    bank_db=db.query(database_models.Bank).filter(database_models.Bank.bankID==bank_data.bankID).first()
    if bank_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Bank Already exist"
        )
    new_bank=database_models.Bank(**bank_data.model_dump())
    db.add(new_bank)
    db.commit()
    db.refresh(new_bank)
    return {
        "status":"success",
        "bank_id":new_bank.bankID,
        "data":new_bank
    }

@app.post('/createBranch')
def createBranch(branch_data:schemas.BranchCreate,db:Session=Depends(isDBconnected)):
    db_branch=db.query(database_models.Branch).filter(database_models.Branch.branchId==branch_data.branchId).first()
    if db_branch:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details='Specified branch already exist.'
        )
    new_branch=database_models.Branch(**branch_data.model_dump())
    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)
    return {
        "status":"success",
        "branchId":new_branch.branchId,
        "data":new_branch
    }

@app.post('/createTransaction')
def createTransaction(trans_data:schemas.TransactionCreate,db:Session=Depends(isDBconnected)):
    db_trans=db.query(database_models.Transaction).filter(database_models.Transaction.id==trans_data.id).first()
    if db_trans:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details='Transaction already exist'
        )
    new_trans=database_models.Transaction(**trans_data.model_dump())
    db.add(new_trans)
    db.commit()
    db.refresh(new_trans)
    return {
        "status":"success",
        "transactionId":new_trans.id,
        "data":new_trans
    }

@app.get("/")
def read_root():
    """Welcome endpoint"""
    return {"message": "Welcome to the Simple Banking API"}


#--------------------------------------ALL UPDATION FUNCTIONS GO HERE--------------------------------------------------
@app.put('/updateCustomer/{customer_id}')
def update_customer(customer_id: int, customer_update: schemas.CustomerUpdate, db: Session = Depends(isDBconnected)):
    db_customer = db.query(database_models.Customer).filter(
        database_models.Customer.id == customer_id
    ).first()
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Customer not found"
        )
    update_data = customer_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return {
        "status":"success",
        "data":db_customer
    }
@app.put("/updateAccount/{accNo}")
def updateAccount(accNo:int,new_acc:schemas.AccountUpdate,db: Session=Depends(isDBconnected)):
    db_acc=db.query(database_models.Account).filter(database_models.Account.accNo==accNo).first()
    if db_acc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The specified account not found'
        )
    update_acc=new_acc.model_dump(exclude_unset=True)
    for key,value in update_acc.items():
        setattr(db_acc,key,value)
    db.commit()
    db.refresh(db_acc)
    return {
        "status":"success",
        "data":db_acc
    }

@app.put('/updateLoan/{loanId}')
def updateLoan(loanId:int,new_loan:schemas.LoanUpdate,db:Session=Depends(isDBconnected)):
    db_loan=db.query(database_models.Loan).filter(database_models.Loan.loanId==loanId).first()
    if db_loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The specified Loan not found'
        )
    update_loan=new_loan.model_dump(exclude_unset=True)
    for key, value in update_loan.items():
        setattr(db_loan,key,value)
    db.commit()
    db.refresh(db_loan)
    return {
        "status":"success",
        "data":db_loan
    }
@app.put('/updateBranch/{branchId}')
def updateBranch(branchId:int,new_branch:schemas.BranchUpdate,db:Session=Depends(isDBconnected)):
    db_branch=db.query(database_models.Branch).filter(database_models.Branch.branchId==branchId).first()
    if db_branch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Specified Loan does not exist'
        )
    update_branch=new_branch.model_dump(exclude_unset=True)
    for key,value in update_branch.items():
        setattr(db_branch,key,value)
    db.commit()
    db.refresh(db_branch)
    return {
        "status":"success",
        "data":db_branch
    }

@app.put('/updateTransaction/{id}')
def updateTransaction(id:str,new_tran:schemas.TransactionUpdate,db:Session=Depends(isDBconnected)):
    db_transaction=db.query(database_models.Transaction).filter(database_models.Transaction.id==id).first()
    if db_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Transaction Not Found'
        )
    update_trans=new_tran.model_dump(exclude_unset=True)
    for key,value in update_trans.items():
        setattr(db_transaction,key,value)
    db.commit()
    db.refresh(db_transaction)
    return {
        "status":"success",
        "data":db_transaction
    }