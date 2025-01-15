from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import verify_password
from database import get_session

from typing import Annotated

from models import User

SessionDep = Annotated[AsyncSession, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




async def authenticate_user(db: AsyncSession, username: str, password: str):
    # Используем асинхронный запрос
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()  # Получаем первого пользователя, если он существует

    # Проверка пароля
    if user and verify_password(password, user.hashed_password):
        return user
    return None


