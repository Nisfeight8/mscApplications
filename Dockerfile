# pull official base image
FROM python:3.8-alpine

# set workdir
WORKDIR /usr/src/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev\
    && apk add --virtual build-deps\
    && apk add jpeg-dev zlib-dev libjpeg

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN apk del build-deps
#copy project
COPY . .



