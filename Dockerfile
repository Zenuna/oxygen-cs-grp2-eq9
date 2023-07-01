# syntax=docker/dockerfile:1
FROM python:3.8-alpine as build
WORKDIR /app
COPY Pipfile Pipfile.lock ./
COPY ./src ./src
RUN pip install pipenv && pipenv install

FROM python:3.8-alpine as main
COPY --from=build /app /
CMD ["pipenv", "run", "python", "-u", "./src/main.py"]
