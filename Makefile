SHELL := /bin/bash
.PHONY: help all lint test watch isntall setup-pre-commit clean

help:                    ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

all:                     ## Run everything 
	clean install run-pre-commit lint test

lint:                    ## Lint with flake
	poetry run flake8 .

test:                    ## Run tests 
	poetry run pytest -x -s -vvvv -l --tb=long tests/

watch:                   ## Run tests on file changes
	ls **/**.py | entr -s "make lint test"

install:                 ## Install dependencies
	poetry install --no-interaction

setup-pre-commit:        ## Setup pre-commit hooks
	pre-commit install
	pre-commit install-hooks

run-pre-commit:          ## Run pre-commit hooks
	rm -rf .tox/
	rm -rf build/
	pre-commit run --files $$(find -regex '.*\.\(py\|yaml\|yml\|md\)') -v

clean:                   ## Clean up python artifacts
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
