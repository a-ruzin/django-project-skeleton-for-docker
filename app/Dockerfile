FROM python:3.10-slim-bullseye as requirements
ARG PIPENV_OPTIONS=""
RUN pip install -U pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --keep-outdated ${PIPENV_OPTIONS} --requirements > requirements.txt

FROM python:3.10-slim-bullseye
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY --from=requirements /tmp/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "config.wsgi:application", "--bind",  "0.0.0.0:8000"]
