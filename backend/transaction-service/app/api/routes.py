from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_db
from app.utils.security import get_current_user,get_token
from app.schemas.schemas import CurrentUser,UserTransactionDetail,TransactionResponse
from app.services.services import createTransaction, getAllTransactions
router=APIRouter(prefix="/transactions")


@router.post('/', response_model=TransactionResponse)
async def makeTransaction(
    trans_details: UserTransactionDetail,
    user: CurrentUser = Depends(get_current_user),
    token: str = Depends(get_token),
    db: AsyncSession = Depends(get_db)
):
    return await createTransaction(trans_details, user, token, db)


@router.get('/all', response_model=list[TransactionResponse])
async def fetchAllTransactions(
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await getAllTransactions(user, db)
