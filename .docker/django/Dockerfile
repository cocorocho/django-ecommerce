FROM python:3.12-slim as base

RUN apt update

COPY ./server /code

# CD to Project dir
WORKDIR /code/api

COPY .docker/django/entrypoint.sh /
RUN chmod +x /entrypoint.sh

# Install base requirements
RUN pip install -r api/requirements/base.txt

##### DEV Build ######
FROM base as development
RUN pip install -r api/requirements/dev.txt
######################


##### Prod Build #####
FROM base as production

# Set env to PROD
ENV DJANGO_SETTINGS_MODULE="api.settings.prod"
RUN pip install -r api/requirements/prod.txt
######################

ENTRYPOINT [ "/entrypoint.sh" ]
