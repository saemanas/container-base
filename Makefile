.PHONY: help install lint test format up down logs ci local docker-test

PY ?= python3

help:
	@echo "Available targets:"
	@echo "  install    Install API/OCR Python deps and portal/mobile npm deps"
	@echo "  lint       Run Ruff (API/OCR) and portal ESLint"
	@echo "  test       Run pytest suites"
	@echo "  ci         Run scripts/run-all-checks.sh"
	@echo "  local      Run scripts/run-local.sh"
	@echo "  up         docker compose up --build"
	@echo "  down       docker compose down"
	@echo "  logs       docker compose logs -f"

install:
	$(PY) -m pip install -r src/apps/api/requirements.txt
	$(PY) -m pip install -r src/apps/ocr/requirements.txt
	npm install --prefix src/apps/portal
	npx expo install --cwd src/apps/mobile

lint:
	ruff check src/apps/api src/apps/ocr
	npm run lint --prefix src/apps/portal
	@echo "Mobile lint skipped (no automated lint script yet)"

test:
	pytest

ci:
	bash scripts/run-all-checks.sh

local:
	bash scripts/run-local.sh

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

docker-test:
	@if ! docker compose ps api >/dev/null 2>&1; then \
		echo "API container not running. Run 'make up' first."; \
		exit 1; \
	fi
	docker compose exec api pytest
