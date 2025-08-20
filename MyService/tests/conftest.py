import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlmodel import SQLModel
from testcontainers.postgres import PostgresContainer

from .utils import create_random_task
from ..core.db import get_db
from ..core.models import DataBaseHelper
from ..main import app


@pytest_asyncio.fixture(loop_scope="module")
def postgres_container():
    with PostgresContainer("postgres:17-alpine") as postgres:
        postgres.driver = "+asyncpg"  # Правильный драйвер asyncpg
        yield postgres


@pytest_asyncio.fixture(loop_scope="module")
def test_db_helper(postgres_container):
    return DataBaseHelper(url=postgres_container.get_connection_url(), echo=False)


@pytest_asyncio.fixture(loop_scope="module")
async def override_get_db(test_db_helper):
    async def _override():
        async for session in test_db_helper.session_dependency():
            yield session

    return _override


@pytest_asyncio.fixture(loop_scope="module")
async def async_client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(autouse=True)
async def prepare_test_db_per_function(test_db_helper):
    print("Очистка и подготовка базы перед тестом")
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


@pytest_asyncio.fixture(loop_scope="module")
async def create_some_tasks(async_client):
    print("Заполняем задачами")
    tasks = []
    for _ in range(5):
        task_data = await create_random_task()
        response = await async_client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 201
        tasks.append(response.json())
    return tasks


@pytest_asyncio.fixture(loop_scope="module")
async def create_task(async_client):
    task_data = await create_random_task()
    response = await async_client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    yield created_task
