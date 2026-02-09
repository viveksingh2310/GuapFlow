import uuid
from sqlalchemy import (ARRAY,Column,String,DateTime)
from sqlalchemy import Enum,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import date, datetime
from app.db.db import Base

class Consultant(Base):
    __tablename__ = "consultants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    status = Column(Enum("online", "offline", "busy", name="consultant_status"),default="offline")
    specs = Column(ARRAY(String))  # Postgres array
    last_assigned_at = Column(DateTime, default=datetime.utcnow)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loan_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    consultant_id = Column(UUID(as_uuid=True),ForeignKey("consultants.id"),nullable=False)
    status = Column(Enum("active", "closed", "escalated", name="conversation_status"),default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True),ForeignKey("conversations.id"),nullable=False,index=True)
    sender_id = Column(UUID(as_uuid=True), nullable=False) #either user_id, consultant_id
    sender_type = Column(Enum("user", "consultant", name="sender_type"),nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)