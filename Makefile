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
	@rm -rf ./scripts
	@mkdir ./scripts
	@rm -rf ./server_backend/test_data/${TEST_SCRIPTS_DIR}
	@mkdir ./server_backend/test_data/${TEST_SCRIPTS_DIR}

run:
	@flask --app flaskr --debug run

internal_test_server_backend:
	@pytest server_backend -v

internal_test_flask:
	@pytest -v

test: internal_test_server_backend internal_test_flask clean
