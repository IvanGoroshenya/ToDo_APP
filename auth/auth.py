from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_session
from models import User
from typing import Annotated


SessionDep = Annotated[AsyncSession, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Фиктивная функция для декодирования токена
def decode_token(token: str) -> str:
    # Замените на свою логику для декодирования и валидации токена (например, через JWT)
    return token  # Для примера возвращаем токен как имя пользователя

# Получаем текущего пользователя асинхронно
async def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)) -> User:
    username = decode_token(token)
    # Выполняем асинхронный запрос с использованием сессии AsyncSession
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    user = result.scalars().first()  # Извлекаем первого пользователя
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

# Проверка прав администратора
async def admin_required(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
