PYCACHE=__pycache__
SCRIPTS_DB_DATA=scripts_db_data
PYTEST_CACHE=.pytest_cache
TEST_SCRIPTS_DIR=scripts_dir

.PHONY: clean format init run test

clean:
	@find ./ -type d -name ${PYCACHE} -prune -exec rm -rf {} \;
	@find ./server_backend/test_data -type d -name ${TEST_SCRIPTS_DIR} -prune -exec rm -rf {} \;
	@find ./ -type d -name ${PYTEST_CACHE} -prune -exec rm -rf {} \;
	@find ./ -type d -name ${PYCACHE} -exec rmdir {} \;
	@find ./server_backend/test_data -type d -name ${TEST_SCRIPTS_DIR} -exec rmdir {} \;
	@find ./ -type d -name ${PYTEST_CACHE} -exec rmdir {} \;

format:
	@yapf3 --in-place ./*.py
	@yapf3 --in-place ./*/*.py
	@yapf3 --in-place ./*/*/*.py

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
