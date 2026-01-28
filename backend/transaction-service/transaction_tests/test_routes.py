import pytest
from uuid import uuid4
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.schemas.schemas import TransactionResponse

pytestmark = pytest.mark.asyncio

async def test_create_transaction_success(mocker, override_user):
    override_user(role="user")
    mocker.patch(
        "app.api.routes.createTransaction",
        return_value={
            "id": str(uuid4()),
            "user_id": str(uuid4()),
            "sender_acc": "ACC123",
            "receiver_acc": "ACC456",
            "amount": 100,
            "description": "test transfer",
            "type": "transfer",
            "isSuccess": True,
            "onRevert": False,
            "timestamp": "2025-01-01T00:00:00",
        },
    )

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/transactions/",
            json={
                "receiver_acc": "ACC456",
                "amount": 100,
                "description": "test transfer",
            },
            headers={"Authorization": "Bearer faketoken"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["isSuccess"] is True
    assert body["amount"] == 100
async def test_fetch_all_transactions_forbidden(override_user):
    override_user(role="user")

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/transactions/all",
            headers={"Authorization": "Bearer faketoken"},
        )

    assert response.status_code == 403

async def test_fetch_all_transactions_admin(mocker, override_user):
    override_user(role="admin")

    mocker.patch(
        "app.api.routes.getAllTransactions",
        return_value=[],
    )

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/transactions/all",
            headers={"Authorization": "Bearer faketoken"},
        )

    assert response.status_code == 200
    assert response.json() == []
