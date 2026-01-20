from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi import HTTPException, status,BackgroundTasks
from app.models.models import User
from app.schemas.schemas import UserCreate,UserBase,UserUpdate,UserResponse,UserUpdateAdmin
from passlib.context import CryptContext
from datetime import timedelta
from app.utils.security import create_access_token
from app.utils.emails import email_conf
from app.core.config import settings

pwd_context=CryptContext(schemes=["argon2"],deprecated="auto")
async def getauser(current_user: UserResponse):
    return current_user

async def create_user(db: AsyncSession, user: UserBase):
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd=pwd_context.hash(user.password)
    db_user = User(
        fname=user.fname,
        lname=user.lname,
        email=user.email,
        dob=user.dob,
        phone=user.phone,
        isAdmin=user.isAdmin,
        hashed_password=hashed_pwd,
        is_active=True
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    token_expires_minutes=timedelta(int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    role = settings.ROLE_ADMIN if db_user.isAdmin else settings.ROLE_USER
    access_token=create_access_token(data={"sub":str(db_user.id),"role":role},expires_delta=token_expires_minutes)
    return {
        "id": db_user.id,
        "fname": db_user.fname,
        "lname": db_user.lname,
        "email": db_user.email,
        "dob": db_user.dob,
        "phone": db_user.phone,
        "isAdmin":db_user.isAdmin,
        "is_active": db_user.is_active,
        "access_token": access_token,
        "token_type": "bearer"
    }

async def get_user(db:AsyncSession,user:UserCreate):
    query=select(User).where(User.email==user.email)
    result=await db.execute(query)
    db_user=result.scalars().first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
    if not pwd_context.verify(user.password,db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
    token_expires_minutes=timedelta(int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    role = settings.ROLE_ADMIN if db_user.isAdmin else settings.ROLE_USER
    access_token=create_access_token(data={"sub":str(db_user.id),"role":role},expires_delta=token_expires_minutes)
    return {
        "id": db_user.id,
        "fname": db_user.fname,
        "lname": db_user.lname,
        "email": db_user.email,
        "dob": db_user.dob,
        "phone": db_user.phone,
        "isAdmin":db_user.isAdmin,
        "is_active": db_user.is_active,
        "access_token": access_token,
        "token_type": "bearer"
    }

async def getAllUsers(user:UserResponse,db: AsyncSession):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details='Unauthorized user- Only ADMIN access.'
        )
    users=await db.execute(select(User))
    result=users.scalars()
    return result
    
async def update_user_service(db: AsyncSession, update_data: UserUpdate, current_user: User,background_tasks:BackgroundTasks):
    if update_data.fname:
        current_user.fname = update_data.fname
    if update_data.lname:
        current_user.lname = update_data.lname
    if update_data.dob:
        current_user.dob = update_data.dob
  
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    message = MessageSchema(
        subject="Profile Updated Successfully",
        recipients=[current_user.email], 
        body=f"""
        <h3>Hello {current_user.fname},</h3>
        <p>Your profile details have been successfully updated.</p>
        <p>If this wasn't you, please contact support immediately.</p>
        """,
        subtype=MessageType.html
    )
    fm = FastMail(email_conf)
    background_tasks.add_task(fm.send_message, message)
    return current_user



async def update_user_by_admin(db: AsyncSession, update_data: UserUpdateAdmin, current_user: User,background_tasks:BackgroundTasks):
    if update_data.id is None:
       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID not provided in the request"
        )
    query=select(User).where(User.id==update_data.id)
    result=await db.execute(query)
    db_user=result.scalars().first()
    if db_user is None: 
       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
       )
    if update_data.password:
       db_user.hashed_password=pwd_context.hash(update_data.password)
    if update_data.email:
        db_user.email=update_data.email
    if update_data.phone:
       db_user.phone=update_data.phone
    if update_data.isAdmin is not None:
        db_user.isAdmin=update_data.isAdmin
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    message = MessageSchema(
        subject="Profile Updated Successfully",
        recipients=[db_user.email], 
        body=f"""
        <h3>Hello {db_user.fname},</h3>
        <p>Admin has succesfully updated your details.</p>
        <p>Please login(with updated credentials if done)after 30 minutes to see the updated details.</p>
        <p>If this wasn't you, please contact support immediately.</p>
        """,
        subtype=MessageType.html
    )
    fm = FastMail(email_conf)
    background_tasks.add_task(fm.send_message, message)
    return db_user

async def is_admin(user:UserResponse):
    if not user.isAdmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: User is not an admin"
        )
    # If they are admin, return the user object

    return user