from tcp_server import Server
from rpc_stub import RPC_STUB
from json_rpc import JSON_RPC


class RPC_SERVER(Server, JSON_RPC, RPC_STUB):
    def __init__(self):
        super().__init__()

    def loop(self):
        self.bind_listen(5000)
        while True:
            self.accept_receive_close()

    def on_msg(self, data):
        self.from_data(data)
        self.call_method()
