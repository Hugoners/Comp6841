import threading
import socket
import logging
from Crypto.PublicKey import RSA
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
    ret_addr: int
    client: socket
    publicKey = rsa.key.PublicKey = None
    nick: str = None
    user: str = None
    channels: list = None


nicks = []
clients = []
users = {}


# TODO: Add encrption for privmsg https://devguide.dev/blog/multitenant-backend-with-python-end-to-end-encryption
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html

def broadcast_all(message):
    for client in clients:
        client.send(f"SERVER: {message}".encode('utf8'))


def nick_check(message, addr):
    user = users[addr]
    nick = message.split()[1]
    command = message.split()[0]
    if command == 'NICK' and nick not in nicks:
        nicks.append(nick)
        user.nick = nick
        return "Please register a user using USER username to start chatting"
    else:
        return "Nick is in use already, please register another NICK"


def reg_user(message, addr):
    user = users[addr]
    command = message.split()[0]
    if command == 'USER':
        username = ' '.join(message.split()[1:])
        user.user = username
        return f"Welcome {username}"
    else:
        return "Please register a user using USER username to start chatting"


def privmsg(message):
    command = message.split(' ')[0]
    receiver = message.split(' ')[1].split(':')[0]
    message_to_send = message.split(':')[1]

    for user in users.keys():
        if users[user].user == receiver:
            users[user].client.send(f"hi please work".encode('utf8'))
            log.info(f"{command}, {receiver}, {message_to_send}")

    # return f"{message_to_send}"


def message_handle(client, addr):
    connected = True
    while connected:
        try:
            message = client.recv(1024)
            log.info(f"{message}")
            rsa.key.PublicKey.load_pkcs1(message.encode('utf8'))
            # log.warning(f"{b}")
            log.info(f"{client}, {message}")
            # command = message.split()[0]
            user = users[addr]

            if ' ' not in message:
                continue

            if user.nick is None:
                msg = nick_check(message, addr)
                client.send(msg.encode('utf8'))
            elif user.user is None:
                msg = reg_user(message, addr)
                client.send(msg.encode('utf8'))
            else:
                privmsg(message)
                broadcast_all(message)
            # # log.warning(message)
            # client_port = client.getsockname()[1]
            # log.info(users.get(addr))

            # TODO: implement PRIV message -> all in on privmsging -> encryption
        except:
            # TODO: remove client and nick
            disconnected_nick = users[addr].nick
            users.pop(addr)
            clients.remove(client)
            nicks.remove(disconnected_nick)
            client.close()
            connected = False
            broadcast_all(
                f"{disconnected_nick} has disconncted!".encode('utf8'))
            log.info(f"{users} remaining")


def connection_handler():
    log.info('server is open')
    while 1:
        client, addr = server.accept()
        log.info(client)
        log.info(f"a new client from {addr[0]}:{addr[1]} just connected")
        log.info("waiting for message...")

        # client.send('NICK'.encode())
        # nickname = client.recv(1024).decode()
        # nicks.append(nickname)
        clients.append(client)
        # publicKey, privateKey = rsa.newkeys(512)
        # client.send(privateKey)
        user = User(addr[1], client)
        users[addr[1]] = user

        # # log.info(f"{type(publicKey)}, {type(privateKey)}")
        # log.info(f"{publicKey}")
        # log.info(f"{privateKey}")

        # test_message = 'h'.encode('utf8')
        # test = rsa.encrypt(test_message, publicKey)
        # log.info(f"{test}")
        # log.info(f"{type(test)}")
        thread = threading.Thread(
            target=message_handle, args=(client, addr[1]))
        thread.start()


if __name__ == '__main__':
    connection_handler()
