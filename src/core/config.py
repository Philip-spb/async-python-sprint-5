import os
from logging import config as logging_config

import boto3
from dotenv import load_dotenv
from pydantic.env_settings import BaseSettings
from pydantic.networks import PostgresDsn

from core.logger import LOGGING

load_dotenv('.env')

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

s3 = boto3.client('s3', endpoint_url='https://storage.yandexcloud.net/')


class AppSettings(BaseSettings):
    project_host: str
    project_port: int
    database_dsn: PostgresDsn
    secret: str

    jwt_lifetime: int = 3600

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str
    aws_bucket_name: str

    class Config:
        env_file = '.env'


app_settings = AppSettings()
