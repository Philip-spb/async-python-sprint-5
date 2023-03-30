from typing import Generic, Optional, Type, TypeVar, Union, Dict, Any, List
from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.sql.selectable import Select

from db.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class Repository:

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


def set_params(statement: Select, model: Type[ModelType], params: dict) -> Select:
    for key, value in params.items():
        statement = statement.where(getattr(model, key) == value)

    return statement


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(self, db: AsyncSession, **kwargs) -> Optional[ModelType]:
        statement = select(self._model)
        statement = set_params(statement, self._model, kwargs)

        results = await db.execute(statement=statement)
        return results.unique().scalar_one_or_none()

    async def get_multi(
            self,
            db: AsyncSession,
            **kwargs
    ) -> List[ModelType]:
        statement = select(self._model)
        statement = set_params(statement, self._model, kwargs)

        results = await db.execute(statement=statement)
        return results.unique().scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        stmt = (
            update(self._model).
            where(self._model.id == db_obj.id).
            values(obj_in.dict(exclude_unset=True)).
            returning(self._model)
        )
        await db.execute(stmt)
        await db.commit()

        return db_obj
