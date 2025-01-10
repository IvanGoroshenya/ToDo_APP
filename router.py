from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from schemas import STaskADD
from dependencies import SessionDep
# from celery_tasks.tasks import create_task_async
from fastapi import Request
from crud import create_task, get_all_tasks, update_task, delete_task, get_task_by_id

# from celery_tasks.tasks import create_task_async



router = APIRouter(prefix='/tasks', tags=['Задачи'])
templates = Jinja2Templates(directory="templates")  # Папка с вашими HTML-шаблонами

# uvicorn main:app --reload --host 127.0.0.1 --port 8002


###################################################  БЕЗ CELERY   ##############################################################################
# Создание задачи
@router.post("/")
async def add_task(data: STaskADD, session: SessionDep):
    new_task = await create_task(session, data.name, data.description)
    return {"ok": True, "task_id": new_task.id}

@router.get("/")
async def get_task(request: Request, session: SessionDep):
    tasks = await get_all_tasks(session)
    return templates.TemplateResponse(name = "get_tasks.html",context= {"request": request, "tasks": tasks})
#################################################################################################################################


##############################  SELERY
# @router.post("/")
# async def add_task(data: STaskADD, session: SessionDep):
#     # Отправляем задачу в очередь Celery для фоново обработки
#     task = create_task_async.apply_async(args=[session, data.name, data.description])
#     return {"ok": True, "task_id": task.id}  # Возвращаем ID задачи для отслеживания статуса
#
# # Получение статуса задачи
# @router.get("/status/{task_id}")
# async def get_task_status(task_id: str):
#     # Получаем статус задачи из Celery
#     task_result = AsyncResult(task_id)
#     if task_result.state == 'PENDING':
#         return {"status": "Task is still processing"}
#     if task_result.state == 'SUCCESS':
#         return {"status": "Task completed", "result": task_result.result}
#     if task_result.state == 'FAILURE':
#         return {"status": "Task failed", "error": str(task_result.result)}
#     return {"status": task_result.state}








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

# Удаление задачи
@router.get("/{task_id}")
async def get_task_creation_time(task_id: int, session: SessionDep):
    task = await get_task_by_id(session,task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task.id, "created_at": task.created_at}
