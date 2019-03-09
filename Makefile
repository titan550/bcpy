cnf ?= .env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

test: ## Tests the package by running a SQL Server container and running the test cases
			docker stop bcpy_test_mssql_server || true && docker rm bcpy-mssq-test || true
			docker run --rm --name 'bcpy_test_mssql_server' -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=$(TEST_MSSQL_SA_PASSWORD)' -p $(TEST_MSSQL_PORT):1433 -d mcr.microsoft.com/mssql/server:2017-latest
			docker images | grep "bcpy_test_py_client" | awk '{print $1 ":" $2}' | xargs --no-run-if-empty docker rmi
			python3 -m pip install --upgrade setuptools wheel
			rm -rf dist build bcpy.egg-info
			python3 setup.py sdist bdist_wheel
			docker build --force-rm -t bcpy_test_py_client -f ./tests/Dockerfile .
			docker run --rm bcpy_test_py_client
			docker stop bcpy_test_mssql_server