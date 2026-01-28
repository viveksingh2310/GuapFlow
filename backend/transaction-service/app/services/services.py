from fastapi import HTTPException,status
import httpx
from app.schemas.schemas import UserTransactionDetail,CurrentUser
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import Settings
from sqlalchemy import insert,select
from app.models.models import Transaction

async def fetch_account_number(token:str) -> str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        print('token is '+token)
        response = await client.get(
            f"{Settings.ACCOUNT_SERVICE_URL}/accno",
              headers={
                "Authorization": f"Bearer {token}"
            }
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to fetch account number from AccountService"
        )
    return response.json()["acc_no"]

async def validateAccountNumber(acc_no:str)->str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(
            f"{Settings.ACCOUNT_SERVICE_URL}/validateAc/{acc_no}"
        )
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to fetch account number from AccountService"
        )
    return response.json()["acc_no"]

async def executeTransaction(sender_acc:str,receiver_acc:str,amount:int,token:str)->str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            f"{Settings.ACCOUNT_SERVICE_URL}/createTransaction",
             headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "sender_acc":sender_acc,
                "receiver_acc":receiver_acc,
                "amount":amount
            }
        )
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to fetch account number from AccountService"
        )
    return response.json()

async def createTransaction(trans_details: UserTransactionDetail,user: CurrentUser,token: str,db: AsyncSession):
    receiver_info = await validateAccountNumber(trans_details.receiver_acc)
    if not receiver_info:
        raise HTTPException(400, "Receiver does not exist")
    sender_acc = await fetch_account_number(token)
    result = await executeTransaction(
        sender_acc,
        trans_details.receiver_acc,
        trans_details.amount,
        token
    )
    new_tx = Transaction(
        user_id=user.user_id,
        sender_acc=sender_acc,
        receiver_acc=trans_details.receiver_acc,
        amount=trans_details.amount,
        description=trans_details.description,
        isSuccess=True,
        onRevert=False,
        type="transfer"
    )
    db.add(new_tx)
    await db.commit()
    await db.refresh(new_tx)
    return new_tx

async def getAllTransactions(user: CurrentUser, db: AsyncSession):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access only"
        )
    result = await db.execute(select(Transaction))
    return result.scalars().all()