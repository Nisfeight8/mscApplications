# pull official base image
FROM python:3.8-alpine

# set workdir
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev\
    && apk add --virtual build-deps\
    && apk add jpeg-dev zlib-dev libjpeg

# add user
RUN addgroup -S appuser && adduser -S appuser -G appuser  --home /usr/src/app
# add permissions

ENV PATH=$PATH:/usr/src/app/.local/bin

# install requirements
RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN apk del build-deps

#copy project
COPY mscApplications .

USER root
RUN chown -R appuser:appuser /usr/src/app

USER appuser:appuser

RUN  python manage.py collectstatic --noinput

# TODO: superuser, migrations
WORKDIR /usr/src/app

EXPOSE 8000/tcp
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000","mscApplications.wsgi"]

