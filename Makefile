.PHONY: help install format build down logs check docker-test rebuild clean prune

# ANSI-colored status marks to highlight success/failure without external dependencies.
GREEN ?= \033[32m
RED ?= \033[31m
RESET ?= \033[0m

PY ?= python3
VENV ?= .venv
PIP ?= $(VENV)/bin/pip
PATH := $(abspath $(VENV)/bin):$(PATH)

LOG_LEVEL ?= info
OCR_URL ?= http://127.0.0.1:9000
MAX_IMAGE_MB ?= 15
TIMEOUT_MS ?= 15000

# Allow selective log tailing with `make logs api|ocr|portal`.
LOG_ARGS := $(filter api ocr portal,$(MAKECMDGOALS))

ifneq ($(words $(LOG_ARGS)),0)
ifneq ($(words $(LOG_ARGS)),1)
$(error Specify only one of api, ocr, or portal when invoking "make logs")
endif
endif

LOG_TARGET ?= all

ifneq ($(filter api,$(MAKECMDGOALS)),)
LOG_TARGET := api
endif
ifneq ($(filter ocr,$(MAKECMDGOALS)),)
LOG_TARGET := ocr
endif
ifneq ($(filter portal,$(MAKECMDGOALS)),)
LOG_TARGET := portal
endif

$(LOG_ARGS):
	@:

help:
	@echo "Available targets:"
	@echo "  install    Install API/OCR Python deps and portal/mobile npm deps"
	@echo "  check      Run scripts/run-all-checks.sh"
	@echo "  healthz    Curl healthz endpoints for api/ocr/portal"
	@echo "  build      docker compose up --build -d"
	@echo "  rebuild    docker compose up --build -d --force-recreate"
	@echo "  down       docker compose down"
	@echo "  logs       docker compose logs -f (use 'make logs api|ocr|portal' to filter)"
	@echo "  clean      docker compose down --remove-orphans"
	@echo "  prune      Stop stack + remove local images/volumes created by docker compose (destructive)"

install:
	@set -e; \
	if ! command -v $(PY) >/dev/null 2>&1; then \
		printf '$(RED)[FAIL]$(RESET) make install missing dependency: python3 is required. Install via "brew install python" or ensure it is on PATH.\n' >&2; \
		exit 1; \
	fi; \
	if ! command -v npm >/dev/null 2>&1; then \
		printf '$(RED)[FAIL]$(RESET) make install missing dependency: npm is required. Install Node.js via "brew install node".\n' >&2; \
		exit 1; \
	fi; \
	if ! command -v npx >/dev/null 2>&1; then \
		printf '$(RED)[FAIL]$(RESET) make install missing dependency: npx is required (bundled with npm >=5.2).\n' >&2; \
		exit 1; \
	fi; \
	if ! docker compose version >/dev/null 2>&1; then \
		printf '$(RED)[FAIL]$(RESET) make install missing dependency: Docker Compose V2 is required. Update Docker Desktop or install the compose plugin.\n' >&2; \
		exit 1; \
	fi; \
	if $(PIP) install --upgrade pip \
		&& $(PIP) install -r src/apps/api/requirements.txt \
		&& $(PIP) install -r src/apps/ocr/requirements.txt \
		&& $(PIP) install ruff pytest \
		&& npm install --prefix src/apps/portal; then \
		printf '$(GREEN)[OK]$(RESET) make install completed successfully.\n'; \
		if [ -f "src/apps/mobile/package.json" ]; then \
			cd src/apps/mobile && EXPO_NO_INTERACTIVE=1 npx expo install; \
		else \
			printf 'Skipping mobile install: src/apps/mobile/package.json not found\n'; \
		fi; \
		printf 'Activate with: source .venv/bin/activate\n'; \
	else \
		printf '$(RED)[FAIL]$(RESET) make install failed (see logs above).\n' >&2; \
		exit 1; \
	fi

check:
	@set -e; \
	if bash scripts/run-all-checks.sh; then \
		printf '$(GREEN)[OK]$(RESET) make check passed.\n'; \
	else \
		printf '$(RED)[FAIL]$(RESET) make check failed (see logs above).\n' >&2; \
		exit 1; \
	fi

healthz:
	@set -e; \
	health_targets="api:http://localhost:8000/healthz ocr:http://localhost:8080/healthz portal:http://localhost:8888/"; \
	failed=""; \
	for target in $$health_targets; do \
		service=$${target%%:*}; \
		url=$${target#*:}; \
		if curl -sfS "$$url" >/dev/null; then \
			printf '$(GREEN)[OK]$(RESET) %s (%s)\n' "$$service" "$$url"; \
		else \
			printf '$(RED)[FAIL]$(RESET) %s (%s)\n' "$$service" "$$url"; \
			failed="true"; \
		fi; \
	done; \
	if [ -n "$$failed" ]; then \
		printf '$(RED)[FAIL]$(RESET) make healthz failed.\n'; \
		exit 1; \
	else \
		printf '$(GREEN)[OK]$(RESET) make healthz succeeded for all services.\n'; \
	fi

build:
	@set -e; \
	if docker compose up --build -d; then \
		printf '$(GREEN)[OK]$(RESET) make build completed.\n'; \
	else \
		printf '$(RED)[FAIL]$(RESET) make build failed (see logs above).\n' >&2; \
		exit 1; \
	fi

rebuild:
	@set -e; \
	if docker compose up --build -d --force-recreate; then \
		printf '$(GREEN)[OK]$(RESET) make rebuild completed.\n'; \
	else \
		printf '$(RED)[FAIL]$(RESET) make rebuild failed (see logs above).\n' >&2; \
		exit 1; \
	fi

down:
	@set -e; \
	if docker compose down; then \
		printf '$(GREEN)[OK]$(RESET) make down completed.\n'; \
	else \
		printf '$(RED)[FAIL]$(RESET) make down failed (see logs above).\n' >&2; \
		exit 1; \
	fi

logs:
	@set -e; \
	RUNNING_SERVICES=$$(docker compose ps --status=running --services); \
	if [ -z "$$RUNNING_SERVICES" ]; then \
		printf '$(RED)[FAIL]$(RESET) make logs requires running containers. Start the stack with "make build" first.\n' >&2; \
		exit 1; \
	fi; \
	if [ "$(LOG_TARGET)" != "all" ] && ! echo "$$RUNNING_SERVICES" | grep -qx "$(LOG_TARGET)"; then \
		printf '$(RED)[FAIL]$(RESET) make logs %s requires the %s service to be running. Start it with "make build" first.\n' "$(LOG_TARGET)" "$(LOG_TARGET)" >&2; \
		exit 1; \
	fi; \
	case "$(LOG_TARGET)" in \
		api) docker compose logs -f api ;; \
		ocr) docker compose logs -f ocr ;; \
		portal) docker compose logs -f portal ;; \
		*) docker compose logs -f ;; \
	esac

clean:
	@set -e; \
	if docker compose down --remove-orphans; then \
		printf '$(GREEN)[OK]$(RESET) make clean completed.\n'; \
	else \
		printf '$(RED)[FAIL]$(RESET) make clean failed (see logs above).\n' >&2; \
		exit 1; \
	fi

prune:
	@set -e; \
	if docker compose down --remove-orphans --volumes --rmi local; then \
		docker image prune -f >/dev/null; \
		docker volume prune -f >/dev/null; \
		printf '$(GREEN)[OK]$(RESET) make prune completed (containers, images, and dangling volumes removed).\n'; \
	else \
		printf '$(RED)[FAIL]$(RESET) make prune failed (see logs above).\n' >&2; \
		exit 1; \
	fi

docker-test:
	@if ! docker compose ps api >/dev/null 2>&1; then \
		echo "API container not running. Run 'make build' first."; \
		exit 1; \
	fi
	docker compose exec api pytest
