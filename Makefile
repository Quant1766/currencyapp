# Project Targets
build:
	make build-docker
	make migrate-python
	#make manage-createsuperuser
	make update_currency-python


build-docker:
	docker-compose build

run:
	docker-compose up

manage-python:
	docker-compose run --rm web python manage.py $(command)

makemigrations-python: command=makemigrations
makemigrations-python: manage-python
mm: makemigrations-python

migrate-python: command=migrate
migrate-python: manage-python

update_currency-python: command=update_currency
update_currency-python: manage-python

manage-createsuperuser: manage-python
csu: manage-createsuperuse

lint:
	docker-compose run --rm web flake8

bash:
	docker-compose run --rm web sh