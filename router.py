from fastapi import APIRouter, HTTPException
from schemas import STaskADD
from dependencies import SessionDep
from crud import create_task, get_all_tasks, update_task, delete_task

router = APIRouter(prefix='/tasks', tags=['Задачи'])

# Создание задачи
@router.post("")
async def add_task(data: STaskADD, session: SessionDep):
    new_task = await create_task(session, data.name, data.description)
    return {"ok": True, "task_id": new_task.id}

# Получение всех задач
@router.get("")
async def get_task(session: SessionDep):
    tasks = await get_all_tasks(session)
    return tasks

# Обновление задачи
@router.put("/{task_id}")
async def put_tasks(task_id: int, data: STaskADD, session: SessionDep):
    task = await update_task(session, task_id, data.name, data.description)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True, "updated_task": {"id": task.id, "title": task.title, "description": task.description}}

# Удаление задачи
@router.delete("/{task_id}")
async def delete_task_route(task_id: int, session: SessionDep):
    deleted_task_id = await delete_task(session, task_id)
    if not deleted_task_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True, "deleted_task_id": deleted_task_id}

