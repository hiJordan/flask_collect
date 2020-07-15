import socket


class Client(object):
    def __init__(self):
        self.sock = socket.socket()

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, data):
        self.sock.send(data)


if __name__ == '__main__':
    client = Client()
    client.connect('127.0.0.1', 5000)
    client.send("shit".encode('utf-8'))
