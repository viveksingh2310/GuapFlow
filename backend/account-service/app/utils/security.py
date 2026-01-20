from jose import jwt
from fastapi import Depends
from fastapi import HTTPException, Header
from app.core.config import settings
from app.schemas.schemas import CurrentUser

def verify_token(token: str):
    try:
        print('this is the fucking token')
        print(token)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # user_id:str=payload.get('sub')
        # role:str=payload.get('role')
        # print('i am at the get current user and the role not chicke roll is ')
        # print(role)
        # print('i am at the verify token function and here the user id is as follows:')
        # print(user_id)
        return CurrentUser(
        user_id=payload.get("sub"),
        role=payload.get("role"),
    )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    return verify_token(token)
def get_token(authorization: str = Header(...)):
    token=authorization.replace("Bearer ", "")
    return token
def get_admin_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    current_user=verify_token(token)
    return admin_required(current_user)

def admin_required(current_user:CurrentUser):
    if current_user.role!="admin":
        raise HTTPException(
            status_code=401,
            detail="Only Admin-accessible route"
        )
    return current_user