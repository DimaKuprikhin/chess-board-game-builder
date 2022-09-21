PYCACHE=__pycache__
SCRIPTS_DB_DATA=scripts_db_data
PYTEST_CACHE=.pytest_cache
TEST_SCRIPTS_DIR=scripts_dir

.PHONY: clean format init run test

clean:
	@find ./ -type d -name ${PYCACHE} -prune -exec rm -rf {} \;
	@rm -rf ./server_backend/test_data/${TEST_SCRIPTS_DIR}/*
	@find ./ -type d -name ${PYTEST_CACHE} -prune -exec rm -rf {} \;
	@find ./ -type d -name ${PYCACHE} -exec rmdir {} \;
	@find ./ -type d -name ${PYTEST_CACHE} -exec rmdir {} \;

format:
	@yapf3 --in-place ./*.py
	@yapf3 --in-place ./flask_tests/*.py
	@yapf3 --in-place ./flaskr/*.py
	@yapf3 --in-place ./server_backend/common/*.py
	@yapf3 --in-place ./server_backend/controller/*.py
	@yapf3 --in-place ./server_backend/database/*.py
	@yapf3 --in-place ./server_backend/executer/*.py
	@yapf3 --in-place ./server_backend/script_checker/*.py

init:
	@flask --app flaskr init-db
	@rm -rf ./scripts/*

run:
	@flask --app flaskr --debug run

internal_test_server_backend:
	@pytest server_backend -v

internal_test_flask:
	@pytest -v

test: internal_test_server_backend internal_test_flask clean

build_flask:
	python3 setup.py bdist_wheel

move_flask:
	scp ./dist/flaskr-1.0.0-py3-none-any.whl 51.250.76.192:/home/dima/server/flaskr-1.0.0-py3-none-any.whl

install_ONLY_ON_SERVER:
	ssh dima@51.250.76.192
	cd server
	virtualenv venv
	source venv/bin/activate
	mkdir script
	pip install Flask
	pip install flaskr-1.0.0-py3-none-any.whl
	pip install typing_extensions
	flask --app flaskr init-db
	pip install waitress
	waitress-serve --call 'flaskr:create_app'
	sudo kill -9 `sudo lsof -t -i:8080`
	waitress-serve --call 'flaskr:create_app'
