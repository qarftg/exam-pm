# Makefile для проекта на Python с использованием Poetry

.PHONY: install test lint run

install:
	python -m pip install poetry 
	poetry install --no-root

test:
	poetry run pytest -v

run:
	poetry run python main.py

test-steps:
	poetry run pytest -v tests/test_models.py
	poetry run pytest -v tests/test_database.py
	poetry run pytest -v tests/test_controllers.py

test-step-models:
	poetry run pytest -v tests/test_models.py
	
test-step-database:
	poetry run pytest -v tests/test_database.py
	
test-step-controllers:
	poetry run pytest -v tests/test_controllers.py
	