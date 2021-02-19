import os

from indi.client import elements
from indi.client.client import Client
from indi.message import const
from indi.transport.client import TCP


host = os.environ.get("INDISERVER_HOST", "indiserver")
port = int(os.environ.get("INDISERVER_PORT", 7624))

control_connection = TCP(host, port)
blob_connection = TCP(host, port)

def client_callback(event):
    print(event)


client = Client(control_connection, blob_connection)
client.onevent(callback=client_callback)
client.start()

while True:
    pass
