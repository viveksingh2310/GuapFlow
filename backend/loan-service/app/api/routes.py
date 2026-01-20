from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.models import Loan
from app.utils.security import get_current_user,get_admin_user,get_token
from app.schemas.schemas import LoanResponseSchema,LoanCreateSchema,CurrentUser,LoanUpdateSchema,LoanUpdateAdminSchema
from app.services.services import createLoan,get,updateByUser,adminUpdate
router=APIRouter(prefix="/loans")

@router.post('/',response_model=LoanResponseSchema)
async def makeLoan(loan:LoanCreateSchema,user:CurrentUser=Depends(get_current_user),db:Session=Depends(get_db),token:str=Depends(get_token)):
    return await createLoan(loan,user.user_id,db,token)

@router.get('/',response_model=LoanResponseSchema)
async def getLoan(user:CurrentUser=Depends(get_current_user),db:Session=Depends(get_db)):
    return await get(user.user_id,db)

@router.get('/admin',response_model=LoanResponseSchema)
async def getAdminLoan(user:CurrentUser=Depends(get_admin_user),db:Session=Depends(get_db)):
    return await get(user.user_id,db)

@router.patch('/',response_model=LoanResponseSchema)
async def udpate(new_loan:LoanUpdateSchema,loan:LoanResponseSchema=Depends(getLoan),db:Session=Depends(get_db)):
    return await updateByUser(new_loan,loan,db)

@router.patch('/admin',response_model=LoanResponseSchema)
async def admin(new_loan:LoanUpdateAdminSchema,loan:LoanResponseSchema=Depends(getAdminLoan),db:Session=Depends(get_db)):
    return await adminUpdate(new_loan,loan,db)