import threading
import socket
import logging
import rsa
# from Crypto.PublicKey import RSA
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


# TODO:
# def broadcast_all(message):
#     for client in clients:
#         log.warning(f"why here")
#         msg = message_to_send.encode('utf8')
#             # log.warning(f"here")
#         crypted_msg = rsa.encrypt(msg, users[user].publicKey)
#         users[user].client.send(crypted_msg)
#         client.send(f"SERVER: {message}".encode('utf8'))


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
            # log.warning(f"privhere")
            msg = message_to_send.encode('utf8')
            # log.warning(f"here")
            crypted_msg = rsa.encrypt(msg, users[user].publicKey)
            users[user].client.send(crypted_msg)
            # users[user].client.send(f"hi please work".encode('utf8'))
            # log.info(f"{command}, {receiver}, {message_to_send}")

    # return f"{message_to_send}"


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


def message_handle(client, addr):
    connected = True
    while connected:
        try:
            message = client.recv(1024).decode('utf8')
            user = users[addr]
            log.info(f"line 87: {user.publicKey}")
            log.info(f"{user.nick}")
            log.info(f"{type(user.nick)}")

            # if ' ' not in message:
            #     log.info('here????')
            #     continue

            if user.nick is None:
                # log.info('heresssss')
                # log.info(f"{message}")

                msg = nick_check(message, addr)
                msg = msg.encode('utf8')
                # log.warning(f"this:{user.publicKey}")
                # log.info(f"{rsa.encrypt(msg, user.publicKey)}")

                crypted_msg = rsa.encrypt(msg, user.publicKey)
                # log.info(f"here{crypted_msg}")
                client.send(crypted_msg)
            elif user.user is None:
                msg = reg_user(message, addr)
                msg = msg.encode('utf8')
                # log.warning(f"here")
                crypted_msg = rsa.encrypt(msg, user.publicKey)
                client.send(crypted_msg)
            else:
                # log.warning(f"hereddsadadas")
                privmsg(message)
                # broadcast_all(message)

        except:
            disconnected_nick = users[addr].nick
            users.pop(addr)
            clients.remove(client)
            nicks.remove(disconnected_nick)
            client.close()
            connected = False
            # broadcast_all(
            #     f"{disconnected_nick} has disconncted!".encode('utf8'))
            log.info(f"{users} remaining")


def connection_handler():
    log.info('server is open')
    while 1:
        client, addr = server.accept()
        log.info(client)
        clients.append(client)
        log.info(f"a new client from {addr[0]}:{addr[1]} just connected")

        pub_key_bytes = client.recv(1024)

        pub_key = rsa.PublicKey.load_pkcs1(pub_key_bytes, format='DER')
        # log.warning(f"{pub_key}")

        user = User(addr[1], client)
        user.publicKey = pub_key
        users[addr[1]] = user

        thread = threading.Thread(
            target=message_handle, args=(client, addr[1]))
        log.info("waiting for message...")
        thread.start()


if __name__ == '__main__':
    connection_handler()
