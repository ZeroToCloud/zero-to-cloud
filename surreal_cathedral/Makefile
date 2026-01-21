DAYS ?= 10
FPS ?= 4
LABELS ?= 1



.PHONY: build regen up down ps logs open

build:
	docker compose build

regen:
	docker compose run --rm -e DAYS=$(DAYS) -e FPS=$(FPS) -e LABELS=$(LABELS) cathedral


up:
	docker compose up -d web

down:
	docker compose down

ps:
	docker compose ps

logs:
	docker compose logs -f web

open:
	explorer.exe http://localhost:8080
