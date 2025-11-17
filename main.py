from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import date
from pydantic import BaseModel
from typing import Dict, List
from sqlalchemy.orm import Session
# Import your new/updated modules
import database_models
import schemas
import auth
from database_models import engine, get_db # Import get_db

#START UP COMMAND =>  py -m uvicorn main:app --reload

# Create all tables
# This will create the new 'users' table
database_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Simple Banking API",
    description="A basic API for banking operations",
    version="0.1.0",
)

# --- AUTHENTICATION ENDPOINTS ---

@app.post("/register", response_model=schemas.UserDisplay, status_code=status.HTTP_201_CREATED)   #done
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(database_models.User).filter(database_models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    db_user_name = db.query(database_models.User).filter(database_models.User.username == user.username).first()
    if db_user_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )    
    # Hash the password
    hashed_password = auth.get_password_hash(user.password)
    # Create the user object
    new_user = database_models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=user.is_admin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@app.post("/login", response_model=schemas.Token)    #done
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(database_models.User).filter(database_models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.UserDisplay)
def read_users_me(
    current_user: database_models.User = Depends(auth.get_current_user)
):
    """
    Get details for the currently logged-in user.
    """
    return current_user


# --- HEALTH CHECK ENDPOINT ---

@app.get('/health')
def health_check(db: Session = Depends(get_db)):
    """
    Check if the database connection is successful.
    """
    try:
        # Try to execute a simple query
        db.execute("SELECT 1")
        return {"status": "success", "message": "Database connection is active."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {e}",
        )

# --- CREATE ENDPOINTS (FIXED) ---

@app.post('/createCustomer', response_model=schemas.CustomerCreate, status_code=status.HTTP_201_CREATED)
def create_customer(customer_data: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = db.query(database_models.Customer).filter(database_models.Customer.email == customer_data.email).first()
    if db_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    new_customer = database_models.Customer(**customer_data.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@app.post("/createAccount", status_code=status.HTTP_201_CREATED)
def createAccount(account_data:schemas.AccountCreate, db: Session=Depends(get_db)):
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
    return {"status":"success","account_id":new_account.accNo,"data":account_data}

@app.post("/createLoan", status_code=status.HTTP_201_CREATED)
def createLoan(loan_data:schemas.LoanCreate, db:Session=Depends(get_db)):
    db_loan=db.query(database_models.Loan).filter(database_models.Loan.accNo==loan_data.accNo).first()
    if db_loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't create as loan already assigned to the account no"
        )
    new_loan=database_models.Loan(**loan_data.model_dump())
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return {"status":"success","loanId":new_loan.loanId,"data":new_loan}

@app.post("/createBank", status_code=status.HTTP_201_CREATED)
def createBank(bank_data:schemas.BankCreate, db:Session=Depends(get_db)):
    bank_db=db.query(database_models.Bank).filter(database_models.Bank.bankID==bank_data.bankID).first()
    if bank_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bank Already exist" # 'detail' not 'details'
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

@app.post('/createBranch', status_code=status.HTTP_201_CREATED)
def createBranch(branch_data:schemas.BranchCreate, db:Session=Depends(get_db)):
    db_branch=db.query(database_models.Branch).filter(database_models.Branch.branchId==branch_data.branchId).first()
    if db_branch:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Specified branch already exist.' # 'detail' not 'details'
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

@app.post('/createTransaction', status_code=status.HTTP_201_CREATED)
def createTransaction(trans_data:schemas.TransactionCreate, db:Session=Depends(get_db)):
    db_trans=db.query(database_models.Transaction).filter(database_models.Transaction.id==trans_data.id).first()
    if db_trans:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Transaction already exist' # 'detail' not 'details'
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

# --- UPDATE ENDPOINTS (FIXED) ---

@app.put('/updateCustomer/{customer_id}')
def update_customer(customer_id: int, customer_update: schemas.CustomerUpdate, db: Session = Depends(get_db)):
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
def updateAccount(accNo:int, new_acc:schemas.AccountUpdate, db: Session=Depends(get_db)):
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
def updateLoan(loanId:int, new_loan:schemas.LoanUpdate, db:Session=Depends(get_db)):
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
def updateBranch(branchId:int, new_branch:schemas.BranchUpdate, db:Session=Depends(get_db)):
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
def updateTransaction(id:str, new_tran:schemas.TransactionUpdate, db:Session=Depends(get_db)):
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

# --- READ ENDPOINTS (FIXED) ---

@app.get('/customers')
def getCustomers(db:Session=Depends(get_db)):
    customer_data=db.query(database_models.Customer).all()
    # FIX: Check for an empty list
    if not customer_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No customer present in DB'
        )
    return {
        "status":"success",
        "data":customer_data
    }

@app.get('/customer/{id}')
def getCustomer(id:int, db:Session=Depends(get_db)):
    db_customer=db.query(database_models.Customer).filter(database_models.Customer.id==id).first()
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Specified ID not found'
        )
    return {
        "status":"success",
        "id":db_customer.id,
        "data":db_customer
    }

@app.get('/account/{accNo}')
def getAccount(accNo:int, db:Session=Depends(get_db)):
    db_acc=db.query(database_models.Account).filter(database_models.Account.accNo==accNo).first()
    if db_acc is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Account not found with the given Account No.'
        )
    return {
        "status":"success",
        "data":db_acc
    }

@app.get('/loan/{loanId}')
def getLoan(loanId:int, db:Session=Depends(get_db)): # Renamed function
    db_loan=db.query(database_models.Loan).filter(database_models.Loan.loanId==loanId).first()
    if db_loan is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Loan not found with the given Account No.' # Corrected detail
        )
    return {
        "status":"success",
        "data":db_loan
    }

@app.get('/branch/{branchId}')
def getBranch(branchId:int, db:Session=Depends(get_db)): # Renamed function
    db_branch=db.query(database_models.Branch).filter(database_models.Branch.branchId==branchId).first()
    if db_branch is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Branch not found with the given Branch ID.' # Corrected detail
        )
    return {
        "status":"success",
        "data":db_branch
    }

@app.get('/transaction/{id}')
def getTransaction(id:str, db:Session=Depends(get_db)): # Renamed function
    db_transaction=db.query(database_models.Transaction).filter(database_models.Transaction.id==id).first()
    if db_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Transaction not found with the given ID.' # Corrected detail
        )
    return {
        "status":"success",
        "data":db_transaction
    }

# --- ADMIN-ONLY PROTECTED ENDPOINT EXAMPLE ---
# This endpoint can only be accessed by a logged-in user who is an admin.
@app.get('/admin/all_customers', response_model=List[schemas.CustomerCreate])
def get_all_customers_admin(db: Session = Depends(get_db),admin_user: schemas.UserDisplay = Depends(auth.get_current_admin_user)):
    customers = db.query(database_models.Customer).all()
    if not customers:
        raise HTTPException(status_code=404, detail="No customers found")
    return customers

@app.get("/")
def read_root():
    """Welcome endpoint"""
    return {"message": "Welcome to the Simple Banking API"}