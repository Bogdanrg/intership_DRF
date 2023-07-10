FROM python:latest

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt /usr/src/app/requirements.txt

RUN apt-get update \
    && apt-get install netcat-traditional -y

RUN pip install -r requirements.txt


COPY ./entrypoint.sh .

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]