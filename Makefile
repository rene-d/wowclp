

default: run

.PHONY: run
run:
	docker-compose run --rm main

.PHONY: build
build:
	docker-compose build main
