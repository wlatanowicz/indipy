FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update \
 && apt-get -y install software-properties-common git python3-pip \
 && apt-add-repository -y ppa:mutlaqja/ppa \
 && apt-get -y update \
 && apt-get -y install indi-full gsc \
 && apt-get -y clean

ARG INDIPY_BRANCH=master
RUN pip3 install git+https://github.com/wlatanowicz/indipy.git@${INDIPY_BRANCH}

COPY devices /app/devices/
COPY tty.py /app/tty.py

EXPOSE 7624
ENTRYPOINT ["indiserver"]
