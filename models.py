from typing import Optional
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped




class Base(DeclarativeBase):
    pass

class TodoORM(Base):
    __tablename__ = 'todo'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())  # Время создания задачи


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    access_token: Mapped[Optional[str]] = mapped_column(nullable=True)

