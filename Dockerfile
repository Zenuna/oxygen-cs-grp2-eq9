# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /app
RUN pip install pipenv

COPY ./Pipfile /app
COPY ./Pipfile.lock /app
RUN pipenv install

COPY . ./

CMD ["pipenv", "run", "python", "./src/main.py"]