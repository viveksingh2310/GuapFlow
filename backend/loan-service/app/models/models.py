import uuid
from sqlalchemy import (Column,String,Boolean,Date,Integer,CheckConstraint,Enum,Float,ForeignKey)
from sqlalchemy.dialects.postgresql import UUID,JSONB
from datetime import date
from app.db.db import Base
import enum
from sqlalchemy.orm import relationship

class LoanType(enum.Enum):
    secured = "secured"
    unsecured = "unsecured"

class Loan(Base):
    __tablename__="loans"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id=Column(UUID(as_uuid=True), nullable=False, index=True)
    acc_no = Column(String, unique=True, nullable=False)
    name=Column(String,nullable=False)
    issue_date=Column(Date,nullable=False)
    loan_type=Column(Enum(LoanType), nullable=False)
    time=Column(Integer,nullable=False)
    consultant_name=Column(String,nullable=False)
    status=Column(String,nullable=False) #approved,registered,repayed,checking
    created_at = Column(Date, default=date.today)
    __mapper_args__ = {
        "polymorphic_on": loan_type,
        "polymorphic_identity": "loan"
    }

class SecuredLoan(Loan):
    __tablename__ = "secured_loans"

    id = Column(UUID(as_uuid=True), ForeignKey("loans.id", ondelete="CASCADE"), primary_key=True)
    scheme_name = Column(String, nullable=False)
    collateral_type = Column(String,nullable=False)  # property, vehicle, FD, gold
    collateral_value = Column(Float, nullable=False)
    assessed_value = Column(Float, nullable=True)
    files = Column(JSONB,nullable=True,default=list)
    __mapper_args__ = {
        "polymorphic_identity": LoanType.secured
    }

class UnsecuredLoan(Loan):
    __tablename__ = "unsecured_loans"

    id = Column(UUID(as_uuid=True), ForeignKey("loans.id", ondelete="CASCADE"), primary_key=True)
    credit_score = Column(Integer, nullable=False)
    monthly_income = Column(Float, nullable=False)
    emp_type = Column(String,nullable=False)  # salaried, self-employed
    emp_proof = Column(JSONB,nullable=True,default=list)
    employer_name = Column(String,nullable=False,default="Not Applicable")
    __mapper_args__ = {
        "polymorphic_identity": LoanType.unsecured
    }