cnf ?= .env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

.PHONY: help test dev build

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

test: ## Test using docker-compose
	docker-compose -f tests/docker-compose.yml up --exit-code-from client --build

dev: build ## Starts a shell in the client environment
	chcon -Rt svirt_sandbox_file_t $(shell pwd)
	docker-compose -f tests/docker-compose.yml run --rm -v "$(shell pwd):/bcpy" client bash || true
	docker-compose -f tests/docker-compose.yml down

build: ## builds docker images in the docker-compose file
	docker build --force-rm -t bcpy_client -f ./tests/Dockerfile .
