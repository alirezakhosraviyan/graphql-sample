help:
	@echo 'Available commands:'
	@echo '  make install  - Installs dependencies'
	@echo '  make run      - Runs a development server on localhost:8000'
	@echo '  make test     - Runs the tests'
	@echo '  make check    - Runs all checks'
	@echo '  make fix      - Fixes coding standards problems'
	@echo '  make db-gen   - Create migrations'
	@echo '  make db-head  - Apply migrations'

install:
	poetry install

run:
	source .env && fastapi run

test:
	source .env.test && poetry run pytest

check:
	poetry run ruff check .
	poetry run mypy .

fix:
	poetry run ruff format .
	poetry run ruff check --fix .

db-gen:
	source .env && alembic revision --autogenerate

db-head:
	source .env && alembic upgrade head