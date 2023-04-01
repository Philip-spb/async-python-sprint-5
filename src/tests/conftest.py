import asyncio

import pytest
from alembic.config import Config
from alembic.command import upgrade, downgrade

from httpx import AsyncClient

from db.db import engine
from main import app


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
def test_db_engine(event_loop):
    config = Config()
    config.set_main_option('script_location', 'src/migrations')

    upgrade(config, 'head')
    yield engine
    downgrade(config, 'base')


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
