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


# public_key, private_key = rsa.newkeys(
#     2048)
# server_pub_key_bytes = public_key.save_pkcs1(format='DER')

# TODO: Add encrption for privmsg https://devguide.dev/blog/multitenant-backend-with-python-end-to-end-encryption
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html


# TODO:
def broadcast_all(message):
    for user in users.keys():
        msg = message.encode('utf8')
        crypted_msg = rsa.encrypt(msg, users[user].publicKey)
        users[user].client.send(crypted_msg)


def reg_user(message, addr):
    user = users[addr]
    username = ' '.join(message.split()[1:])
    user.user = username
    return f"Welcome {username}"
    # else:
    #     return "Please register a user using USER username to start chatting"


def nick_check(message, addr):
    user = users[addr]
    nick = message.split()[1]
    if nick not in nicks:
        nicks.append(nick)
        user.nick = nick
        return "Please register a user using USER username to start chatting"
    else:
        return "Nick is in use already, please register another NICK"


def privmsg(message, sender):
    receiver = message.split(' ')[1].split(':')[0]
    message_to_send = message.split(':')[1]
    message_to_send = message_to_send.strip()
    for user in users.keys():
        if users[user].user == receiver:
            message_to_send = f"{sender}: {message_to_send}"
            msg = message_to_send.encode('utf8')
            crypted_msg = rsa.encrypt(msg, users[user].publicKey)
            users[user].client.send(crypted_msg)


def message_handle(client, addr):
    connected = True
    while connected:
        try:
            message = client.recv(1024)
            # message = rsa.decrypt(message, private_key)
            message = message.decode('utf8')
            user = users[addr]
            message = message.strip()

            if not message:
                log.warning(f"{user.user} left")
                break

            if ' ' not in message:
                log.warning(
                    f"User inputed invalid command or used a command wrong {message}")
                continue
            command = message.split()[0]
            if user.nick is None and command == 'NICK':
                msg = nick_check(message, addr)
                msg = msg.encode('utf8')
                crypted_msg = rsa.encrypt(msg, user.publicKey)
                client.send(crypted_msg)
            elif user.user is None:
                if command == 'USER':
                    msg = reg_user(message, addr)
                    msg = msg.encode('utf8')
                    crypted_msg = rsa.encrypt(msg, user.publicKey)
                    client.send(crypted_msg)
                else:
                    msg = "Please register a user using USER username to start chatting"
                    msg = msg.encode('utf8')
                    crypted_msg = rsa.encrypt(msg, user.publicKey)
                    client.send(crypted_msg)
            elif command == 'PRIVMSG':
                privmsg(message, user.user)

        except:
            disconnected_nick = users[addr].nick
            users.pop(addr)
            clients.remove(client)
            nicks.remove(disconnected_nick)
            client.close()
            connected = False
            broadcast_all(
                f"SERVER: {disconnected_nick} has disconncted!")
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

        # client.send(server_pub_key_bytes)

        user = User(addr[1], client)
        user.publicKey = pub_key
        users[addr[1]] = user

        thread = threading.Thread(
            target=message_handle, args=(client, addr[1]))
        log.info("waiting for message...")
        thread.start()


if __name__ == '__main__':
    # pub, priv = rsa.newkeys(2048)
    # server_pub_key_bytes = public_key.save_pkcs1(format='DER')
    connection_handler()
