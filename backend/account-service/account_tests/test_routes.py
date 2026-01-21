import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import date
from app.main import app
from app.db.db import get_db
from app.utils.security import get_current_user, get_admin_user
from app.api.routes import checkUser

client = TestClient(app)
class FakeUser:
    def __init__(self, user_id, role="user"):
        self.user_id = user_id
        self.role = role
          
def override_get_current_user():
    return FakeUser(user_id=uuid4(), role="user")

def override_get_admin_user():
    return FakeUser(user_id=uuid4(), role="admin")
async def fake_checkUser():
    return FAKE_ACCOUNT_RESPONSE
def override_get_db():
    return "fake-db-session"

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_admin_user] = override_get_admin_user
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[checkUser] = fake_checkUser

FAKE_ACCOUNT_RESPONSE = {
    "id": str(uuid4()),
    "user_id": str(uuid4()),
    "acc_no": "ACC123456",
    "name": "Vivek Singh",
    "age": 24,
    "phone": "9999999999",
    "email": "vivek@test.com",
    "dob": "2000-01-01",
    "pin": "hashed-pin",
    "amount": 5000,
    "other_charges": 0,
    "opening_date": str(date.today()),
    "ifsc_code": "SBIN0000123",
    "isDigital": True,
    "pan_no": "ABCDE1234F",
    "aadhar_no": "123412341234",
    "type": "saving",
    "isActive": True
}

async def fake_createAccount(account, user_id, db):
    return FAKE_ACCOUNT_RESPONSE

async def fake_get(user_id, db):
    return FAKE_ACCOUNT_RESPONSE

async def fake_getAc(user_id, db):
    return {
        "user_id": str(user_id),
        "acc_no": "ACC123456"
    }

async def fake_login(account, user_id, db):
    return FAKE_ACCOUNT_RESPONSE



async def fake_update(account, db_account, db):
    updated = FAKE_ACCOUNT_RESPONSE.copy()
    updated["name"] = "Updated Name"
    return updated

async def fake_updatebyadmin(account, user_id, db):
    updated = FAKE_ACCOUNT_RESPONSE.copy()
    updated["amount"] = 10000
    return updated

def test_create_account(monkeypatch):
    monkeypatch.setattr("app.api.routes.createAccount", fake_createAccount)

    payload = {
        "acc_no": "ACC123456",
        "name": "Vivek Singh",
        "phone": "9999999999",
        "email": "vivek@test.com",
        "dob": "2000-01-01",
        "pin": "1234",
        "amount": 5000,
        "ifsc_code": "SBIN0000123",
        "isDigital": True,
        "pan_no": "ABCDE1234F",
        "aadhar_no": "123412341234",
        "type": "saving"
    }

    response = client.post("/accounts/", json=payload)

    assert response.status_code == 200
    assert response.json()["acc_no"] == "ACC123456"


def test_get_account(monkeypatch):
    monkeypatch.setattr("app.api.routes.get", fake_get)

    response = client.get("/accounts/")

    assert response.status_code == 200
    assert response.json()["name"] == "Vivek Singh"


def test_get_account_number(monkeypatch):
    monkeypatch.setattr("app.api.routes.getAc", fake_getAc)

    response = client.get("/accounts/accno")

    assert response.status_code == 200
    assert response.json()["acc_no"] == "ACC123456"


def test_account_login(monkeypatch):
    monkeypatch.setattr("app.api.routes.login", fake_login)

    payload = {
        "email": "vivek@test.com",
        "pin": "1234"
    }

    response = client.post("/accounts/login", json=payload)

    assert response.status_code == 200
    assert response.json()["email"] == "vivek@test.com"


def test_update_account_by_user(monkeypatch):
    from app.api.routes import checkUser
    async def fake_checkUser():
        return FAKE_ACCOUNT_RESPONSE
    app.dependency_overrides[checkUser] = fake_checkUser
    monkeypatch.setattr("app.api.routes.update", fake_update)
    payload = {
        "name": "Updated Name"
    }
    response = client.put("/accounts/update", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"
    app.dependency_overrides.pop(checkUser, None)


def test_update_account_by_admin(monkeypatch):
    monkeypatch.setattr("app.api.routes.updatebyadmin", fake_updatebyadmin)

    payload = {
        "amount": 10000
    }

    response = client.put("/accounts/admin", json=payload)
    assert response.status_code == 200
    assert response.json()["amount"] == 10000