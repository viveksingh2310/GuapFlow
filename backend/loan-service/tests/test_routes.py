import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from app.main import app
from app.schemas.schemas import LoanResponseSchema
from app.db.db import get_db
from app.utils.security import get_admin_user,get_current_user,get_token
client=TestClient(app)
class FakeUser:
    def __init__(self,user_id,role="user"):
        self.user_id=user_id
        self.role=role

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

def override_get_current_user():
    return FakeUser(user_id=uuid4(),role="user")
def override_get_db():
    return "fake-db-session"
def override_get_admin_user():
    return FakeUser(user_id=uuid4(),role="admin")
def override_get_token():
    return "Bearer token-authentication"
FAKE_SECURED_LOAN_RESPONSE={
  "id": str(uuid4()),
  "user_id":str(uuid4()),
  "acc_no": "ACC123456789",
  "name": "Vivek Singh",
  "issue_date": "2025-01-10",
  "loan_type": "secured",
  "time": 60,
  "consultant_name": "Rohit Sharma",
  "status": "approved",
  "scheme_name": "Home Loan Scheme A",
  "collateral_type": "Property",
  "collateral_value": 8500000.0,
  "assessed_value": 8000000.0,
  "files": [
    "property_deed.pdf",
    "valuation_report.pdf"
  ]
}
FAKE_UNSECURED_LOAN_RESPONSE={
  "id": str(uuid4()),
  "user_id":str(uuid4()),
  "acc_no": "ACC987654321",
  "name": "Vivek Singh",
  "issue_date": "2025-01-12",
  "loan_type": "unsecured",
  "time": 36,
  "consultant_name": "Anjali Verma",
  "status": "pending",
  "credit_score": 750,
  "monthly_income": 85000.0,
  "emp_type": "salaried",
  "emp_proof": [
    "salary_slip_jan.pdf",
    "bank_statement.pdf"
  ],
  "employer_name": "ABC Technologies Pvt Ltd"
}
app.dependency_overrides[get_current_user]=override_get_current_user
app.dependency_overrides[get_admin_user]=override_get_admin_user
app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_token]=override_get_token
async def fake_CreateLoan(loan,user_id,db=override_get_db(),token=override_get_token()):
    return FAKE_SECURED_LOAN_RESPONSE

async def fake_getLoan(user_id,db=override_get_db()):
    return FAKE_SECURED_LOAN_RESPONSE

async def fake_get_Admin(user_id=override_get_admin_user().user_id,db=override_get_db()):
    return FAKE_UNSECURED_LOAN_RESPONSE
async def fake_updateByUser(new_loan,loan,db=override_get_db()):
    return FAKE_SECURED_LOAN_RESPONSE
def test_create_loan(monkeypatch):
    monkeypatch.setattr("app.api.routes.createLoan",fake_CreateLoan)
    payload = {
        "name": "Vivek Singh",
        "issue_date": "2025-01-10",
        "loan_type": "secured",
        "time": 60,
        "consultant_name": "Rohit Sharma",
        "status": "approved",
        "scheme_name": "Home Loan Scheme A",
        "collateral_type": "Property",
        "collateral_value": 8500000.0,
        "assessed_value": 8000000.0,
        "files": [
            "property_deed.pdf",
            "valuation_report.pdf"
        ]
}
    response=client.post('/loans/',json=payload)
    assert response.status_code==200
    assert response.json().get("name")=="Vivek Singh"

def test_get_loan(monkeypatch):
    monkeypatch.setattr("app.api.routes.get",fake_getLoan)
    result=client.get('/loans/')
    assert result.status_code==200
    assert result.json().get("name")=="Vivek Singh"

def test_get_loan_by_admin(monkeypatch):
    monkeypatch.setattr("app.api.routes.get",fake_get_Admin)
    result=client.get('/loans/admin')
    assert result.status_code==200
    assert result.json().get("loan_type")=="unsecured"
    assert result.json().get("name")=="Vivek Singh"

def test_update_by_user(monkeypatch):
    from app.api.routes import getLoan
    def fake_getLoan():
        return FAKE_SECURED_LOAN_RESPONSE  # dict is OK here
    async def fake_updateByUser(new_loan, loan, db):
        loan["collateral_type"] = new_loan.collateral_type
        loan["collateral_value"] = new_loan.collateral_value
        return loan
    app.dependency_overrides[getLoan] = fake_getLoan
    monkeypatch.setattr(
        "app.api.routes.updateByUser",
        fake_updateByUser
    )
    payload = {
        "collateral_type": "Property with flats",
        "collateral_value": 45900.35
    }
    result = client.patch("/loans/", json=payload)
    assert result.status_code == 200
    assert result.json()["collateral_type"] == "Property with flats"

def test_update_by_admin_user(monkeypatch):
    from app.api.routes import getAdminLoan
    def fake_getAdminLoan():
        return FAKE_SECURED_LOAN_RESPONSE 
    async def fake_updateByAdmin(new_loan, loan, db):
        loan["scheme_name"] = new_loan.scheme_name
        loan["assessed_value"] = new_loan.assessed_value
        return loan
    app.dependency_overrides[getAdminLoan] = fake_getAdminLoan
    monkeypatch.setattr(
        "app.api.routes.adminUpdate",
        fake_updateByAdmin
    )
    payload = {
        "scheme_name": "Scheme 1",
        "assessed_value": 45900.35
    }
    result = client.patch("/loans/admin", json=payload)
    assert result.status_code == 200
    assert result.json()["scheme_name"] == "Scheme 1"