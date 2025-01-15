import tempfile

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from starlette.testclient import TestClient

from main import app
from models import TodoORM

DATABASE_URL = f"sqlite+aiosqlite:///{tempfile.mktemp()}"
engine = create_async_engine(DATABASE_URL, echo=True)


new_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def setup_database():
    # Настройка тестовой базы данных
    async with engine.begin() as conn:
        await conn.run_sync(TodoORM.metadata.create_all)  # Создаем таблицы


@pytest.fixture
def client():
    return TestClient(app)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    # Настройка тестовой базы данных
    await setup_database()
    async for session in new_session():
        yield session  # Возвращаем сессию для тестов


@pytest.mark.asyncio
async def test_create_task(client: TestClient, db_session: AsyncSession):
    # Тест на создание задачи
    new_task_data = {
        "name": "Test Task",
        "description": "This is a test task."
    }

    response = client.post("/tasks", json=new_task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert "task_id" in data

    task_id = data["task_id"]
    # Проверяем, что задача создана в базе
    result = await db_session.execute(select(TodoORM).filter(TodoORM.id == task_id))
    task = result.scalars().first()
    assert task is not None
    assert task.title == new_task_data["name"]
    assert task.description == new_task_data["description"]

@pytest.mark.asyncio
async def test_get_tasks(client: TestClient, db_session: AsyncSession):
    # Тест на получение всех задач
    task_data_1 = {"name": "Test Task 1", "description": "First test task."}
    task_data_2 = {"name": "Test Task 2", "description": "Second test task."}

    response = client.post("/tasks", json=task_data_1)
    assert response.status_code == 200
    response = client.post("/tasks", json=task_data_2)
    assert response.status_code == 200

    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 2
    assert any(task["title"] == task_data_1["name"] for task in tasks)
    assert any(task["title"] == task_data_2["name"] for task in tasks)

@pytest.mark.asyncio
async def test_update_task(client: TestClient, db_session: AsyncSession):
    # Тест на обновление задачи
    new_task_data = {"name": "Update Task", "description": "Updated description"}
    response = client.post("/tasks", json=new_task_data)
    task_id = response.json()["task_id"]

    updated_data = {"name": "Updated Task", "description": "This is an updated task description."}
    response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    updated_task = response.json()["updated_task"]
    assert updated_task["title"] == updated_data["name"]
    assert updated_task["description"] == updated_data["description"]

@pytest.mark.asyncio
async def test_delete_task(client: TestClient, db_session: AsyncSession):
    # Тест на удаление задачи
    new_task_data = {"name": "Delete Task", "description": "This task will be deleted"}
    response = client.post("/tasks", json=new_task_data)
    task_id = response.json()["task_id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["deleted_task_id"] == task_id

    # Проверяем, что задача удалена
    result = await db_session.execute(select(TodoORM).filter(TodoORM.id == task_id))
    task = result.scalars().first()
    assert task is None



@pytest.mark.asyncio
async def test_create_admin():
    # Подготовка данных администратора
    data = {"username": "test_admin", "password": "secure_password"}

    # Отправка POST-запроса
    response = client.post("/tasks/create_admin", json=data)
    assert response.status_code == 200

    # Проверка ответа
    response_data = response.json()
    assert response_data["ok"] is True
    assert response_data["username"] == "test_admin"
    assert response_data["is_admin"] is True