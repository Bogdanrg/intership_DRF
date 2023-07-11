FROM python:latest

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt /usr/src/app/requirements.txt

COPY Pipfile Pipfile.lock ./

RUN apt-get update \
    && apt-get install netcat-traditional -y

RUN pip install -U pipenv \
    && pipenv install --system


COPY entrypoint.sh /usr/src/app/entrypoint.sh

COPY . .