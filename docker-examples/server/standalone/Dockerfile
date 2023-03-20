ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}-slim

RUN apt-get -y update \
 && apt-get -y install git \
 && apt-get -y clean

ARG INDIPY_BRANCH=master
RUN pip3 install git+https://github.com/wlatanowicz/indipy.git@${INDIPY_BRANCH}

COPY devices /app/devices/
COPY server.py /app/server.py

EXPOSE 7624
ENTRYPOINT ["python"]
CMD ["/app/server.py"]
