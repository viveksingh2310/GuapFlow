# tests/test_service.py
import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import UserTransactionDetail, CurrentUser
from app.services.services import createTransaction, getAllTransactions
from app.models.models import Transaction

@pytest.mark.asyncio
async def test_create_transaction_service(mocker, async_session: AsyncSession):
    mocker.patch(
        "app.services.services.validateAccountNumber",
        return_value="ACC456"
    )

    mocker.patch(
        "app.services.services.fetch_account_number",
        return_value="ACC123"
    )

    mocker.patch(
        "app.services.services.executeTransaction",
        return_value={"status": "success"}
    )

    user = CurrentUser(user_id=uuid4(), role="user")
    data = UserTransactionDetail(
        receiver_acc="ACC456",
        amount=100,
        description="unit test"
    )

    tx = await createTransaction(
        trans_details=data,
        user=user,
        token="faketoken",
        db=async_session
    )

    assert tx.sender_acc == "ACC123"
    assert tx.receiver_acc == "ACC456"
    assert tx.amount == 100
    assert tx.isSuccess is True


@pytest.mark.asyncio
async def test_get_all_transactions_admin(mocker, async_session: AsyncSession):
    user = CurrentUser(user_id=uuid4(), role="admin")

    result = await getAllTransactions(user, async_session)
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_get_all_transactions_non_admin(async_session):
    user = CurrentUser(user_id=uuid4(), role="user")

    with pytest.raises(Exception):
        await getAllTransactions(user, async_session)