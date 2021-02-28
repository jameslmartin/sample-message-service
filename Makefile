.PHONY: help network start-db unit-test dev start message-service
.DEFAULT_GOAL := help

DOCKER_IMAGE  := guild:latest
APP_PORT      := 8080

NETWORK       := guild

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run-docker:
	@-docker rm -f $(DOCKER_CONTAINER_NAME)
	@docker run --rm \
		$(DOCKER_OPTS) \
		$(DOCKER_PORTS) \
 		--name=$(DOCKER_CONTAINER_NAME) \
		--network=$(NETWORK) \
		--workdir /home/app/ \
		$(DOCKER_IMAGE) $(DOCKER_CMD)

network: ## Create docker network
	docker network create --driver bridge $(NETWORK)

build: ## Build the latest Flask app
	docker build -t guild -f ./Dockerfile .

service: ## Rebuild and stand up Postgres database and service in detached mode
	docker-compose up --build

# Adds host to /etc/hosts/ file that might be shared by Docker network
start-db: DOCKER_CONTAINER_NAME=postgres
start-db: DOCKER_OPTS=--add-host=postgres:0.0.0.0 \
	-v db_volume:/var/lib/postgresql/data \
	-v `pwd`/db/init:/docker-entrypoint-initdb.d \
	-e POSTGRES_PASSWORD=education
start-db: DOCKER_PORTS=-p 5432:5432
start-db: DOCKER_IMAGE=postgres:latest
start-db: run-docker
start-db: ## Run Postgres with mounted init script

unit-test: DOCKER_CONTAINER_NAME=guild-test
unit-test: DOCKER_OPTS=-it
unit-test: DOCKER_IMAGE=guild:latest
unit-test: DOCKER_CMD=pytest -s app
unit-test: run-docker
unit-test: ## Run unit tests in project

functional-test: DOCKER_CONTAINER_NAME=guild-test
functional-test: DOCKER_OPTS=-it \
	-v `pwd`:/home/app/ 
functional-test: NETWORK=host
functional-test: DOCKER_IMAGE=guild:latest
functional-test: DOCKER_CMD=pytest -s functional_test
functional-test: run-docker
functional-test: ## Run functional tests on project - must be running both db and service (either through compose or manually)

dev: DOCKER_CONTAINER_NAME=message-service
dev: DOCKER_PORTS=-p 0.0.0.0:$(APP_PORT):8080
dev: DOCKER_OPTS=-it -v `pwd`:/home/app/ \
	--env-file ./.env
dev: DOCKER_CMD=bash
dev: run-docker
dev: ## Run Flask app container with local dir mounted to iterate

start: ## Shortcut to running a wsgi server with gunicorn, can be run in dev container
	gunicorn -b 0.0.0.0:8080 wsgi:app

message-service: DOCKER_CONTAINER_NAME=message-service
message-service: DOCKER_PORTS=-p 0.0.0.0:$(APP_PORT):8080
message-service: DOCKER_OPTS=-it --env-file ./.env
message-service: run-docker
message-service: ## Run Flask app server for messages, must start db first
