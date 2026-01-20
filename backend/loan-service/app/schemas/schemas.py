from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import date
from typing import List, Optional, Union, Literal
from enum import Enum
# ---------------------------------------------------------BASE SCHEMA-------------------------------------------
class LoanTypeEnum(str, Enum):
    secured = "secured"
    unsecured = "unsecured"

class CurrentUser(BaseModel):
    user_id: UUID
    role: str
    
class LoanBase(BaseModel):
    name: str
    issue_date: date
    loan_type: LoanTypeEnum
    time: int
    consultant_name: str
    status: str  # approved, registered, repayed, checking
    class Config:
        from_attributes = True

class SecuredLoanBase(LoanBase):
    scheme_name: str
    collateral_type: str  # property, vehicle, FD, gold
    collateral_value: float
    assessed_value: Optional[float] = None
    files: Optional[List[str]] = []

class UnsecuredLoanBase(LoanBase):
    credit_score: int
    monthly_income: float
    emp_type: str  # salaried, self-employed
    emp_proof: Optional[List[str]] = []
    employer_name: str = "Not Applicable"
# ----------------------------------------------CREATE SCHEMA------------------------------------------------------
class LoanCreate(BaseModel):
    name:str
    issue_date:date
    loan_type:LoanTypeEnum
    time:int
    consultant_name:str
    status:str

class SecuredLoanCreate(LoanBase):
    loan_type:LoanTypeEnum
    scheme_name: str
    collateral_type: str  # property, vehicle, FD, gold
    collateral_value: float
    assessed_value: Optional[float] = None
    files: Optional[List[str]] = Field(default_factory=list)
    
class UnsecuredLoanCreate(LoanBase):
    loan_type: LoanTypeEnum
    credit_score: int
    monthly_income: float
    emp_type: str  # salaried, self-employed
    emp_proof: Optional[List[str]] = Field(default_factory=list)
    employer_name: str = "Not Applicable"

LoanCreateSchema = Union[
    SecuredLoanCreate,
    UnsecuredLoanCreate
]
# -----------------------------------------RESPONSE SCHEMA-------------------------------------------------------
class LoanResponseBase(BaseModel):
    id: UUID
    user_id: UUID
    acc_no: str
    name: str
    issue_date: date
    loan_type: LoanTypeEnum
    time: int
    consultant_name: str
    status: str
    class Config:
        from_attributes = True

class SecuredLoanResponse(LoanResponseBase):
    # loan_type: Literal["secured"]
    scheme_name: str
    collateral_type: str
    collateral_value: float
    assessed_value: Optional[float] = None
    files: List[str] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)

class UnsecuredLoanResponse(LoanResponseBase):
    # loan_type: Literal["unsecured"]
    credit_score: int
    monthly_income: float
    emp_type: str
    emp_proof: List[str] = Field(default_factory=list)
    employer_name: str
    model_config = ConfigDict(from_attributes=True)
    
LoanResponseSchema = Union[
    SecuredLoanResponse,
    UnsecuredLoanResponse
]
# --------------------------------------------------------UPDATE SCHEMA (BY USER)-----------------------------
class LoanUpdate(BaseModel):
    name:Optional[str]=None

class SecuredLoanUpdate(LoanUpdate):
    collateral_type:Optional[str]=None
    collateral_value:Optional[float]=None
    files:Optional[List[str]]=None

class UnsecuredLoanUpdate(LoanUpdate):
    emp_proof:Optional[List[str]]=None

LoanUpdateSchema=Union[
    SecuredLoanUpdate,
    UnsecuredLoanUpdate
    ]
# --------------------------------------------------------UPDATE SCHEMA (BY ADMIN)-----------------------------
class LoanUpdateAdmin(BaseModel):
    name:Optional[str]=None
    issue_date:Optional[date]=None
    time:Optional[int]=None
    consultant_name:Optional[str]=None
    status:Optional[str]=None #approved,registered,repayed,checking
    created_at:Optional[date]=None

class SecuredLoanUpdateAdmin(LoanUpdateAdmin):
    scheme_name:Optional[str]=None
    assessed_value:Optional[float]=None

class UnsecuredLoanUpdateAdmin(LoanUpdateAdmin):
    monthly_income:Optional[float]=None
    emp_type:Optional[str]=None
    emp_proof:Optional[List[str]]=None
    employer_name:Optional[str]=None
    credit_score:Optional[int]=None

LoanUpdateAdminSchema= Union[
    SecuredLoanUpdateAdmin,
    UnsecuredLoanUpdateAdmin
    ]