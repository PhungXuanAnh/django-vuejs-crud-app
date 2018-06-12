# Author: Cuong Nguyen
#
# Build: docker build -t push_channel:0.1.0 .
#-----------------------------------------------------------------------------------------------------------------------

FROM ubuntu:16.04
MAINTAINER Phung Xuan Anh phungxuananh1991@gmail.com

RUN apt-get update -qq

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip build-essential \
    python3-dev locales

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y npm curl
RUN DEBIAN_FRONTEND=noninteractive curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y vim iputils-ping
# libmysqlclient-dev libxml2-dev libxslt1-dev libssl-dev libffi-dev

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8

RUN mkdir -p /build
WORKDIR /build

COPY . /build

# RUN pip3 install pip --upgrade # pip3 version 10 has bug
RUN pip3 install -r requirements.txt

RUN cd frontend && npm install
RUN cd frontend && npm run build
RUN python3 manage.py collectstatic --noinput

ENV C_FORCE_ROOT="true"
CMD ["honcho", "start"]