FROM python:3.13-slim-bookworm

WORKDIR /app
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    locales \
    net-tools \
    procps \
    vim \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools && pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "config.wsgi:application", "--bind",  "0.0.0.0:8000"]
