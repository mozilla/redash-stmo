.PHONY: bash build clean database devserver node_modules test_database test up

bash:
	docker-compose run --rm server bash

build:
	docker-compose build --pull

clean:
	rm -rf build/ dist/

up:
	docker-compose up

node_modules:
	docker-compose run --rm server npm install

database:
	docker-compose run --rm server create_tables

devserver:
	docker-compose run --publish 8080:8080 server webpack_devserver

test_database:
	docker-compose up --no-start
	docker-compose start postgres
	docker-compose run --rm server /extension/bin/wait-for-it.sh postgres:5432 -- echo "Postgres started"
	docker-compose run --rm postgres psql -U postgres -h postgres -c "create database tests;" || echo "Error while creating tests database"
	docker-compose run --rm server create_test_tables

test: build test_database
	docker-compose run --rm server tests
	docker-compose stop
