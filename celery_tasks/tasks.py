# # celery_tasks/tasks.py
#
#
# from crud import create_task
# from celery import Celery
#
#
#
#
# # Настройка брокера сообщений
# app = Celery(
#     'tasks',
#     broker='redis://localhost:6379/0',  # Используем Redis как брокер сообщений
#     backend='redis://localhost:6379/0',  # Где будут храниться результаты выполнения задач
#     include=['tasks']  # Указываем, где искать задачи
# )
#
# # Настроим конфигурацию
# app.conf.update(
#     result_expires=3600,  # Время жизни результатов
# )
#
#
# @app.task
# def create_task_async(session, name, description):
#     # Задача, которая будет выполняться фоново
#     task = create_task(session, name, description)
#     return {"id": task.id, "title": task.title, "description": task.description}
