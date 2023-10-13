import threading
import socket
import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

bind_addr = ('127.0.0.1', 6841)
server = socket.socket()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(bind_addr)
server.listen()


@dataclass
class User:
    port: int
    nick: str
    user: str = None
    channels: list = None


nicks = []
clients = []

users = {}


def broadcast_all(message):
    for client in clients:
        client.send(message)


def message_handle(client, addr):
    connected = True
    while connected:
        try:
            message = client.recv(1024)
            broadcast_all(message)
            # log.warning(message)
            # client_port = client.getsockname()[1]
            # log.info(users.get(addr))

            # TODO: implement IRC feeatures
        except:
            # TODO: remove client and nick
            log.info(users.get(addr))
            clients.remove(client)
            client.close()
            connected = False
            broadcast_all(f" has disconncted!".encode())


def connection_handler():
    log.info('server is open')
    while 1:
        client, addr = server.accept()
        log.info(f"a new client from {addr[0]}:{addr[1]} just connected")
        log.info("waiting for message...")

        client.send('NICK'.encode())
        nickname = client.recv(1024).decode()
        # TODO: add a checker for dupe nicks, make it a loop and anothe func
        nicks.append(nickname)
        clients.append(client)
        client_port = client.getsockname()[1]
        user = User(addr, nick=nickname)
        users[addr] = user

        thread = threading.Thread(target=message_handle, args=(client, addr))
        thread.start()


connection_handler()


# def nick_func():
#     if ! nick in verified_nicks
