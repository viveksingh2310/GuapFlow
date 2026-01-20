from typing import List
from fastapi import APIRouter, Depends,BackgroundTasks
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.schemas import UserCreate, UserResponse,UserBase,UserAuthResponse,UserUpdate,UserUpdateAdmin
from app.services.services import create_user,get_user,update_user_service,is_admin,update_user_by_admin,getAllUsers,getauser
from app.utils.security import get_current_user

router = APIRouter(prefix="/users")

@router.get("/")
def getUsers():
    return {"dfghjk":"lkjhgf"}

@router.get("/me",response_model=UserResponse)
async def getUser(current_user: UserResponse = Depends(get_current_user)):
    return await getauser(current_user)

@router.get('/isAdmin', response_model=UserResponse)
async def check_admin_route(current_user: UserResponse = Depends(get_current_user)):
    return await is_admin(current_user)

@router.get('/all', response_model=List[UserResponse])
async def getAllUser(current_user:UserResponse=Depends(check_admin_route),db:Session=Depends(get_db)):
    return await getAllUsers(current_user,db)

@router.post("/", response_model=UserAuthResponse)
async def create(user: UserBase, db: Session = Depends(get_db)):
    new_user=await create_user(db, user)
    return new_user

@router.put("/update", response_model=UserResponse)
async def update_user_route(update_data: UserUpdate, background_tasks: BackgroundTasks,db: Session = Depends(get_db),current_user: UserResponse = Depends(get_current_user)):
    return await update_user_service(db, update_data, current_user,background_tasks)

@router.put('/adminUpdate',response_model=UserResponse)
async def updateByAdmin(update_data:UserUpdateAdmin, background_tasks: BackgroundTasks,db: Session = Depends(get_db),current_user: UserResponse = Depends(check_admin_route)):
    return await update_user_by_admin(db, update_data, current_user,background_tasks)

@router.post('/check',response_model=UserAuthResponse)
async def loginUser(user:UserCreate,db:Session=Depends(get_db)):
    return await get_user(db,user)