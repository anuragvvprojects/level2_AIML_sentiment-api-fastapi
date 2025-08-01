SHELL := /bin/bash
PY := python

.PHONY: help install fmt lint test run docker-build docker-run pre-commit

help:
	@echo "Targets:"
	@echo "  install       - install requirements"
	@echo "  fmt           - run formatters (black, isort)"
	@echo "  lint          - run flake8"
	@echo "  test          - run pytest"
	@echo "  run           - run API locally (uvicorn --reload)"
	@echo "  docker-build  - build Docker image"
	@echo "  docker-run    - run Docker container"
	@echo "  pre-commit    - install pre-commit hooks"

install:
	pip install -r requirements.txt

fmt:
	black . && isort .

lint:
	flake8 .

test:
	pytest -q

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker build -t sentiment-analysis-api:latest -f infra/Dockerfile .

docker-run:
	docker run --rm -p 8000:8000 \
		-e MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english \
		sentiment-analysis-api:latest

pre-commit:
	pre-commit install
