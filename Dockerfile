# pull official base image
FROM python:3.9-alpine

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
RUN chown -R appuser:appuser /usr/src/app

USER appuser:appuser

ENV PATH=$PATH:/usr/src/app/.local/bin


# install requirements
RUN pip install --upgrade pip

COPY  --chown=appuser:appuser ./requirements.txt .

RUN pip install -r requirements.txt

#copy project
COPY  --chown=appuser:appuser mscApplications .

RUN  python manage.py collectstatic --noinput

# TODO: superuser, migrations
WORKDIR /usr/src/app

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000","mscApplications.wsgi"]

