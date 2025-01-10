import json
import os
from fastapi import HTTPException
from urllib.request import Request
from authx import AuthX,AuthXConfig
from fastapi import FastAPI
from fastapi.openapi.utils import status_code_ranges
from fastapi.params import Depends
from sqlalchemy import select
from starlette.responses import HTMLResponse, FileResponse, Response
from dependencies import SessionDep
from loger_config import service_logger as logger
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from models import TodoORM
from database import setup_database, engine
from router import router

from schemas import STaskADD, UserLoginSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    print('БД готова')
    yield
    print('Выключение')



app = FastAPI(lifespan=lifespan,swagger_ui_parameters={"swagger_ui_css": "/static/swagger.css"})
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)



config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_token"
config.JWT_TOKEN_LOCATION = ['cookies']
security = AuthX(config=config)


IMAGE_PATH = os.path.join(os.getcwd(), "static", "example.jpg")



@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_ip = request.client.host if request.client else "Unknown"
    logger.info(f"Request to {request.url} - Method: {request.method} - Client IP: {client_ip}")

    query_params = dict(request.query_params)
    if query_params:
        logger.debug(f"Query Params: {query_params}")

    body = await request.body()
    if body:
        try:
            parsed_body = json.loads(body.decode("utf-8"))
            logger.debug(f"Request Body: {json.dumps(parsed_body, indent=2)}")
        except json.JSONDecodeError:
            logger.debug(f"Request Body (raw): {body.decode('utf-8')}")

    response = await call_next(request)
    logger.info(f"Response: {response.status_code} for {request.method} {request.url}")
    return response



@app.get("/", response_class=HTMLResponse)
async def read_main():
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome</title>
        <style>
            .image-container {{
                position: relative;
                text-align: center;
                color: white;
                font-family: Arial, sans-serif;
            }}
            .centered-text {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 2em;
                font-weight: bold;
                background-color: rgba(0, 0, 0, 0.5); /* Полупрозрачный фон для выделения текста */
                padding: 10px 20px;
                border-radius: 10px;
            }}
            .docs-link {{
                position: absolute;
                top: 60%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 1.2em;
                color: #ffffff;
                text-decoration: none;
                background-color: rgba(0, 0, 0, 0.5);
                padding: 8px 15px;
                border-radius: 5px;
            }}
            .docs-link:hover {{
                background-color: rgba(0, 0, 0, 0.8);
            }}
        </style>
    </head>
    <body>
        <h1>Welcome Page</h1>
        <div class="image-container">
            <img src="/image" alt="Example Image" style="max-width: 100%; height: auto;">
            <div class="centered-text">Hello User</div>
            <a href="/docs" target="_blank" class="docs-link">Перейти к документации FastAPI</a>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)

@app.get("/image")
async def get_image():
    if not os.path.exists(IMAGE_PATH):
        return {"error": "Image not found!"}
    return FileResponse(IMAGE_PATH)


@app.post('/login')
def login(credentials: UserLoginSchema, responce: Response):
    if credentials.username == 'test' and credentials.password == 'test':
        token = security.create_access_token(uid='1111')
        responce.set_cookie(config.JWT_ACCESS_COOKIE_NAME,token)
        return {'access_token': token}
    raise HTTPException(status_code=401, detail='Incorrect username or password')

@app.get('/protected',dependencies=[Depends(security.access_token_required)])
def protected():
    return {'data':'Secret'}



