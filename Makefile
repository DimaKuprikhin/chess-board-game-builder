PYCACHE=__pycache__
SCRIPTS_DB_DATA=test_data/scripts_db_data

clean:
	rm -rf ${PYCACHE}/*
	rm -rf .pytest_cache/*
	rm -rf common/${PYCACHE}/*
	rm -rf database/${PYCACHE}/*
	rm -rf executer/${PYCACHE}/*
	rm -rf test_data/${PYCACHE}/*
	rm -rf test_data/${SCRIPTS_DB_DATA}/*
