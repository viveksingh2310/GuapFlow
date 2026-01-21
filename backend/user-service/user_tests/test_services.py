from app.services.services import create_user,get_user,getAllUsers,update_user_service,update_user_by_admin,is_admin
import pytest
from fastapi import BackgroundTasks
from app.services import services
from uuid import uuid4
from types import SimpleNamespace
from app.schemas.schemas import UserBase,UserCreate,UserUpdate,UserUpdateAdmin

class FakeResult:
    def __init__(self,obj):
        self._obj=obj
    def scalars(self):
        return self
    def first(self):
        return self._obj
    
class FakeAsyncSession:
    def __init__(self,result=None):
        self._result=result
        self.added=None
        self.committed=False
        self.refreshed=False
    
    async def execute(self,*_):
        return FakeResult(self._result)
    def add(self,obj):
        self.added=obj
    async def commit(self):
        self.committed=True
    async def refresh(self,obj):
        self.refreshed=True
    async def rollback(self):
        pass

def fake_user():
    return SimpleNamespace(
        id=str(uuid4()),
        fname="Vivek",
        lname="Singh",
        dob="2003-10-23",
        email="1234@gmail.com",
        phone="1234567890",
        hashed_password="flskjfdsafsdfsfd",
        isAdmin=False,
        is_active=True
    )

@pytest.mark.asyncio
async def test_create_user():
    db = FakeAsyncSession(result=None)
    user = UserBase(
        fname="Vivek",
        lname="Singh",
        dob="2003-10-23",
        email="1234@gmail.com",
        phone="1234567890",
        password="StrongPass123",
        isAdmin=True
    )
    result= await create_user(db,user)
    assert db.added is not None
    assert db.committed is True
    assert db.refreshed is True
    assert result["email"]==user.email

@pytest.mark.asyncio
async def test_get_user():
    db=FakeAsyncSession(result=fake_user())
    user=UserCreate(
        email="1234@gmail.com",
        password="StrongPass123"
    )
    services.pwd_context.verify=lambda *_: True
    result= await get_user(db,user)
    assert result["email"]==user.email
    assert result["fname"]=="Vivek"

@pytest.mark.asyncio
async def test_get_all_users():
    db=FakeAsyncSession(result=fake_user())
    test_create_user()
    result =await getAllUsers(fake_user(),db)
    assert result.scalars() is not None
    assert result.first().fname == "Vivek"

@pytest.mark.asyncio
async def test_update_user_service():
    db=FakeAsyncSession(result=None)
    tmp_bg_tasks=BackgroundTasks()
    user_update=UserUpdate(
        fname="Viiiivek",
        lname="SSINGH"
    )
    curr_user=fake_user()
    result=await update_user_service(db,user_update,curr_user,tmp_bg_tasks)
    assert result.fname==user_update.fname
    assert result.lname==user_update.lname

@pytest.mark.asyncio
async def test_update_user_by_admin():
    db=FakeAsyncSession(result=fake_user())
    tmp_bg_tasks=BackgroundTasks()
    curr_user=fake_user()
    update_data=UserUpdateAdmin(
        id=uuid4(),
        email="test_email@gmail.com",
        isAdmin=False
    )
    result=await update_user_by_admin(db,update_data,curr_user,tmp_bg_tasks)
    assert result.email==update_data.email
    assert result.isAdmin is not True

@pytest.mark.asyncio
async def test_is_admin():
    user=fake_user()
    user.isAdmin=True
    result =await is_admin(user)
    assert result.isAdmin is True
    assert result.fname=="Vivek"
