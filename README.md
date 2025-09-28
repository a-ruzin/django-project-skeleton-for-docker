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
       git clone git@github.com:a-ruzin/django-project-skeleton-for-docker.git $PRJ_NAME
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

4. Install pre-commit hooks

    ```
    brew install pre-commit
    pre-commit install
    ```
    > NOTE: To bypass pre-commit hooks, use the `git commit ... --no-verify`.

5. Configure local docker-compose.yml

    Configure or remove `db` and `nginx` sections if necessary. 

       cp docker-compose.override.yml.example.yml docker-compose.override.yml
       vi docker-compose.override.yml

6. Build containers

       docker compose build

   > WARNING: `app` container may not be built because outdated
   > binary psycopg2 library. In this case remove --keep-outdated
   > flag in .env (PIPENV_KEEP_OUTDATED)

7. Start containers

       docker compose up -d

8. Make initial django setup

       docker compose exec app ./manage.py migrate
       docker compose exec app ./manage.py createsuperuser

9. Check for web-interface

   open http://127.0.0.X/admin/ and log in with chosen attributes
   where X is your IP if you changed it in /etc/hosts or '1' otherwise.

10. setup pycharm

     1. open settings dialog
     2. search for "python interpreter" section
     3. click on link "Add interpreter"
     4. choose "On Docker Compose"
     5. follow instructions (select service 'app', ...)

## CSRF Protection

> If you changed `domain/port` in `docker-compose.override.yml`,
> don't forget to change it in `CSRF_TRUSTED_ORIGINS` variable
> in `app/config/settings/__init__.py`


## Conflicts while developing several projects {#ip-conflicts}

Developing several projects we encounter conflicts in port bindings.
We can solve this problem by changing ports or IP using `docker-compose.override.yml`.
It is useful to bind services to ports as they used in production.
So let's use different IPs - bring up different loopback interface 127.0.0.* for each project.

Add loopback into /etc/hosts
   
    127.0.0.2	project

Then bring up this loopback interface up (for mac).

    sudo ifconfig lo0 alias 127.0.0.2 up

## Adding new package to repository
1. Add your package to `Pipenv` file. Be sure that you specified version if needed, or just add `"*"`. Also, put that package to `[dev-packages]` section if this package is used only in development (not in production environment).
2. Lock you `Pipenv` file:
```
pipenv lock
```
3. Sync you virtual environment packages:
```
pipenv sync
```


## Frontend (React SPA)

For that reasons you may want to put frontend in a separate repository:
 - foreign team has no access to backend repository
 - frontend developer does not need to install docker
 - different teams may use different tools for frontend and backend development

All you need from frontend is contents of a build directory which become a part of django app.

So basic setup is:

    cd $PRJ_NAME
    git clone https://github.com/a-ruzin/react-frontend-skeletor-for-django frontend
    cd frontend
    rm -rf .git
    git init
    git add .
    git commit -m 'initial commit'



## Next steps
remove all the content above and leave (tuned) following part:

# Project

Project - инструмент ...


- [Архитектура](docs/ARCHITECHTURE-C4/README.md).
- [Установка (для локальной разработки)](docs/installation_local_dev.md).
- [Установка (для продакшн)](docs/installation_production.md).
- [Локализация](docs/localization.md).
