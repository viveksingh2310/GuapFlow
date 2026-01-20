from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4
from app.utils.security import get_current_user
from app.api.routes import check_admin_route
client=TestClient(app)
class FakeUser:
    def __init__(self,user_id,role="user"):
        self.user_id=user_id
        self.role=role

class FakeAdminUser:
    def __init__(self,user_id,role="admin"):
        self.user_id=user_id
        self.role=role

def override_get_current_user():
    return FakeUser(user_id=uuid4(),role="admin")

def override_get_admin_user():
    return FakeAdminUser(user_id=uuid4(),role="admin")
async def checkUser():
    return FAKE_USER_RESPONSE
FAKE_USER_RESPONSE={ 
    "id":str(uuid4()),
    "fname":"Vivek",
    "lname":"Singh",
    "dob":"2003-10-23",
    "email":"1234@gmail.com",
    "phone":"123456789",
    "hashed_password":"hashedpwd",
    "isAdmin":True,
    "is_active":True 
}

app.dependency_overrides[get_current_user]=override_get_current_user
app.dependency_overrides[check_admin_route]=override_get_admin_user
async def fake_get(user):
    return FAKE_USER_RESPONSE
async def fake_create(db,user):
    return {
    "id":str(uuid4()),
    "fname":"Vivek",
    "lname":"Singh",
    "dob":"2003-10-23",
    "email":"1234@gmail.com",
    "phone":"123456789",
    "is_active":True,
    "access_token": "str",
    "token_type":"bearer"
    }
async def fake_is_admin(user):
    return {
    "id": uuid4(),
    "email": "123@gmail.com",
    "fname":"Vivek",
    "lname":"Singh",
    "dob":"2003-10-23",
    "phone":"123456789",
    "isAdmin":True,
    "is_active": True
    }
async def fake_getAllUsers(user,db):
    return [ {
    "id": uuid4(),
    "email": "123@gmail.com",
    "fname":"Vivek",
    "lname":"Singh",
    "dob":"2003-10-23",
    "phone":"123456789",
    "isAdmin":True,
    "is_active": True
    }
    ]

async def fake_UpdateUser(db, update_data, current_user,background_tasks):
    FAKE_USER_RESPONSE["fname"]="Vivekkkk"
    return FAKE_USER_RESPONSE
async def fake_Update_User_By_Admin(db, update_data, current_user,background_tasks):
    FAKE_USER_RESPONSE["fname"]="Vivek"
    FAKE_USER_RESPONSE["email"]="viveksingh1234@gmail.com"
    return FAKE_USER_RESPONSE
def test_get_user(monkeypatch):
    monkeypatch.setattr("app.api.routes.getauser",fake_get)
    response=client.get('/users/me')
    assert response.status_code==200
    assert response.json()["fname"]=="Vivek"
def test_create_user(monkeypatch):
    monkeypatch.setattr("app.api.routes.create_user",fake_create)
    payload={
    "fname":"Vivek",
    "lname":"Singh",
    "dob":"2003-10-23",
    "email":"1234@gmail.com",
    "phone":"123456789",
    "password":"hashedpwd",
    "isAdmin":True
    }
    response=client.post('/users/',json=payload)
    assert response.status_code==200
    assert response.json()["fname"]=="Vivek"
def test_isAdmin_success(monkeypatch):
    monkeypatch.setattr("app.api.routes.is_admin",fake_is_admin)
    response=client.get('/users/isAdmin/')
    assert response.status_code==200
    assert response.json()["isAdmin"]==True
def test_get_All(monkeypatch):
    monkeypatch.setattr("app.api.routes.getAllUsers",fake_getAllUsers)
    response=client.get('/users/all/')
    assert response.status_code==200
    assert response.json()[0]["fname"]=="Vivek"
def test_update_User(monkeypatch):
    monkeypatch.setattr("app.api.routes.update_user_service",fake_UpdateUser)
    payload={
        "fname":"Vivekkkk",
        "lname":"Singh"
    }
    response=client.put('/users/update',json=payload)
    assert response.status_code==200
    assert response.json()["fname"]=="Vivekkkk"
def test_update_Admin_success(monkeypatch):
    monkeypatch.setattr("app.api.routes.update_user_by_admin",fake_Update_User_By_Admin)
    payload={
        "id":str(uuid4()),
        "email":"viveksingh1234@gmail.com"
    }
    response=client.put('/users/adminUpdate',json=payload)
    assert response.status_code==200
    assert response.json()["fname"]=="Vivek"

def test_update_Admin_failure(monkeypatch):
    monkeypatch.setattr("app.api.routes.update_user_by_admin",fake_Update_User_By_Admin)
    payload={
        # "id":str(uuid4()),
        "email":"viveksingh1234@gmail.com"
    }
    response=client.put('/users/adminUpdate',json=payload)
    assert response.status_code==422