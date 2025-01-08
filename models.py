from typing import Optional

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped




class Base(DeclarativeBase):
    pass

class TodoORM(Base):
    __tablename__ = 'todo'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
