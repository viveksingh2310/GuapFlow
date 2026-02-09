from jose import jwt
from fastapi import Depends, WebSocket
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
# this is for the websocket function 
# ---------------------------------------------------------------------------------------
def websocket_verify_token(token: str) -> CurrentUser:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return CurrentUser(
            user_id=payload.get("sub"),
            role=payload.get("role"),
        )

    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")

    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
#  this is again for the websocket as well
async def websocket_get_current_user(websocket: WebSocket) -> CurrentUser:

    auth_header = websocket.headers.get("authorization")

    if not auth_header:
        await websocket.close(code=1008)
        raise Exception("Authorization header missing")

    if not auth_header.startswith("Bearer "):
        await websocket.close(code=1008)
        raise Exception("Invalid authorization format")

    token = auth_header.replace("Bearer ", "")

    try:
        current_user = websocket_verify_token(token)
        return current_user

    except Exception:
        await websocket.close(code=1008)
        raise
# -----------------------------------------------------------------------------------
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