import json

from fastapi import status

from main import app


async def test_create_user(event_loop, client):
    user_data = {
        'email': 'homer@simpson.com',
        'password': 'springfield',
    }

    response = await client.post(app.url_path_for('register:register'), json=user_data)
    assert response.status_code == status.HTTP_201_CREATED


async def test_upload_file(event_loop, client, monkeypatch):
    def mock_send_file(path, file_data):
        ...

    monkeypatch.setattr('api.files.send_file_to_s3', mock_send_file)

    user_data = {
        'username': 'homer@simpson.com',
        'password': 'springfield',
    }
    response = await client.post(app.url_path_for('auth:jwt.login'), data=user_data)
    token = json.loads(response.content)['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    files = {'file': b'123123123'}
    data = {'path': 'test/new_file.txt'}

    response = await client.post(
        app.url_path_for('upload'),
        headers=headers,
        files=files,
        data=data
    )
    assert response.status_code == status.HTTP_201_CREATED


async def test_download_file(event_loop, client, monkeypatch):
    user_data = {
        'username': 'homer@simpson.com',
        'password': 'springfield',
    }
    response = await client.post(app.url_path_for('auth:jwt.login'), data=user_data)
    token = json.loads(response.content)['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    data = {'path': 'test/new_file.txt'}

    response = await client.get(
        app.url_path_for('download'),
        headers=headers,
        params=data
    )

    assert response.status_code == status.HTTP_200_OK


async def test_get_file_list(event_loop, client):
    user_data = {
        'username': 'homer@simpson.com',
        'password': 'springfield',
    }
    response = await client.post(app.url_path_for('auth:jwt.login'), data=user_data)
    token = json.loads(response.content)['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    response = await client.get(app.url_path_for('user_files'), headers=headers)

    assert response.status_code == status.HTTP_200_OK
