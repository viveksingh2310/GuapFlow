from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.models import Loan,SecuredLoan,UnsecuredLoan,LoanType
from app.core.config import Settings
from fastapi import HTTPException,status
from passlib.context import CryptContext
from uuid import UUID
import httpx
from app.schemas.schemas import LoanCreateSchema,UnsecuredLoanResponse,SecuredLoanResponse,LoanUpdateSchema,LoanUpdateAdminSchema

async def fetch_account_number(token:str) -> str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        print('token is '+token)
        response = await client.get(
            f"{Settings.ACCOUNT_SERVICE_URL}/accno",
              headers={
                "Authorization": f"Bearer {token}"
            }
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to fetch account number from AccountService"
        )
    return response.json()["acc_no"]
async def createLoan(loan: LoanCreateSchema,user_id: UUID,db: AsyncSession,token: str):
    result = await db.execute(select(Loan).where(Loan.user_id == user_id))
    existing_loan = result.scalars().first()
    if existing_loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan already exists"
        )
    acc_no = await fetch_account_number(token)
    print(acc_no)
    if loan.loan_type == "secured":
        db_loan = SecuredLoan(
            user_id=user_id,
            acc_no=acc_no,
            name=loan.name,
            issue_date=loan.issue_date,
            loan_type=LoanType.secured,
            time=loan.time,
            consultant_name=loan.consultant_name,
            status=loan.status,
            scheme_name=loan.scheme_name,
            collateral_type=loan.collateral_type,
            collateral_value=loan.collateral_value,
            assessed_value=loan.assessed_value,
            files=loan.files or [],
        )

    elif loan.loan_type == "unsecured":
        db_loan = UnsecuredLoan(
            user_id=user_id,
            acc_no=acc_no,
            name=loan.name,
            issue_date=loan.issue_date,
            loan_type=LoanType.unsecured,
            time=loan.time,
            consultant_name=loan.consultant_name,
            status=loan.status,
            credit_score=loan.credit_score,
            monthly_income=loan.monthly_income,
            emp_type=loan.emp_type,
            emp_proof=loan.emp_proof or [],
            employer_name=loan.employer_name,
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid loan type"
        )
    db.add(db_loan)
    await db.commit()
    await db.refresh(db_loan)
    return db_loan

async def get(user_id: UUID, db: AsyncSession):
    result = await db.execute(select(Loan.loan_type).where(Loan.user_id == user_id))
    loan_type = result.scalar_one_or_none()

    if not loan_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    if loan_type == LoanType.unsecured:
        result = await db.execute(
            select(UnsecuredLoan).where(UnsecuredLoan.user_id == user_id)
        )
        db_loan = result.scalar_one()

        return UnsecuredLoanResponse(
            id=db_loan.id,
            user_id=db_loan.user_id,
            acc_no=db_loan.acc_no,
            name=db_loan.name,
            issue_date=db_loan.issue_date,
            loan_type=db_loan.loan_type.value,
            time=db_loan.time,
            consultant_name=db_loan.consultant_name,
            status=db_loan.status,
            credit_score=db_loan.credit_score,
            monthly_income=db_loan.monthly_income,
            emp_type=db_loan.emp_type,
            emp_proof=db_loan.emp_proof or [],
            employer_name=db_loan.employer_name,
        )
        # return db_loan
    
    if loan_type == LoanType.secured:
        result = await db.execute(
            select(SecuredLoan).where(SecuredLoan.user_id == user_id)
        )
        db_loan = result.scalar_one()
        return SecuredLoanResponse(
            id=db_loan.id,
            user_id=db_loan.user_id,
            acc_no=db_loan.acc_no,
            name=db_loan.name,
            issue_date=db_loan.issue_date,
            loan_type=db_loan.loan_type.value,
            time=db_loan.time,
            consultant_name=db_loan.consultant_name,
            status=db_loan.status,
            scheme_name=db_loan.scheme_name,
            collateral_type=db_loan.collateral_type,
            collateral_value=db_loan.collateral_value,
            assessed_value=db_loan.assessed_value,
            files=db_loan.files or [],
        )
        # return db_loan
    raise HTTPException(500, "Invalid loan type")

async def updateByUser(new_loan:LoanUpdateSchema,loan:Loan,db: AsyncSession):
    # print('here is the new loan given to be updated and its is inside the update by user function')
    # print(new_loan)
    result=await db.execute(select(Loan).where(Loan.user_id==loan.user_id))
    old_loan=result.scalars().first()
    print('this is the old loan that i get from database as model:')
    print(old_loan)
    if old_loan.loan_type==LoanType.secured:
        if new_loan.collateral_type:
            old_loan.collateral_type=new_loan.collateral_type
        if new_loan.collateral_value:
            old_loan.collateral_value=new_loan.collateral_value
        if new_loan.files:
            old_loan.files=new_loan.files
    elif old_loan.loan_type==LoanType.unsecured:
        if new_loan.emp_proof:
            old_loan.emp_proof=new_loan.emp_proof
    db.add(old_loan)
    await db.commit()
    await db.refresh(old_loan)
    return old_loan


async def adminUpdate(new_loan:LoanUpdateAdminSchema,loan:Loan,db: AsyncSession):
    result=await db.execute(select(Loan).where(Loan.user_id==loan.user_id))
    old_loan=result.scalars().first()
    print('this is the old loan that i get from database as model:')
    print(old_loan)
    if new_loan.name:
        old_loan.name=new_loan.name
    if new_loan.issue_date:
        old_loan.issue_date=new_loan.issue_date
    if new_loan.time:
        old_loan.time=new_loan.time
    if new_loan.consultant_name:
        old_loan.consultant_name=new_loan.consultant_name
    if new_loan.status:
        old_loan.status=new_loan.status
    if new_loan.created_at:
        old_loan.created_at=new_loan.created_at
    if old_loan.loan_type==LoanType.secured:
        if new_loan.scheme_name:
            old_loan.scheme_name=new_loan.scheme_name
        if new_loan.assessed_value:
            old_loan.assessed_value=new_loan.assessed_value
    elif old_loan.loan_type==LoanType.unsecured:
        if new_loan.monthly_income:
            old_loan.monthly_income=new_loan.monthly_income
        if new_loan.emp_type:
            old_loan.emp_type=new_loan.emp_type
        if new_loan.emp_proof:
            old_loan.emp_proof=new_loan.emp_proof
        if new_loan.employer_name:
            old_loan.employer_name=new_loan.employer_name
        if new_loan.credit_score:
            old_loan.credit_score=new_loan.credit_score
    db.add(old_loan)
    await db.commit()
    await db.refresh(old_loan)
    return old_loan