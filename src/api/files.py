import logging
from typing import Any, Optional
from botocore.exceptions import ClientError

from fastapi import APIRouter, UploadFile, File, status, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from db.db import get_async_session
from models.general import User
from core.config import app_settings, s3
from schemas.personal_file import ShortLinkToDBBase, ShortLinkInDBBase, UserFile
from services.crud import personal_file_crud
from services.helpers import parse_path, is_uuid
from services.users import current_active_user

logger = logging.getLogger()
files_router = APIRouter()


@files_router.get('/download',
                  status_code=status.HTTP_200_OK,
                  tags=['files']
                  )
async def download(
        *,
        db: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user),
        path: str
) -> Any:
    if is_uuid(path):
        personal_file = await personal_file_crud.get(db=db, id=path, owner_id=user.id)
        if not personal_file:
            return None
        else:
            file_path = f'{user.id}/'
            if personal_file.path:
                file_path = f'{file_path}{personal_file.path}/'

            file_path = f'{file_path}{personal_file.name}'
    else:
        file_path = f'{user.id}/{path}'

    if not app_settings.is_test:
        try:
            obj = s3.get_object(Bucket=app_settings.aws_bucket_name, Key=file_path)
        except ClientError:
            logger.info(f'Can\'t find file: {file_path}')
            return None

    response = StreamingResponse(obj['Body'], media_type=obj["ContentType"])
    response.headers["Content-Disposition"] = f"attachment; filename={file_path}"
    return response


@files_router.post('/upload',
                   response_model=Optional[ShortLinkInDBBase],
                   status_code=status.HTTP_201_CREATED,
                   tags=['files']
                   )
async def upload(
        *,
        db: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user),
        file: UploadFile = File(),
        path: str = Form()
) -> Any:
    real_path, filename = parse_path(path)

    if not filename:
        filename = file.filename

    file_path = f'{user.id}/{real_path}/{filename}'

    personal_file = await personal_file_crud.get(
        db=db, name=filename,
        path=real_path,
        owner_id=user.id
    )

    new_file = ShortLinkToDBBase(
        name=filename,
        path=real_path,
        size=file.size,
        owner_id=user.id
    )

    if not personal_file:
        personal_file = await personal_file_crud.create(db=db, obj_in=new_file)

    if not app_settings.is_test:
        s3.put_object(Bucket=app_settings.aws_bucket_name, Key=file_path, Body=file.file)

    logger.info(f'File {file_path} uploaded')

    await personal_file_crud.update(db=db, db_obj=personal_file, obj_in=new_file)

    return personal_file


@files_router.get('',
                  response_model=UserFile,
                  status_code=status.HTTP_200_OK,
                  tags=['files']
                  )
async def user_files(
        db: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user),
) -> Any:
    files = await personal_file_crud.get_multi(db=db, owner_id=user.id)

    user_files_data = UserFile(
        account_id=user.id,
        files=files
    )

    return user_files_data
