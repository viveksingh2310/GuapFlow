from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.utils.security import get_current_user,get_token
from app.services.services import getDef,createConsultant,getLoan,select_consultant,createConversation
from app.schemas.schemas import ConsultantResponse,ConsultantCreate,CurrentUser,ConversationResponse
router=APIRouter(prefix="/chats")

@router.get('/')
async def getDefault():
    return await getDef()

@router.post('/consultant',response_model=ConsultantResponse)
async def consultantCreate(consultant:ConsultantCreate,db:Session=Depends(get_db)):
    return await createConsultant(consultant,db)

@router.get('/consul',response_model=None)
async def getConsultant(db:Session=Depends(get_db)):
    return await select_consultant(db)

@router.get('/getLoan',response_model=None)
async def getloan(token:str=Depends(get_token)):
    return await getLoan(token)

@router.post('/conversation',response_model=ConversationResponse)
async def createCon(current_user:CurrentUser=Depends(get_current_user),token:str=Depends(get_token),db:Session=Depends(get_db)):
    return await createConversation(current_user.user_id,token,db)