import pytest
from uuid import uuid4
from datetime import date
from types import SimpleNamespace
from fastapi import HTTPException
from app.services.services import (createAccount,login,updateAc,updatebyadmin,get,getAc)
from app.services import services
from app.schemas.schemas import (AccountCreate,AccountLogin,UpdateAccountByUser,UpdateAccountByAdmin)
class FakeResult:
    def __init__(self, obj):
        self._obj = obj

    def scalars(self):
        return self

    def first(self):
        return self._obj

class FakeAsyncSession:
    def __init__(self, result=None):
        self._result = result
        self.added = None # these are the asssumed returned value from mock db
        self.committed = False
        self.refreshed = False

    async def execute(self, *_):
        return FakeResult(self._result)

    def add(self, obj):
        self.added = obj

    async def commit(self):
        self.committed = True

    async def refresh(self, obj):
        self.refreshed = True

def fake_account(user_id=None):
    return SimpleNamespace(
        user_id=user_id,
        acc_no="ACC123",
        name="Vivek",
        age=24,
        phone="9999999999",
        email="vivek@test.com",
        dob=date(2000, 1, 1),
        pin="$argon2id$hashed",
        amount=5000,
        other_charges=0,
        opening_date=date.today(),
        ifsc_code="SBIN0000123",
        isDigital=True,
        pan_no="ABCDE1234F",
        aadhar_no="123412341234",
        type="saving"
    )

@pytest.mark.asyncio
async def test_create_account_success():
    db = FakeAsyncSession(result=None)
    user_id = uuid4()
    account = AccountCreate(
        acc_no="ACC123",
        name="Vivek",
        phone="9999999999",
        email="vivek@test.com",
        dob=date(2000, 1, 1),
        pin="1234",
        amount=5000,
        ifsc_code="SBIN0000123",
        pan_no="ABCDE1234F",
        aadhar_no="123412341234",
        type="saving"
    )

    result = await createAccount(account, user_id, db)

    assert db.added is not None
    assert db.committed is True
    assert db.refreshed is True
    assert result.acc_no == "ACC123"


@pytest.mark.asyncio
async def test_create_account_duplicate():
    db = FakeAsyncSession(result=fake_account())
    user_id = uuid4()
    account = AccountCreate(
        acc_no="ACC123",
        name="Vivek",
        phone="9999999999",
        email="vivek@test.com",
        dob=date(2000, 1, 1),
        pin="1234",
        amount=5000,
        ifsc_code="SBIN0000123",
        pan_no="ABCDE1234F",
        aadhar_no="123412341234",
        type="saving"
    )

    with pytest.raises(HTTPException) as exc:
        await createAccount(account, user_id, db)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_login_success():
    db = FakeAsyncSession(result=fake_account())
    user_id = uuid4()
    account = AccountLogin(
        email="vivek@test.com",
        pin="1234"
    )

    services.pwd_context.verify = lambda *_: True
    result = await login(account, user_id, db)
    assert result.email == "vivek@test.com"
    
@pytest.mark.asyncio
async def test_login_invalid_password():
    db = FakeAsyncSession(result=fake_account())
    user_id = uuid4()

    account = AccountLogin(
        email="vivek@test.com",
        pin="wrong"
    )

    from app.services import services
    services.pwd_context.verify = lambda *_: False

    with pytest.raises(HTTPException) as exc:
        await login(account, user_id, db)

    assert exc.value.status_code == 401

@pytest.mark.asyncio
async def test_update_account_by_user():
    db = FakeAsyncSession()
    db_account = fake_account()

    update_data = UpdateAccountByUser(
        name="Updated Name",
        phone="8888888888"
    )

    result = await updateAc(update_data, db_account, db)

    assert result.name == "Updated Name"
    assert result.phone == "8888888888"
    assert db.committed is True

@pytest.mark.asyncio
async def test_update_by_admin_success():
    db = FakeAsyncSession(result=fake_account(user_id=uuid4()))
    admin_id = uuid4()

    update_data = UpdateAccountByAdmin(
        amount=10000
    )

    result = await updatebyadmin(update_data, admin_id, db)

    assert result.amount == 10000
    assert db.committed is True


@pytest.mark.asyncio
async def test_update_by_admin_unauthorized():
    db = FakeAsyncSession(result=None)

    with pytest.raises(HTTPException):
        await updatebyadmin(UpdateAccountByAdmin(), None, db)


@pytest.mark.asyncio
async def test_get_account_success():
    db = FakeAsyncSession(result=fake_account())
    user_id = uuid4()

    result = await get(user_id, db)

    assert result.acc_no == "ACC123"


@pytest.mark.asyncio
async def test_get_account_not_found():
    db = FakeAsyncSession(result=None)

    with pytest.raises(HTTPException):
        await get(uuid4(), db)


@pytest.mark.asyncio
async def test_get_account_number():
    user_id = uuid4()
    db = FakeAsyncSession(result=fake_account())
    result = await getAc(user_id, db)
    assert result["acc_no"] == "ACC123"
    assert result["user_id"] == user_id