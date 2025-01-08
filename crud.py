from sqlalchemy.ext.asyncio import AsyncSession
from models import TodoORM
from sqlalchemy.future import select

# Создание задачи
async def create_task(session: AsyncSession, name: str, description: str):
    new_task = TodoORM(title=name, description=description)
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task

# Получение всех задач
async def get_all_tasks(session: AsyncSession):
    query = select(TodoORM)
    result = await session.execute(query)
    return result.scalars().all()

# Получение задачи по ID
async def get_task_by_id(session: AsyncSession, task_id: int):
    query = select(TodoORM).where(TodoORM.id == task_id)
    result = await session.execute(query)
    task = result.scalars().first()
    return task

# Обновление задачи
async def update_task(session: AsyncSession, task_id: int, name: str, description: str):
    task = await get_task_by_id(session, task_id)
    if not task:
        return None  # Можно выбросить исключение
    task.title = name
    task.description = description
    await session.commit()
    await session.refresh(task)
    return task

# Удаление задачи
async def delete_task(session: AsyncSession, task_id: int):
    task = await get_task_by_id(session, task_id)
    if not task:
        return None  # Можно выбросить исключение
    await session.delete(task)
    await session.commit()
    return task_id
