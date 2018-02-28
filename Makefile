.PHONY: build clean release sdist wheel

clean:
	rm -rf build/ dist/

sdist:
	python setup.py sdist

wheel:
	python setup.py bdist_wheel

build: clean sdist wheel

release: build
	twine upload -s dist/*
