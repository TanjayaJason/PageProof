import socket
import pytest

@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """Allow Windows asyncio's loopback socketpair, block external connections."""
    def guard(original):
        def connect(sock, address):
            if isinstance(address, tuple) and address[0] in ('127.0.0.1', '::1'):
                return original(sock, address)
            raise AssertionError('External network calls are forbidden in offline tests')
        return connect
    monkeypatch.setattr(socket.socket, 'connect', guard(socket.socket.connect))
    monkeypatch.setattr(socket.socket, 'connect_ex', guard(socket.socket.connect_ex))
