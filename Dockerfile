FROM python:3.10.8-slim-buster AS base

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

COPY conf/nginx.conf /etc/nginx
COPY --chown=www-data:www-data . /srv/flask_app

WORKDIR /srv/flask_app
RUN pip install -r requirements.txt --src /usr/local/src
CMD ["/bin/bash", "-e", "./start.sh"]

FROM base AS iast

ARG IMMUNITY_HOST

ARG IMMUNITY_PORT

ARG IMMUNITY_PROJECT

ENV INSTRUMENTED=True

RUN pip install requests immunity-iast==0.2.8 --upgrade

RUN python3 -m immunity_agent $IMMUNITY_HOST $IMMUNITY_PORT $IMMUNITY_PROJECT

CMD ["/bin/bash", "-e", "./start.sh"]
