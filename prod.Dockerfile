#https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
###########
# BUILDER #
###########

# pull official base image
FROM python:3.9-alpine as builder

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# lint
RUN pip install --upgrade pip

# install dependencies
COPY ./requirements.txt .
COPY . .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.9-alpine

WORKDIR /app

# install dependencies
RUN apk update && apk add libpq
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    && pip install --no-cache-dir psycopg2 \
    && apk del --no-cache .build-deps
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY . .

# Expose port
EXPOSE 8000