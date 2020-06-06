.PHONY: build
build:
	FLASK_APP=flask_app.py flask run

.PHONY: deploy
deploy:
	gunicorn flask_app:app

.PHONY: sql
sql:
	C:/sqlite/sqlite3 ./data.db < createdb.sql

.PHONY: tokens
tokens:
	git update-index --assume-unchanged tokens.py

.PHONY: secret_url
secret_url:
	python -c "import secrets;print(secrets.token_hex(16))"

.DEFAULT_GOAL := build