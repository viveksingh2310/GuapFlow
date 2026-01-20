import pytest
from uuid import uuid4
from types import SimpleNamespace
from datetime import date

from app.services.services import (
    createLoan,
    get,
    updateByUser,
    adminUpdate,
)
from app.schemas.schemas import (
    SecuredLoanCreate,
    LoanTypeEnum,
    SecuredLoanUpdate,
    SecuredLoanUpdateAdmin,
)
from app.models.models import LoanType

class FakeResult:
    def __init__(self, scalar=None, row=None):
        self._scalar = scalar
        self._row = row

    def scalars(self):
        return self

    def first(self):
        return self._row

    def scalar_one_or_none(self):
        return self._scalar

    def scalar_one(self):
        if self._row is None:
            raise Exception("No row found")
        return self._row

class FakeAsyncSession:
    def __init__(self, *, scalar=None, row=None):
        self._scalar = scalar
        self._row = row
        self.added = None
        self.committed = False
        self.refreshed = False

    async def execute(self, *_):
        return FakeResult(
            scalar=self._scalar,
            row=self._row
        )

    def add(self, obj):
        self.added = obj

    async def commit(self):
        self.committed = True

    async def refresh(self, obj):
        self.refreshed = True

    async def rollback(self):
        pass
def fakeSecuredLoan():
    return SimpleNamespace(
        id=uuid4(),
        user_id=uuid4(),
        acc_no="SEC-LOAN-10001",
        name="Vivek Singh",
        issue_date=date(2026, 1, 15),
        loan_type=LoanType.secured,
        time=60,
        consultant_name="Rahul Sharma",
        status="approved",
        created_at=date(2026, 1, 15),
        scheme_name="Home Loan Scheme A",
        collateral_type="property",
        collateral_value=8500000.0,
        assessed_value=8000000.0,
        files=[
            "property_deed.pdf",
            "valuation_report.pdf",
        ],
    )
@pytest.mark.asyncio
async def test_create_loan(monkeypatch):
    async def fake_fetch_account_number(token: str):
        return "TEST-ACC-0001"

    monkeypatch.setattr(
        "app.services.services.fetch_account_number",
        fake_fetch_account_number,
    )

    db = FakeAsyncSession(
        scalar=None,  # no existing loan
        row=None
    )

    loan = SecuredLoanCreate(
        name="Vivek Singh",
        issue_date=date(2026, 1, 15),
        loan_type=LoanTypeEnum.secured,
        time=60,
        consultant_name="Rahul Sharma",
        status="approved",
        scheme_name="Home Loan Scheme A",
        collateral_type="property",
        collateral_value=8500000.0,
        assessed_value=8000000.0,
        files=[
            "property_deed.pdf",
            "valuation_report.pdf",
        ],
    )

    user_id = uuid4()
    result = await createLoan(loan, user_id, db, "dummy-token")

    assert db.added is not None
    assert db.committed is True
    assert db.refreshed is True
    assert result.acc_no == "TEST-ACC-0001"
    assert result.name == "Vivek Singh"

@pytest.mark.asyncio
async def test_get_loan():
    secured_loan = fakeSecuredLoan()

    db = FakeAsyncSession(
        scalar=LoanType.secured,   # select(Loan.loan_type)
        row=secured_loan           # select(SecuredLoan)
    )

    result = await get(secured_loan.user_id, db)

    assert result.name == "Vivek Singh"
    assert result.loan_type == LoanTypeEnum.secured
    assert result.scheme_name == "Home Loan Scheme A"

@pytest.mark.asyncio
async def test_update_by_user():
    secured_loan = fakeSecuredLoan()

    db = FakeAsyncSession(
        row=secured_loan
    )

    update_data = SecuredLoanUpdate(
        collateral_type="gold",
        collateral_value=9000000.0,
        files=["updated_doc.pdf"],
    )

    result = await updateByUser(update_data, secured_loan, db)

    assert db.committed is True
    assert db.refreshed is True
    assert result.collateral_type == "gold"
    assert result.collateral_value == 9000000.0

@pytest.mark.asyncio
async def test_admin_update():
    secured_loan = fakeSecuredLoan()

    db = FakeAsyncSession(
        row=secured_loan
    )

    update_data = SecuredLoanUpdateAdmin(
        name="Updated Name",
        assessed_value=8200000.0,
        status="repayed",
    )

    result = await adminUpdate(update_data, secured_loan, db)

    assert db.committed is True
    assert db.refreshed is True
    assert result.name == "Updated Name"
    assert result.assessed_value == 8200000.0
    assert result.status == "repayed"
