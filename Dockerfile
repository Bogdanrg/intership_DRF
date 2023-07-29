FROM python:latest

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./

RUN apt-get update \
    && apt-get install netcat-traditional -y

RUN pip install -U pipenv \
    && pipenv install --system


COPY entrypoint.sh /usr/src/app/entrypoint.sh
COPY celery-ep.sh /usr/src/app/celery-ep.sh
COPY consumer-ep.sh /usr/src/app/consumer-ep.sh

COPY . .
