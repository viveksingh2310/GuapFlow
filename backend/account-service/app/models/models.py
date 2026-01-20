import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Date,
    Integer,
    CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from datetime import date
from app.db.db import Base

class Account(Base):
    __tablename__ = "account"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    acc_no = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    pin = Column(String, nullable=False)  # hashed before storing
    age = Column(Integer, nullable=False)
    amount = Column(Integer, default=0)
    other_charges = Column(Integer, default=0)
    opening_date = Column(Date, default=date.today)
    ifsc_code = Column(String, nullable=False)
    isDigital = Column(Boolean, default=False)
    pan_no = Column(String, nullable=False)
    aadhar_no = Column(String, nullable=False)
    type = Column(String, default="default")  # savings, current, minor, FD
    __table_args__ = (
        CheckConstraint("age >= 0", name="check_age_positive"),
        CheckConstraint("amount >= 0", name="check_amount_positive"),
        CheckConstraint("other_charges >= 0", name="check_charges_positive"),
    )
