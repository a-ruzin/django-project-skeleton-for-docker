-include .env
ifneq ("$(wildcard .env)","")
export $(shell sed 's/=.*//' .env)  # Export all variables to subprocesses
endif
.PHONY: all test testv dcrb clean_db dump_db restore_db up down build migrate migrations static shell check_db_container_is_running nginx

MAIN_BRANCH=main
DEFAULT_DB_DUMP_FILE=deploy/data/backup/db/dump.sql.gz
DEFAULT_MEDIA_DUMP_FILE=deploy/data/backup/app_media/media.tar.gz

RED = \033[0;31m
WHITE = \033[1;37m
NC = \033[0m

ifdef MEDIA_DUMP
  MEDIA_BACKUP_DIR := $(dir $(MEDIA_DUMP))
  MEDIA_BACKUP_FILE := $(notdir $(MEDIA_DUMP))

  ifeq ($(MEDIA_BACKUP_DIR),)
    MEDIA_BACKUP_DIR := ./
  endif

  ifneq ($(patsubst /%,/,$(MEDIA_BACKUP_DIR)),/)
    MEDIA_BACKUP_DIR := $(abspath $(MEDIA_BACKUP_DIR))/
  endif
else
  MEDIA_BACKUP_DIR := $$(pwd)/$(dir $(DEFAULT_MEDIA_DUMP_FILE))
  MEDIA_BACKUP_FILE := $(notdir $(DEFAULT_MEDIA_DUMP_FILE))
endif


# COMMANDS

all: build down up migrate collectstatic

check_db_container_is_running:
	@if ! docker compose ps db --status running | grep -q "db"; then \
		echo "Error: Database container is not running!" >&2; \
		exit 1; \
	fi

clean_db: check_db_container_is_running
	@echo "Cleaning database..."
	@docker compose exec -T db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"


dump_test_db: check_db_container_is_running
	@echo "Dumping database..."
	@docker compose exec -T db /bin/bash -c 'PGPASSWORD="$$POSTGRES_PASSWORD" pg_dump -U "$$POSTGRES_USER" "$$POSTGRES_DB" > /var/lib/backup/test_data/stage_db.sql'


dump_db: check_db_container_is_running
	@echo "Dumping database..."
	$(eval BRANCH = $(shell git rev-parse --abbrev-ref HEAD))
	@if [ ! "${BRANCH}" = "${MAIN_BRANCH}" ]; then \
		echo "${RED}WARNING:${NC} make dump_db should be done on ${WHITE}${MAIN_BRANCH}${NC} branch."; \
		echo "Type 'yes' to continue"; \
		read user_input; \
		if [ "$$user_input" != "yes" ]; then \
			echo "Aborting execution."; \
			exit 1; \
		fi; \
    fi
ifeq ($(DB_DUMP),)
	$(eval DB_DUMP=${DEFAULT_DB_DUMP_FILE})
endif
	@if [ -f ${DB_DUMP} ]; then \
		echo "${RED}WARNING:${NC} a file ${WHITE}${DB_DUMP}${NC} exists. The command will overwrite its contents" ; \
		echo "Optionally you could specify a target file:"; \
		echo "${WHITE}Usage:${NC}"; \
		echo "DB_DUMP=${DEFAULT_DB_DUMP_FILE} make dump_db"; \
		echo ; \
		echo "Do you want to continue? Type 'yes' to proceed or anything else to abort." ; \
		read user_input; \
		if [ "$$user_input" != "yes" ]; then \
			echo "Aborting execution."; \
			exit 1; \
		fi; \
    fi
	$(eval SUFFIX = $(suffix ${DB_DUMP}))
	@if [ "${SUFFIX}" = ".gz" ]; then \
		docker compose exec -T db /bin/bash -c 'PGPASSWORD="$$POSTGRES_PASSWORD" pg_dump -U "$$POSTGRES_USER" "$$POSTGRES_DB"' | gzip > ${DB_DUMP} ; \
	else \
		docker compose exec -T db /bin/bash -c 'PGPASSWORD="$$POSTGRES_PASSWORD" pg_dump -U "$$POSTGRES_USER" "$$POSTGRES_DB"' > ${DB_DUMP} ; \
	fi ; \
	if [ -f ${DB_DUMP} ] ; then \
		echo "... saved into ${WHITE}${DB_DUMP}${NC}." ; \
		ls -la ${DB_DUMP} ; \
	fi

restore_db: check_db_container_is_running
	@if [ ! -f "${DB_DUMP}" ]; then \
		echo "${WHITE}Usage:${NC}"; \
		echo "DB_DUMP=${DEFAULT_DB_DUMP_FILE} make restore_db"; \
		echo "${WHITE}${DB_DUMP}${NC}"; \
		exit 1; \
	fi
	$(eval SUFFIX = $(suffix ${DB_DUMP}))
	@echo "You are going to replace DB data with contents of ${WHITE}${DB_DUMP}${NC}."
	@echo
	@echo "${RED}WARNING:${NC} Replacing DB may have serious consequences."
	@echo "Make a backup with backup.sh first."
	@echo
	@echo "Do you want to continue? Type 'yes' to proceed or anything else to abort."
	@read user_input; \
	if [ "$$user_input" != "yes" ]; then \
		echo "Aborting execution."; \
	else \
		echo "Proceeding with replacing DB..."; \
		docker compose exec -T db /bin/bash -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"'; \
		if [ "${SUFFIX}" = ".gz" ]; then \
			docker cp ${DB_DUMP} $(shell docker compose ps -q db):/tmp/dump.sql.gz; \
			docker compose exec -T db /bin/bash -c 'gunzip /tmp/dump.sql.gz'; \
		else \
			docker cp ${DB_DUMP} $(shell docker compose ps -q db):/tmp/dump.sql; \
		fi; \
		docker compose exec -T db /bin/bash -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -f /tmp/dump.sql'; \
		docker compose exec db rm /tmp/dump.sql; \
	fi

dump_media:
	@if [ -f $(MEDIA_BACKUP_DIR)${MEDIA_BACKUP_FILE} ]; then \
		echo "${RED}WARNING:${NC} a file ${WHITE}${MEDIA_BACKUP_FILE}${NC} exists. The command will overwrite its contents" ; \
		echo "Optionally you could specify a target file:"; \
		echo "${WHITE}Usage:${NC}"; \
		echo "MEDIA_DUMP=${DEFAULT_MEDIA_DUMP_FILE} make dump_media"; \
		echo ; \
		echo "Do you want to continue? Type 'yes' to proceed or anything else to abort." ; \
		read user_input; \
		if [ "$$user_input" != "yes" ]; then \
			echo "Aborting execution."; \
			exit 1; \
		fi; \
    fi ; \
    echo MEDIA_BACKUP_DIR $(MEDIA_BACKUP_DIR)
	@docker run --rm --volumes-from $$(docker compose ps -q app) \
	  -v $(MEDIA_BACKUP_DIR):/backup busybox \
	  sh -c 'cd /app/media && tar -czf /backup/$(MEDIA_BACKUP_FILE) .'
	@ls -la $(MEDIA_BACKUP_DIR)$(MEDIA_BACKUP_FILE)


restore_media:
	@if [ ! -f $(MEDIA_BACKUP_DIR)${MEDIA_BACKUP_FILE} ]; then \
        echo "${RED}ERROR:${NC}: Backup file $(MEDIA_BACKUP_DIR)${MEDIA_BACKUP_FILE} not found"; \
        exit 1; \
    fi
	@echo "You are going to replace Media data with contents of ${WHITE}${MEDIA_BACKUP_FILE}${NC}."
	@echo
	@echo "${RED}WARNING:${NC} Replacing media would not be reversible."
	@echo "Make a backup first."
	@echo
	@echo "Do you want to continue? Type 'yes' to proceed or anything else to abort."
	@read user_input; \
	if [ "$$user_input" != "yes" ]; then \
		echo "Aborting execution."; \
	else \
		docker compose exec -T app bash -c '\
			echo "Cleaning existing media..." && \
			rm -rf /app/media/* /app/media/.[!.]* /app/media/..?* && \
			echo "Extracting backup..." && \
			tar -xzf - -C /app --strip-components=1 \
		' < $(MEDIA_BACKUP_DIR)${MEDIA_BACKUP_FILE} ; \
		echo "Media restore completed successfully" ; \
		echo ; \
		echo "RESTORED CONTENT OF ${WHITE}/app/media${NC} in ${WHITE}app${NC} container: ------------------" ; \
		docker compose exec -T app bash -c 'ls -la /app/media/' ; \
		echo "-------------------------------------------------------------------" ; \
	fi

up:
	@docker compose up -d


down:
	@docker compose down


build:
	@docker compose build


migrate:
	@docker compose exec -T app python manage.py migrate $(ARGS)


collectstatic:
	@docker compose exec -T app python manage.py collectstatic --no-input


migrations:
	@docker compose exec -T app python manage.py makemigrations $(ARGS)

messages:
	@docker compose exec -T app python manage.py makemessages -l $(ARGS)

translatemessages:
	@docker compose exec -T app python manage.py translatemessages -l $(ARGS)

cleanmessages:
	@docker compose exec -T app python manage.py cleanmessages -l $(ARGS)

compilemessages:
	@docker compose exec -T app python manage.py compilemessages -l $(ARGS)

createsuperuser:
	@docker compose exec -it app python manage.py createsuperuser

bash:
	@docker compose exec app bash

shell:
	@docker compose exec -it app python manage.py shell

restart:
	@docker compose restart

hard_restart: down up

test:
	@docker compose exec app pytest $(ARGS)

testv:
	@docker compose exec app pytest -vv $(ARGS)

nginx:
	@docker compose exec nginx sh
