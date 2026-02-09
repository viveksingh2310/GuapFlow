from app.schemas.schemas import ConsultantCreate,ConversationCreate,MessageCreate
from app.models.models import Consultant,Conversation,Message
from typing import List
import httpx
from fastapi import HTTPException,status
from sqlalchemy import select,update,func
from uuid import UUID
from app.core.config import Settings
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime  # Import datetime module

async def getDef():
    return {"message":"the chatting service is working fine now"}

async def createConsultant(consultant:ConsultantCreate,db:AsyncSession):
    result=await db.execute(select(Consultant).where(Consultant.email==consultant.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consultant already exists."
        )
    db_consultant=Consultant(
        name=consultant.name,
        email=consultant.email,
        status=consultant.status,
        specs=consultant.specs
    )
    db.add(db_consultant)
    await db.commit()
    await db.refresh(db_consultant)
    return db_consultant

async def getLoan(token:str):
    async with httpx.AsyncClient(timeout=5.0) as client:
        print('inside the getloan function')
        response=await client.get(
            f"{Settings.LOAN_SERVICE_URL}/",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
    if response.status_code!=200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to fetch account number from AccountService"
        )
    return response.json()["id"]

async def select_consultant(db: AsyncSession):
    async with db.begin():
        result = await db.execute(
            select(Consultant)
            .where(Consultant.status == "online")
            .order_by(Consultant.last_assigned_at)
            .with_for_update()
            .limit(1)
        )
        consultant = result.scalars().first()
        if not consultant:
            return None
        consultant.last_assigned_at = func.now()  # ✅ DB time
        db.add(consultant)
        db.flush()
        return consultant.id

async def createConversation(user_id:UUID,token:str,db:AsyncSession):
    consultant_id=await select_consultant(db)
    loan_id=await getLoan(token)
    result=await db.execute(select(Conversation).where(Conversation.loan_id==loan_id))
    if result.scalars().first():
      return result.scalars().first()
    db_conversation=Conversation(
        loan_id=loan_id,
        user_id=user_id,
        consultant_id=consultant_id,
        status="active",
        created_at=func.now()
    )
    db.add(db_conversation)
    await db.commit()
    await db.refresh(db_conversation)
    return db_conversation

async def validate_conversation(db: AsyncSession,conversation_id: UUID,user_id: UUID):
    result = await db.execute(
        select(Conversation)
        .where(Conversation.id == conversation_id)
    )
    conversation = result.scalars().first()
    if not conversation:
        return None
    if user_id not in [
        conversation.user_id,
        conversation.consultant_id
    ]:
        return None
    return conversation

async def validate_message(db:AsyncSession,conversation_id:UUID):
    result=await db.execute(select(Message).where(Message.conversation_id==conversation_id))
    messages=result.scalars()
    if not result:
        return None
    return messages

async def create_message(conversation_id:UUID,sender_id:UUID,sender_type:str,content:str,db:AsyncSession):
    db_message=Message(
        conversation_id=conversation_id,
        sender_id=sender_id,
        sender_type=sender_type,
        content=content,
        timestamp=func.now()
    )
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message