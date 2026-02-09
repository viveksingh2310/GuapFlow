from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr
from enum import Enum

class ConsultantStatus(str, Enum):
    online = "online"
    offline = "offline"
    busy = "busy"

class ConversationStatus(str, Enum):
    active = "active"
    closed = "closed"
    escalated = "escalated"

class SenderType(str, Enum):
    user = "user"
    consultant = "consultant"
#---------------CONSULTANT---------------
class ConsultantBase(BaseModel):
    name: str
    email: EmailStr
    specs: Optional[List[str]] = []

class ConsultantCreate(ConsultantBase):
    name:str
    email:str
    status:ConsultantStatus
    specs:Optional[List[str]]=[]

class ConsultantResponse(ConsultantBase):
    id: UUID
    status: ConsultantStatus
    last_assigned_at:datetime
    class Config:
        orm_mode = True
#--------------------CONVERSATION----------------------
class ConversationBase(BaseModel):
    loan_id: UUID
    user_id: UUID
    consultant_id: UUID

class ConversationCreate(ConversationBase):
    loan_id:UUID
    user_id:UUID
    consultant_id:UUID
    status:ConversationStatus

class ConversationResponse(ConversationBase):
    id: UUID
    status: ConversationStatus
    created_at: datetime
    class Config:
        orm_mode = True

#------------------------------MESSAGE--------------------------------

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    conversation_id: UUID
    sender_id: UUID
    sender_type: SenderType
    content:str

class MessageResponse(MessageBase):
    id: UUID
    conversation_id: UUID
    sender_id: UUID
    sender_type: SenderType
    timestamp: datetime
    class Config:
        orm_mode = True
        
class CurrentUser(BaseModel):
    user_id: UUID
    role: str