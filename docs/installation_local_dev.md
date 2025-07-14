# PROJECT

Установка для локальной разработки

- [Installation](#installation)
- [Conflicts while developing several projects](#conflicts-while-developing-several-projects)

## Installation <a id="installation"></a>

1. Clone repositories

       git@github.com:a-ruzin/django-project-skeleton-for-docker.git project
       cd project
       git@github.com:a-ruzin/django-project-skeleton-for-docker-frontend.git frontend

2. Copy env files

       cp .env.example.env .env
       cp frontend/.env.example frontend/.env

3. Setup alias for domains to /etc/hosts

       127.0.0.11 project

    > Mac OS note\
    By default Mac OS does not bring up all 127.0.0.* interfaces.\
    But if you want to use them you can do it by running following command:
    >
    >     sudo ifconfig lo0 alias 127.0.0.11 up

4. Setup local environment
   You need to setup following variables:
      - **.env**:
         - PROJECT_IP (set 127.0.0.11)
         - PROJECT_DOMAIN (set project)
         - PROJECT_PORT_SSL (leave it empty)
         - SECRET_KEY (set it randomly by yourself)
         - PROXY (ask project maintainer)
         - OPENAI_API_KEY (ask project maintainer)
         - OPENAI_GPT_MODEL (ask project maintainer)
         - OPENAI_ASSISTANT_ID (ask project maintainer)
         - FRONTEND_API_URL (set http://project/api/v1)
         - FRONTEND_NEXT_PUBLIC_STORAGE_URL (set http://project)
         - FRONTEND_PROJECT_DOMAIN (set project)
      - **frontend/.env**:
         - API_URL (set http://project/api/v1)
         - NEXT_PUBLIC_DJANGO_DASHBOARD_URL (set http://project/admin/)
         - NEXT_PUBLIC_STORAGE_URL (set http://project)

5. Configure local docker-compose.yml

    Copy local docker-compose.yml

       cp docker-compose.override.yml.example.yml docker-compose.override.yml

    Copy configuration

       services:
            app: # ------------------------------------------------------------------
                volumes:
                    - ./app:/app
            nginx: # --------------------------------------------------------------------
                ports:
                    - "${PROJECT_IP:-0.0.0.0}:80:80"

6. Install docker containers

       make all

7. Create user

       make createsuperuser
