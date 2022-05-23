# Django Project skeleton for Docker 

This repository is a skeleton for new django project.
It consists of 4 containers:
 - web (nginx - front reverse proxy)
 - app (django app)
 - static (nginx - for feeding static files from django app)
 - db (postgresql)

## Installation

1. clone the repository

       # DISCLAMER: used with [fish shell](https://fishshell.com/)
       set PRJ_NAME prj
       git clone https://github.com/a-ruzin/django-project-skeleto-for-docker $PRJ_NAME
       cd $PRJ_NAME

2. untie from github and create local repository

       rm -rf .git
       git init
       git add .
       git commit -m 'initial commit'

3. setup local environment to your needs

       pushd deploy/envs/
       cp app.env.example.env app.env
       vi app.env
       cp postgres.env.example.env postgres.env
       vi postgres.env
       popd

4. start containers

       docker compose up -d

5. make initial django setup

       docker compose exec app ./manage.py migrate
       docker-compose exec app ./manage.py createsuperuser

6. setup pycharm

       cd app
       pipenv shell
       pipenv install
