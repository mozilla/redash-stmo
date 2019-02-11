.PHONY: build clean release sdist test wheel

clean:
	rm -rf build/ dist/

sdist:
	python setup.py sdist

wheel:
	python setup.py bdist_wheel

build: clean sdist wheel

release: build
	twine upload -s dist/*

test:
	docker-compose build --pull
	docker-compose up -d
	docker-compose run --rm server sh -c "/redash-stmo/bin/wait-for-it.sh postgres:5432 -- python /app/manage.py database create_tables"
	docker-compose run --rm postgres psql -h postgres -U postgres -c "create database tests;" || echo "Test database exists already."
	docker-compose run --rm $(CI_ENV) server tests
	docker-compose down
