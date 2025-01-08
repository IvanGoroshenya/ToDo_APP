import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from database import get_session
from main import app
from models import TodoORM

# Используем асинхронный SQLite
DATABASE_URL = 'sqlite+aiosqlite:///task.db'
engine = create_async_engine(DATABASE_URL, echo=True)

# Используем асинхронную сессию для тестов
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession  # Указываем использование AsyncSession
)

client = TestClient(app)

# Асинхронная сессия для тестов
async def override_get_db():
    async with TestingSessionLocal() as db:
        yield db

# Переопределяем зависимость get_db в приложении FastAPI
app.dependency_overrides[get_session] = override_get_db

@pytest.mark.asyncio
async def test_add_task():
    new_task = {
        "name": "Test Task",
        "description": "This is a test task."
    }

    # Отправка POST-запроса для добавления задачи
    response = client.post("/tasks", json=new_task)

    # Проверка успешности добавления задачи
    assert response.status_code == 200
    response_json = response.json()

    # Проверка, что task_id присутствует в ответе
    assert "task_id" in response_json
    assert response_json["ok"] is True

    task_id = response_json["task_id"]

    # Теперь проверим, что задача добавлена и можем получить её через GET-запрос
    response = client.get(f"/tasks/{task_id}")

    # Проверка, что задача существует
    assert response.status_code == 200
    response_json = response.json()

    # Проверка, что данные задачи корректны
    assert response_json["Status"] == "Success"
    assert response_json["Task"]["id"] == task_id
    assert response_json["Task"]["title"] == new_task["name"]
    assert response_json["Task"]["description"] == new_task["description"]


@pytest.mark.asyncio
async def test_update_task():
    new_task = {
        "name": "Test Task",
        "description": "This is a test task."
    }

    # Создаем задачу
    response = client.post("/tasks", json=new_task)
    response_json = response.json()
    task_id = response_json["task_id"]

    # Обновляем задачу
    updated_task = {
        "name": "Updated Task",
        "description": "This is the updated task description."
    }
    response = client.put(f"/tasks/{task_id}", json=updated_task)

    # Проверка успешности обновления
    assert response.status_code == 200
    response_json = response.json()

    # Проверка, что данные задачи обновлены
    assert response_json["Status"] == "Success"
    assert response_json["Task"]["id"] == task_id
    assert response_json["Task"]["title"] == updated_task["name"]
    assert response_json["Task"]["description"] == updated_task["description"]


@pytest.mark.asyncio
async def test_delete_task():
    new_task = {
        "name": "Test Task to Delete",
        "description": "This task will be deleted."
    }

    # Создаем задачу
    response = client.post("/tasks", json=new_task)
    response_json = response.json()
    task_id = response_json["task_id"]

    # Удаляем задачу
    response = client.delete(f"/tasks/{task_id}")

    # Проверка успешности удаления
    assert response.status_code == 200
    response_json = response.json()

    # Проверка, что задача была удалена
    assert response_json["Status"] == "Success"

    # Теперь проверим, что задача действительно удалена
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404  # Ожидаем, что задача не найдена


