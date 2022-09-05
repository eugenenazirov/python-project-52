start:
	poetry run python manage.py runserver

gunicorn:
	export DJANGO_SETTINGS_MODULE=task_manager.settings
	poetry run gunicorn task_manager.wsgi

install:
	poetry install

lint:
	poetry run flake8 task_manager

test:
	poetry run python3 manage.py test

test-cov:
	poetry run coverage run manage.py test
	poetry run coverage xml

build:
	poetry build
