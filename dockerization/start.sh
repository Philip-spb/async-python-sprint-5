#!/bin/sh
echo "migrate..."
alembic -c src/alembic.ini upgrade head
echo "start app..."
uvicorn --app-dir src main:app --host 0.0.0.0 --port 8000
