import os
from fastapi.responses import FileResponse
from crud import get_all_tasks
from dependencies import SessionDep


async def make_tasks_report(session: SessionDep):
    """
    Позволяет скачать сгенерированный отчет с задачами.
    Записывает задачи в текстовый файл.
    """
    tasks = await get_all_tasks(session)

    # Создание текстового файла для отчета
    filename = "tasks_report.txt"

    # Запись задач в файл
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("ID\tTitle\tDescription\n")
            for task in tasks:
                f.write(f"{task.id}\t{task.title}\t{task.description if task.description else ''}\n")

        # Отправляем файл пользователю для скачивания
        return FileResponse(path=filename, media_type='text/plain', filename=filename)

    except Exception as e:
        return {"error": f"Ошибка при создании файла: {str(e)}"}
