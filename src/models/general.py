from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String, ForeignKey, func
from fastapi_users_db_sqlalchemy.generics import GUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from sqlalchemy.orm import relationship, mapped_column, Mapped

from db.db import Base, get_async_session


class User(SQLAlchemyBaseUserTableUUID, Base):
    personal_files = relationship('PersonalFile', back_populates='owner', lazy=False,
                                  passive_deletes=True)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class PersonalFile(Base):
    __tablename__ = 'personal_file'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    owner_id: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE', name='owner_id_constraint')
    )
    owner: Mapped[Optional[User]] = relationship(User, back_populates='personal_files', lazy=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    path: Mapped[str] = mapped_column(String(4096), nullable=False, name='Folder path')
    size: Mapped[int] = mapped_column()
    is_downloadable: Mapped[bool] = mapped_column(server_default='True')
    create_at: Mapped[datetime] = mapped_column(server_default=func.now())
