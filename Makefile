.PHONY: install lint test cov-testing cov-production run docker-build docker-run docker-up docker-down db-migrate

install:
	pip install -r requirements-dev.txt

lint:
	ruff check .

test:
	python -m pytest -q

cov-testing:
	python -m pytest -q --cov=app --cov-report=term-missing --cov-fail-under=60

cov-production:
	python -m pytest -q --cov=app --cov-report=term-missing --cov-fail-under=85

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker build -t project-godzilla-api:local .

docker-run:
	docker run --rm -p 8000:8000 project-godzilla-api:local

docker-up:
	docker compose up --build

docker-down:
	docker compose down

db-migrate:
	docker compose run --rm api alembic upgrade head
