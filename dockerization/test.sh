#!/bin/sh

echo "migrate..."
alembic -c src/alembic.ini upgrade head

echo "pep8"
flake8

echo "test"
pytest
