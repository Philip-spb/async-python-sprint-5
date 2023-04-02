runserver:
	docker-compose up

runlocal:
	docker-compose up -d filipp_sprint_5_db
	uvicorn --app-dir src main:app

test:
	docker-compose build
	docker-compose run --rm filipp_sprint_5_api pytest -s

pep8:
	docker-compose build
	docker-compose run --rm filipp_sprint_5_api flake8

migrate:
	docker-compose build
	docker-compose run --rm filipp_sprint_5_api alembic -c src/alembic.ini upgrade head

rollback_migrations:
	docker-compose build
	docker-compose run --rm filipp_sprint_5_api alembic -c src/alembic.ini downgrade -1
