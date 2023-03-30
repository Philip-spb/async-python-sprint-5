from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class PersonalFileBase(BaseModel):
    path: str


class PersonalFileCreate(PersonalFileBase):
    ...


class PersonalFileUpdate(PersonalFileBase):
    ...


class ShortLinkToDBBase(BaseModel):
    name: str
    path: str
    size: int
    is_downloadable: Optional[bool] = True
    owner_id: UUID


class ShortLinkInDBBase(BaseModel):
    id: UUID
    create_at: datetime
    name: str
    path: str
    size: int
    is_downloadable: Optional[bool] = True

    class Config:
        orm_mode = True


class UserFile(BaseModel):
    account_id: UUID
    files: Optional[List[ShortLinkInDBBase]]
