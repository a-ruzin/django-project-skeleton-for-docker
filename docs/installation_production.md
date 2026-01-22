# PROJECT

## Installation (for production) <a id="installation"></a>

### Prerequisites
 - Assuming you have a server with docker and docker-compose installed.
 - Domain `project.ru` is pointed to the server IP.
 - You as a user `project` logged in to the server and able to run docker containers.

### Steps

1. Creating ssh keys for deployment

       ssh-keygen -t rsa -b 4096 -C "project@project.ru" -f ~/.ssh/id_rsa_gitlab_project_backend
       ssh-keygen -t rsa -b 4096 -C "project@project.ru" -f ~/.ssh/id_rsa_gitlab_project_frontend

2. Setting up SSH config

   Create a file `~/.ssh/config` with the following content:

       ForwardAgent=yes
       AddKeysToAgent yes

       # git@gitlab.kokoc.com:kg/project/backend/ai-strategist.git
       Host backend
           HostName gitlab.kokoc.com
           User git
           IdentityFile ~/.ssh/id_rsa_gitlab_project_backend

       # git@gitlab.kokoc.com:kg/project/frontend/fe.git
       Host fontend
           HostName gitlab.kokoc.com
           User git
           IdentityFile ~/.ssh/id_rsa_gitlab_project_frontend

3. Setting up these keys into two repositories:

   1. BACKEND:

          cat ~/.ssh/id_rsa_gitlab_project_backend.pub

      create a new deploy key with title 'project.ru (PRODUCTION)' at Backend repository\
      https://gitlab.kokoc.com/kg/project/backend/ai-strategist/-/settings/repository#js-deploy-keys-settings

   2. FRONTEND:

          cat ~/.ssh/id_rsa_gitlab_project_frontend.pub

      create a new deploy key with title 'project.ru (PRODUCTION)' at Frontend repository\
      https://gitlab.kokoc.com/kg/project/frontend/fe/-/settings/repository#js-deploy-keys-settings

4. Clone repositories

   1. BACKEND: cloning repository to ~/project:

          git clone git@backend:kg/project/backend/ai-strategist.git project

   2. FRONTEND: cloning repository to ~/project/frontend:

          cd project
          git clone git@frontend:kg/project/frontend/fe.git frontend

5. Setting up .env files

   1. BACKEND:

          cp .env.example.env .env
          vi .env

      Fill in contents:

          PROJECT_IP=0.0.0.0
          PROJECT_PROTOCOL=https
          PROJECT_DOMAIN=project.ru
          PROJECT_PORT=443
          PROJECT_PORT_HTTP=80
          PROJECT_PORT_SSL=443

          SECRET_KEY=<<<<<< TYPE HERE A RANDOM STRING >>>>>>
          DEBUG=False
          TEMPLATE_DEBUG=
          SENTRY_DSN=<<<<<< GET PROJECT DSN FROM SENTRY ADMIN >>>>>>

          POSTGRES_HOST=db
          POSTGRES_PORT=5432
          POSTGRES_USER=postgres
          POSTGRES_PASSWORD=<<<<<< CHANGE TO A SECRET PASSWORD >>>>>>
          POSTGRES_DB=postgres

          RABBITMQ_DEFAULT_USER=rabbituser
          RABBITMQ_DEFAULT_PASS=<<<<<< CHANGE TO A SECRET PASSWORD >>>>>>

          PROXY=<<<<<< TAKE SETTINGS FROM SYSTEM ADMINISTRATOR >>>>>>

          OPENAI_API_KEY=<<<<<< TAKE SETTINGS FROM OPENAI ACCOUNT OWNER >>>>>>
          OPENAI_GPT_MODEL=gpt-4o
          OPENAI_ASSISTANT_ID=<<<<<< TAKE SETTINGS FROM OPENAI ACCOUNT OWNER >>>>>>

          # for future use, copy settings from frontend.env
          FRONTEND_PROJECT_DOMAIN=project.ru
          FRONTEND_API_URL="https://project.ru/api/v1"
          FRONTEND_NEXT_PUBLIC_STORAGE_URL="https://project.ru"
          FRONTEND_NEXT_PUBLIC_DJANGO_DASHBOARD_URL="https://project.ru/admin/"

   2. FRONTEND:

          cp frontend/.env.example frontend/.env
          vi frontend/.env

      Fill in contents:

          API_URL="https://project.ru/api/v1"
          NEXT_PUBLIC_STORAGE_URL="https://project.ru"
          NEXT_PUBLIC_DJANGO_DASHBOARD_URL="https://project.ru/admin/"

6. Configure local docker-compose.yml

   Copy local docker-compose.yml

       cp docker-compose.override.yml.example.yml docker-compose.override.yml
       vi docker-compose.override.yml

   Tune number of celery workers:

          services:
            celery_worker:
              command: celery -A core worker -l INFO --autoscale=5,1

7. Install docker containers

       make all

8. Setting up SSL

       make ssl-init

9. Create a user

       make createsuperuser
