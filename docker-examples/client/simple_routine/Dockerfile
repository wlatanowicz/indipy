FROM python:3.7-slim

RUN apt-get -y update \
 && apt-get -y install git \
 && apt-get -y clean

RUN pip3 install wait-for-dep==0.2.0

ARG INDIPY_BRANCH=master
RUN pip3 install git+https://github.com/wlatanowicz/indipy.git@${INDIPY_BRANCH}


COPY client.py /app/client.py
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/app/client.py"]
