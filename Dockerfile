FROM ubuntu:18.04

RUN apt-get update -qq

RUN apt install -qqy \
    python3 python3-pip

RUN mkdir -p /srv/app
WORKDIR /srv/app
COPY . /srv/app
CMD dir
RUN pip3 install -r src/requirements.txt

ADD start.sh ./start.sh
RUN chmod +x ./start.sh

ENTRYPOINT ["/bin/bash", "/srv/app/start.sh"]
