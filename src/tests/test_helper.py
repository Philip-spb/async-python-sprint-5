from typing import Optional

import pytest

from services.helpers import parse_path, is_uuid

parametrize_parse_path_list = [
    ('/test/folder/', 'test/folder', None),
    ('/test/folder', 'test', 'folder'),
    ('test/folder/', 'test/folder', None),
    ('test', 'test', None),
    ('/test1/folder2/file', 'test1/folder2', 'file'),
    ('/test1/folder2/folder3/', 'test1/folder2/folder3', None),
    ('test1/folder2/folder3/', 'test1/folder2/folder3', None),
    ('test1/folder2/file', 'test1/folder2', 'file'),
]


@pytest.mark.parametrize('init_path, path, filename', parametrize_parse_path_list)
def test_parse_path(init_path: str, path: str, filename: Optional[str]):
    assert parse_path(init_path) == (path, filename)


parametrize_is_uuid_list = [
    ('682adaf8-48b2-4088-a09d-226d74090043', True),
    ('682adaf848b24088a09d226d74090043123', False),
    ('TEST2', False),
]


@pytest.mark.parametrize('path, is_valid', parametrize_is_uuid_list)
def test_is_uuid(path: str, is_valid: bool):
    assert is_uuid(path) == is_valid
