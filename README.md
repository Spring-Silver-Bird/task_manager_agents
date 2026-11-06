## Task manager (Python)
[![Actions Status](https://github.com/Spring-Silver-Bird/python-django-development-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Spring-Silver-Bird/python-django-development-project-52/actions)
[![my-check](https://github.com/Spring-Silver-Bird/python-django-development-project-52/actions/workflows/my_check.yml/badge.svg)](https://github.com/Spring-Silver-Bird/python-django-development-project-52/actions/workflows/my_check.yml)
---

## Deploy is available [here](https://task-manager-is4e.onrender.com)

Features:
- User registration, login, and profile management
- CRUD for tasks, statuses, and labels
- Task filtering by status, executor, label, and author
- Protection: only authors can delete their tasks
- Error tracking via Sentry (Bugsink)
- Responsive UI with Tailwind CSS

---

## Stack

- **Python** 3.12+
- **Django** 6.1 — ORM, template engine, forms, authentication and authorization
- **PostgreSQL** — in production
- **SQLite** — for local development
- **django-filter** — task list filtering
- **Tailwind CSS** — django-tailwind-cli
- **Whitenoise** — static files serving
- **Gunicorn** — WSGI server
- **Render.com** — PaaS for deployment
- **python-dotenv** — environment variables management
- **uv** — package manager

---

## Installation

### Requirements
- Python 3.12 or higher
- uv (package manager)

### Cloning a repository

## Installation and Launch

```bash
git clone https://github.com/Spring-Silver-Bird/python-django-development-project-52.git
cd python-project-52
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
cp .env.example .env
# заполните .env: SECRET_KEY, DATABASE_URL и при необходимости DJANGO_SUPERUSER_*
make setup
make tailwind-build
make superuser
uv run python manage.py runserver
```

---

## API contract

TypeSpec-контракт web UI и будущего JSON API `/api/v1` находится в [`contract/`](contract/README.md).

Требуется Node.js >= 22.

```bash
make contract-install
make contract-build
make contract-check
```

Сгенерированные OpenAPI-файлы:

- `contract/tsp-output/openapi/web.yaml`
- `contract/tsp-output/openapi/api.yaml`
