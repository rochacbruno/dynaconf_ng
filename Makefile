SHELL := /bin/bash
.PHONY: install lint test watch

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

all: clean install run-pre-commit lint test

lint:
	flake8 .

test:
	pytest -x -s -vvvv -l --tb=long tests/

watch:
	ls **/**.py | entr -s "make lint test"

install:
	poetry install --no-interaction
	make setup-pre-commit

setup-pre-commit:
	pre-commit install
	pre-commit install-hooks

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
