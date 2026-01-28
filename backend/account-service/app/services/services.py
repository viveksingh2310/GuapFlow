from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from app.models.models import Account
from fastapi import HTTPException,status
from app.schemas.schemas import AccountCreate,AccountLogin,UpdateAccountByUser,AccountResponse,UpdateAccountByAdmin,AccountTransactionDetail
from passlib.context import CryptContext
from uuid import UUID

pwd_context=CryptContext(schemes=["argon2"],deprecated="auto")

async def createAccount(account:AccountCreate,user_id:UUID,db:AsyncSession):
    # print('i am at the create Account function and here the user id is as follows:')
    print(user_id)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User not logged in before'
        )
    result=await db.execute(select(Account).where(Account.acc_no==account.acc_no))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The user already exist please login'
        )
    hashed_pin = pwd_context.hash(str(account.pin))
    db_account = Account(
        user_id=user_id,
        acc_no=account.acc_no,
        name=account.name,
        phone=account.phone,
        email=account.email,
        dob=account.dob,
        age=account.age,
        pin=hashed_pin,
        amount=account.amount,
        ifsc_code=account.ifsc_code,
        isDigital=account.isDigital,
        pan_no=account.pan_no,
        aadhar_no=account.aadhar_no,
        type=account.type
    )
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account

async def login(account:AccountLogin,user_id:UUID,db:AsyncSession):
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User not logged in before'
        )
    result=await db.execute(select(Account).where(Account.email==account.email))
    account_db=result.scalars().first()
    if account_db is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No user exist, Register first'
        )
    if not pwd_context.verify(account.pin,account_db.pin):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
    return account_db

async def updateAc(account:UpdateAccountByUser,db_account:AccountResponse,db:AsyncSession):
    if account.name:
        db_account.name=account.name
    if account.phone:
        db_account.phone=account.phone
    if account.email:
        db_account.email=account.email
    if account.dob:
         db_account.dob=account.dob
    if account.pin:
        db_account.pin=pwd_context.hash(account.pin)
    if account.isDigital:
         db_account.isDigital=account.isDigital
    if account.pan_no:
         db_account.pan_no=account.pan_no
    if account.aadhar_no:
         db_account.aadhar_no=account.aadhar_no
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account

async def updatebyadmin(account:UpdateAccountByAdmin,user_id:UUID,db:AsyncSession):
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin accessible."
        )
    result=await db.execute(select(Account).where(Account.user_id==user_id))
    db_account=result.scalars().first()
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin accessible."
        )
    if account.acc_no:
        db_account.acc_no= account.acc_no
    if account.amount:
        db_account.amount= account.amount
    if account.other_charges:
        db_account.other_charges= account.other_charges
    if account.opening_date:
        db_account.opening_date= account.opening_date
    if account.ifsc_code:
        db_account.ifsc_code= account.ifsc_code
    if account.type:
        db_account.type=account.type
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account

async def get(user_id:UUID,db:AsyncSession):
    result=await db.execute(select(Account).where(Account.user_id==user_id))
    res=result.scalars().first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Create account first"
        )
    return res
async def getAc(user_id:UUID,db:AsyncSession):
    result=await db.execute(select(Account).where(Account.user_id==user_id))
    res=result.scalars().first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Create account first"
        )
    return {
        "user_id": user_id,
        "acc_no": res.acc_no,
        "amount":res.amount
    }
async def accountValidation(account_no:str,db:AsyncSession):
    result=await db.execute(select(Account).where(Account.acc_no==account_no))
    res=result.scalars().first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account does not exist for this user id"
        )
    return {
        "user_id": res.user_id,
        "acc_no": account_no,
        "amount":res.amount
        }
async def exec_Transaction(tran_details: AccountTransactionDetail, user_id: UUID, db: AsyncSession):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized route access"
        )

    sender_acc = tran_details.sender_acc
    receiver_acc = tran_details.receiver_acc
    amnt = tran_details.amount

    sender_res = await db.execute(
        select(Account).where(Account.acc_no == sender_acc)
    )
    receiver_res = await db.execute(
        select(Account).where(Account.acc_no == receiver_acc)
    )

    sender = sender_res.scalars().first()
    receiver = receiver_res.scalars().first()

    if not sender:
        raise HTTPException(400, "Sender account does not exist")

    if not receiver:
        raise HTTPException(400, "Receiver account does not exist")

    if sender.amount < amnt:
        raise HTTPException(400, "Insufficient balance")

    # Debit sender
    await db.execute(
        update(Account)
        .where(Account.acc_no == sender_acc)
        .values(amount=Account.amount - amnt)
    )

    # Credit receiver
    await db.execute(
        update(Account)
        .where(Account.acc_no == receiver_acc)
        .values(amount=Account.amount + amnt)
    )

    await db.commit()
    return sender