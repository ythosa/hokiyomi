.PHONY: build
build:
	FLASK_APP=flask_app.py flask run

.PHONY: deploy
deploy:
	gunicorn flask_app:app

.PHONY: sql
sql:
	C:/sqlite/sqlite3 ./db/data.db < createdb.sql

.PHONY: tokens
tokens:
	git update-index --assume-unchanged tokens.py

.DEFAULT_GOAL := build