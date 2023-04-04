runserver:
	docker-compose up

runlocal:
	docker-compose up -d filipp_sprint_5_db
	uvicorn --app-dir src main:app --reload
	#gunicorn --reload --chdir src -k uvicorn.workers.UvicornWorker -w 1 -b 0.0.0.0:8000 src.main:app

test:
	docker-compose run --rm filipp_sprint_5_api pytest

pep8:
	docker-compose run --rm filipp_sprint_5_api flake8

migrate:
	docker-compose run --rm filipp_sprint_5_api alembic -c src/alembic.ini upgrade head

rollback_migrations:
	docker-compose run --rm filipp_sprint_5_api alembic -c src/alembic.ini downgrade -1
