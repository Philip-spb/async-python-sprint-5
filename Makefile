runserver:
	docker-compose up -d filipp_sprint_5_api nginx

run_db:
	docker-compose up -d filipp_sprint_5_db

runlocal:
	uvicorn --app-dir src main:app

test:
	docker-compose up filipp_sprint_5_api_test
	docker-compose stop filipp_sprint_5_api_test

pep8:
	docker-compose up filipp_sprint_5_api_pep8
	docker-compose stop filipp_sprint_5_api_pep8

migrate:
	alembic -c src/alembic.ini upgrade head

rollback_migrations:
	alembic -c src/alembic.ini downgrade -1
