from datetime import timedelta,datetime
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_db
from jose import jwt,JWTError
from app.models.models import User
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings 


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
credentials_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt=jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token:str=Depends(oauth2_scheme),db: AsyncSession = Depends(get_db)):   
        try:
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
            id:str=payload.get('sub')
            role:str=payload.get('role')
            print('i am at the get current user and the role not chicke roll is ')
            print(role)
            if id is None:
                 raise credentials_exception
        except JWTError:
                 raise credentials_exception
        query=select(User).where(User.id==id)
        result=await db.execute(query)
        user=result.scalars().first()
        if user is None:
            raise credentials_exception
        return user
     