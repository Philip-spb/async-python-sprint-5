from typing import Any

from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_async_session
from schemas.general import PingSchema
from schemas.users import UserRead, UserCreate
from services.users import fastapi_users, auth_backend

api_router = APIRouter()

api_router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=False),
    prefix='',
    tags=['auth'],
)

api_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='',
    tags=['auth'],
)


@api_router.get(
    '/ping',
    response_model=PingSchema,
    status_code=status.HTTP_200_OK,
    tags=['system']
)
async def ping_db(
        *,
        db: AsyncSession = Depends(get_async_session),
) -> Any:
    try:
        db_connection_start = datetime.now()
        statement = select(1)
        await db.execute(statement=statement)
        db_connection_time = (datetime.now() - db_connection_start).microseconds
    except Exception:
        db_connection_time = None

    return {'db': db_connection_time}
