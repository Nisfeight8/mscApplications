# MscApplications
Implementation of an application management system for prospective students in the postgraduate program of the institution. Various possibilities are provided at the level of the evaluation committee: summary reports related to the applications, introduction of evaluation criteria, etc.

## Tech

MscApplications uses a number of open source projects to work properly:

- [Django] - Python framework!
- [Bootstrap] - great UI boilerplate for modern web apps
- [Postgres] - Database


And of course MscApplications itself is open source with a [public repository][dill]
 on GitHub.

## Installation

Install the dependencies and devDependencies and start the server.

```sh
cd mscApplications
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Docker

mscApplications is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8000, so change this within the
docker-compose.yml if necessary. When ready, simply use the Dockerfile to
build the image.

```sh
cd mscApplications
docker-compose up --build
```

This will create the web ,db and nginx images and pull in the necessary dependencies.

