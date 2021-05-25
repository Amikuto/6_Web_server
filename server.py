import socket
import yaml
import os
import utils


def read_config() -> dict:
    """Чтение настроек из файла yaml"""
    with open("settings.yaml", "r") as file:
        return yaml.safe_load(file)


class Socket:
    def __init__(self, host, port, buffer):
        self.host = host
        self.port = port
        self.buffer = buffer

    def __repr__(self):
        return f"<ServerSocket {self.host}:{self.port}>"

    def start(self):
        assert self._socket is None, "ServerSocket уже открыт"
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self._socket.bind((self.host, self.port))
        except Exception:
            self.close()
            raise
        else:
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def close(self):
        assert self._socket is not None, "Данный ServerSocket уже был закрыт"
        if self._connection:
            self._connection.close()
            self._connection = None
        self._socket.close()
        self._socket = None


class Server:
    def __init__(self):
        self.socket = socket.socket()
        self.homedir = os.path.abspath(read_config()["HOMEDIR"])

    def open(self):
        self.socket.bind(('localhost', 80))
        self.socket.listen(5)

    def accept_client(self):
        cli_sock, cli_add = self.socket.accept()


def main():
    server = Server()
    server.open()


if __name__ == "__main__":
    main()



















# sock = socket.socket()
#
# try:
#     sock.bind(('', 80))
#     print("Using port 80")
# except OSError:
#     sock.bind(('', 8080))
#     print("Using port 8080")
#
# sock.listen(5)
#
# conn, addr = sock.accept()
# print("Connected", addr)
#
# data = conn.recv(8192)
# msg = data.decode()
#
# print(msg)
#
# resp = """HTTP/1.1 200 OK
# Server: SelfMadeServer v0.0.1
# Content-type: text/html
# Connection: close
#
# Hello, webworld!"""
#
# conn.send(resp.encode())
#
# conn.close()
