import socket


class Server(object):
    def __init__(self):
        self.sock = socket.socket()

    def bind_listen(self, port):
        self.sock.bind(('0.0.0.0', port))
        self.sock.listen(5)

    def accept_receive_close(self):
        conn, address = self.sock.accept()
        msg = conn.recv(1024)
        self.on_msg(msg)
        conn.close()
