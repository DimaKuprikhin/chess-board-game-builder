PYCACHE=__pycache__
SCRIPTS_DB_DATA=scripts_db_data

clean:
	rm -rf .pytest_cache/*
	rm -f .pytest_cache/.gitignore
	rm -rf ${PYCACHE}/*
	rm -rf server_backend/${PYCACHE}/*
	rm -rf server_backend/controller/${PYCACHE}/*
	rm -rf server_backend/database/${PYCACHE}/*
	rm -rf server_backend/executer/${PYCACHE}/*
	rm -rf server_backend/script_checker/${PYCACHE}/*
	rm -rf server_backend/test_data/${PYCACHE}/*
	rm -rf server_backend/test_data/${SCRIPTS_DB_DATA}/*
	-rmdir .pytest_cache
	# -rmdir ${PYCACHE}
	-rmdir server_backend/${PYCACHE}
	-rmdir server_backend/controller/${PYCACHE}
	-rmdir server_backend/database/${PYCACHE}
	-rmdir server_backend/executer/${PYCACHE}
	-rmdir server_backend/script_checker/${PYCACHE}
	-rmdir server_backend/test_data/${PYCACHE}
	-rmdir server_backend/test_data/${SCRIPTS_DB_DATA}
