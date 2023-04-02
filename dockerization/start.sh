#!/bin/sh
# wait for db
sleep 3

echo "migrate..."
alembic -c src/alembic.ini upgrade head
echo "start app..."
gunicorn --chdir src -k uvicorn.workers.UvicornWorker -w 1 -b 0.0.0.0:8000 src.main:app
