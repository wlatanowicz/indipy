FROM ubuntu:20.04

RUN apt-get update \
 && apt-get install -y software-properties-common

RUN apt-add-repository -y ppa:mutlaqja/ppa \
 && apt-get install -y indi-full gsc

RUN apt-get update \
 && apt-get install -y python3-pip

COPY indi /indi/indi/
COPY requirements /indi/requirements/
COPY setup.py /indi/setup.py
RUN pip3 install -e /indi

COPY docker-examples/server/indilib/devices /app/devices/
COPY docker-examples/server/indilib/tty.py /app/tty.py

EXPOSE 7624
ENTRYPOINT ["indiserver"]
