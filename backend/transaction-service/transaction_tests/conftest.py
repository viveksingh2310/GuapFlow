import sys
import os
import pytest
import asyncio
import pytest_asyncio
from uuid import uuid4
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)
from app.db.db import Base
from app.main import app
from app.schemas.schemas import CurrentUser
from app.utils.security import get_current_user


DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture
async def async_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def override_user():
   
    def _override(role: str = "user"):
        async def fake_get_current_user():
            return CurrentUser(
                user_id=uuid4(),
                role=role,
            )

        app.dependency_overrides[get_current_user] = fake_get_current_user

    return _override

@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    app.dependency_overrides.clear()

@pytest.fixture(scope="session", autouse=True)
def shutdown_engine():
    yield
    import asyncio
    asyncio.run(engine.dispose())
