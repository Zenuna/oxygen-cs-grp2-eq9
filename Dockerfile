# syntax=docker/dockerfile:1
FROM python:3.8-alpine

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && pipenv install

COPY ./src ./src

CMD ["pipenv", "run", "python", "-u", "./src/main.py"]
