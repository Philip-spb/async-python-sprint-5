import json

from fastapi import status
from httpx import AsyncClient

from main import app


async def test_create_user(event_loop):
    user_data = {
        'email': 'homer@simpson.com',
        'password': 'springfield',
    }
    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.post(app.url_path_for('register:register'), json=user_data)
        assert response.status_code == status.HTTP_201_CREATED


async def test_get_file_list(event_loop):
    async with AsyncClient(app=app, base_url='http://test') as ac:
        user_data = {
            'username': 'homer@simpson.com',
            'password': 'springfield',
        }
        response = await ac.post(app.url_path_for('auth:jwt.login'), data=user_data)
        token = json.loads(response.content)['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = await ac.get(app.url_path_for('user_files'), headers=headers)
        assert response.status_code == status.HTTP_200_OK
