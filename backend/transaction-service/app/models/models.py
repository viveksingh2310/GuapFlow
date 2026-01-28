import uuid
from sqlalchemy import (Column, DateTime,String,Boolean,Date,Integer,CheckConstraint,Enum,Float,ForeignKey)
from sqlalchemy.dialects.postgresql import UUID,JSONB
from datetime import date, datetime
from app.db.db import Base
import enum
from sqlalchemy.orm import relationship

class Transaction(Base):
    __tablename__="transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id=Column(UUID(as_uuid=True), nullable=False, index=True)
    sender_acc=Column(String,nullable=False)#
    description=Column(String)
    receiver_acc=Column(String,nullable=False)#
    amount=Column(Integer,nullable=False)#
    timestamp= Column(DateTime, default=datetime.utcnow)
    isSuccess=Column(Boolean,nullable=False,default=True)
    onRevert=Column(Boolean,nullable=False,default=False)
    type=Column(String,default="default")