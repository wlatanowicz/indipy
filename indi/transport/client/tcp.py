import logging
import socket
import threading

from indi.transport import Buffer


class ConnectionHandler:
    def __init__(self, client_socket, callback):
        self.buffer = Buffer()
        self.client_socket = client_socket
        self.callback = callback
        self.sender_lock = threading.Lock()

    def wait_for_messages(self):
        while True:
            logging.debug(f"TCP: waiting for data")
            message = self.client_socket.recv(1024)
            if not message:
                logging.debug(f"TCP: no data, breaking")
                break
            logging.debug(f"TCP: got data: {message}")
            self.buffer.append(message.decode("latin1"))
            self.buffer.process(self.message_from_server)

    def message_from_server(self, message):
        if self.callback:
            self.callback(message)

    def send_message(self, message):
        data = message.to_string()
        with self.sender_lock:
            logging.debug(f"TCP: sending data: {data}")
            self.client_socket.sendall(data)

    def close(self):
        if self.client_socket:
            self.client_socket.close()


class TCP:
    def __init__(self, address="127.0.0.1", port=7624):
        self.address = address
        self.port = port

    def connect(self, callback):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.address, self.port))
        handler = ConnectionHandler(sock, callback)

        handler_thread = threading.Thread(
            target=handler.wait_for_messages,
            daemon=True,
        )
        handler_thread.start()

        return handler
