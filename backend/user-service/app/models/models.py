import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Boolean,Date
from app.db.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    fname=Column(String,nullable=False)
    lname=Column(String)
    dob=Column(Date,nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone=Column(String,nullable=False)
    hashed_password = Column(String, nullable=False)
    isAdmin=Column(Boolean,default=False)
    is_active = Column(Boolean, default=True)