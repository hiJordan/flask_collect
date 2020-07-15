from rpc_client import Rpc_Client

m_client = Rpc_Client()
m_client.connect('127.0.0.1', 5000)
m_client.bar(1, 2, c=3)

