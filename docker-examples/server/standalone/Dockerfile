FROM python:3.7-slim

COPY indi /indi/indi/
COPY requirements /indi/requirements/
COPY setup.py /indi/setup.py
RUN pip3 install -e /indi

COPY docker-examples/server/standalone/devices /app/devices/
COPY docker-examples/server/standalone/server.py /app/server.py

EXPOSE 7624
ENTRYPOINT ["python"]
CMD ["/app/server.py"]
