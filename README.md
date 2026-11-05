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

- **Python** 3.14
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
- Python 3.10 or higher
- uv (package manager)

### Cloning a repository

## Installation and Launch

```bash
git clone https://github.com/Spring-Silver-Bird/python-django-development-project-52.git
cd python-project-52
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
make setup
npm install
cp .env.example .env 2>/dev/null || echo "SECRET_KEY=$(uv run python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')\nDEBUG=True\nDATABASE_URL=sqlite:///db.sqlite3" > .env
uv run python manage.py tailwind build
uv run python manage.py migrate
uv run python manage.py createsuperuser
make dev
