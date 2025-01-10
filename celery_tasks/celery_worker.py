# from celery import Celery
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
