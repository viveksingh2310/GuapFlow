# schemas.py
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    sender_acc: str
    receiver_acc: str
    amount: int
    description: str
    type: str = "default"

class TransactionCreate(TransactionBase):
    user_id: UUID

class TransactionResponse(TransactionBase):
    id: UUID
    user_id: UUID
    timestamp: datetime
    isSuccess: bool
    onRevert: bool

    class Config:
        orm_mode = True


class CurrentUser(BaseModel):
    user_id: UUID
    role: str

class UserTransactionDetail(BaseModel):
    receiver_acc: str
    amount: int
    description: str
