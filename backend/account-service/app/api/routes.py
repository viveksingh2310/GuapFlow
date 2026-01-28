from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from pydantic import Json
from app.utils.security import get_current_user,get_admin_user
from app.services.services import createAccount,login,updateAc,get,updatebyadmin,getAc,accountValidation,exec_Transaction
from app.schemas.schemas import AccountCreate,AccountResponse,AccountLogin,UpdateAccountByUser,CurrentUser,UpdateAccountByAdmin,AccNoResponse,AccountTransactionDetail

router=APIRouter(prefix="/accounts")

@router.post('/',response_model=AccountResponse)
async def createaccount(account:AccountCreate,current_user:CurrentUser=Depends(get_current_user),db:Session=Depends(get_db)):
    return await createAccount(account,current_user.user_id,db)

@router.get('/',response_model=AccountResponse)
async def getAcccount(current_user:CurrentUser=Depends(get_current_user),db:Session=Depends(get_db)):
    return await get(current_user.user_id,db)

@router.get('/accno',response_model=AccNoResponse)
async def getAcc(current_user:CurrentUser=Depends(get_current_user),db:Session=Depends(get_db)):
    return await getAc(current_user.user_id,db)

@router.get('/validateAc/{acc_no}',response_model=AccNoResponse)
async def getValAc(acc_no:str,db:Session=Depends(get_db)):
    return await accountValidation(acc_no,db)

@router.post('/createTransaction',response_model=AccountResponse)
async def createTrans(tran_details:AccountTransactionDetail,current_user:CurrentUser=Depends(get_current_user),db:Session=Depends(get_db)):
    return await exec_Transaction(tran_details,current_user.user_id,db)

@router.post('/login',response_model=AccountResponse)
async def checkUser(account:AccountLogin,current_user:CurrentUser=Depends(get_current_user),db:Session=Depends(get_db)):
    return await login(account,current_user.user_id,db)

@router.put('/update',response_model=AccountResponse)
async def updateAccount(account:UpdateAccountByUser,db_account:AccountResponse=Depends(checkUser),db:Session=Depends(get_db)):
    return await updateAc(account,db_account,db)

@router.put('/admin',response_model=AccountResponse)
async def updateAdmin(account:UpdateAccountByAdmin,current_user:CurrentUser=Depends(get_admin_user),db:Session=Depends(get_db)):
    return await updatebyadmin(account,current_user.user_id,db)