# Django Project skeleton for Docker

This repository is a skeleton for new django project.
It consists of 4 containers:

- web (nginx - front reverse proxy)
- app (django app)
- static (nginx - for feeding static files from django app)
- db (postgresql)

## Installation

1. Clone the repository

       # DISCLAMER: used with [fish shell](https://fishshell.com/)
       set PRJ_NAME prj
       git clone https://github.com/a-ruzin/django-project-skeleto-for-docker $PRJ_NAME
       cd $PRJ_NAME

2. Untie from GitHub and create local repository

       rm -rf .git
       git init
       git add .
       git commit -m 'initial commit'

3. Setup local environment to your needs

   Change IP or leave 0.0.0.0 (read more about [ip conflicts](#ip-conflicts)).

   Choose domain name, ports for a project.

       cp .env.example.env .env
       vi .env

   Setup SECRET_KEY and DEBUG:

       pushd deploy/envs/

       cp app.env.example.env app.env
       vi app.env

   Configure PostgreSQL options:

       cp postgres.env.example.env postgres.env
       vi postgres.env

       popd

4. Configure local docker-compose.yml

    Configure or remove `db` and `nginx` sections if necessary. 

       cp docker-compose.override.yml.example.yml docker-compose.override.yml
       vi docker-compose.override.yml

5. Build containers

       docker compose build

   > WARNING: `app` container may not be built because outdated
   > binary psycopg2 library. In this case remove --keep-outdated
   > flag in .env (PIPENV_KEEP_OUTDATED)

6. Start containers

       docker compose up -d

7. Make initial django setup

       docker compose exec app ./manage.py migrate
       docker compose exec app ./manage.py createsuperuser

8. Check for web-interface

   open http://skeleton/admin/ and log in with chosen attributes

9. setup pycharm

    1. open settings dialog
    2. search for "python interpreter" section
    3. click on link "Add interpreter"
    4. choose "On Docker Compose"
    5. follow instructions (select service 'app', ...)

## CSRF Protection

> If you changed `domain/port` in `docker-compose.override.yml`,
> don't forget to change it in `CSRF_TRUSTED_ORIGINS` variable
> in `app/config/settings/__init__.py`

#ip-conflicts
## Conflicts while developing several projects

Developing several projects we encounter conflicts in port bindings.
We can solve this problem by changing ports or IP using `docker-compose.override.yml`.
It is useful to bind services to ports as they used in production.
So let's use different IPs - bring up different loopback interface 127.0.0.* for each project.

Add loopback into /etc/hosts
   
    127.0.0.2	project

Then bring up this loopback interface up (for mac).

    sudo ifconfig lo0 alias 127.0.0.2 up
