import logging
import os
import socket
import utils
from datetime import datetime
from pprint import pprint


class Request:
    def __init__(self, data: bytes):
        self.text = []
        for i in data.decode("utf8", "replace").split("\n"):
            string = i.strip()
            if string:
                self.text.append(string)
        # print(text)

    def getSmth(self):
        return self.text


class Socket:
    def __init__(self, address: str, port: int):
        self.sock = socket.socket()
        self.address = address
        self.port = port
        self.is_open = False

    def __repr__(self):
        return f"<ServerSocket {self.address}:{self.port}>"

    def open(self):
        self.sock.bind((self.address, self.port))
        self.is_open = True

    def close(self):
        self.sock.close()

    def accept(self):
        self.sock.listen(5)
        self._connection, self._user_address = self.sock.accept()
        data = self._connection.recv(512)
        return Request(data).getSmth()

    def send(self, data: bytes):
        self._connection.send(data)


class Server:
    def __init__(self, address="localhost", host=80):
        self.socket = Socket(address, host)

    def start(self):
        self.socket.open()
        while True:
            self.client_request()

    def stop(self):
        self.socket.close()

    def client_request(self):
        pprint(self.socket.accept())
        date = datetime.now()  # "Wed, 21 Oct 2015 07:28:00 GMT"
        content_length = 8000
        content_type = "text/html"
        server_html = "close"

        response = "HTTP/1.1 200 OK\n" \
                   "Content-Type: {}\n" \
                   "Date: {}\n" \
                   "Content-length: {}\n" \
                   "Server: {}\n" \
                   "{}"

        body = utils.read_file("index")
        r = response.format(content_type, date, content_length, server_html, body)
        self.socket.send(r.encode())


if __name__ == "__main__":
    settings = utils.read_config()
    HOST, PORT = settings["ADDRESS"], settings["PORT"]

    server = Server(HOST, PORT)
    server.start()
