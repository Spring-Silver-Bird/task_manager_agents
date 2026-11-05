.PHONY: setup install migrate collectstatic build render-start tailwind-build tests

setup:
	make install
	uv run python manage.py migrate

install:
	uv sync --dev

migrate:
	uv run python manage.py migrate

collectstatic: tailwind-build
	uv run python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi

tailwind-build:
	uv run python manage.py tailwind build

lint:
	uv run ruff check .
	uv run ruff format --check .

tests:
	uv run pytest --cov --cov-report=term --cov-fail-under=80