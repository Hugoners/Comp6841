import threading
import socket
import rsa
import logging


print("Please register a nick using the command NICK nickname")
# nickname = input()

bind_addr = ('127.0.0.1', 6841)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(bind_addr)

public_key, private_key = rsa.newkeys(
    2048)
# RSA can only encrypt messages that are smaller than the key the bytes I was sending was too big
pub_key_send = public_key.save_pkcs1(format='DER')
client.send(pub_key_send)

server_key_bytes = client.recv(1024)
server_key = rsa.PublicKey.load_pkcs1(server_key_bytes, format='DER')


def receive():
    while True:
        try:
            message = client.recv(1024)
            message = rsa.decrypt(message, private_key)
            print(message.decode('utf8'))
        except Exception as e:
            logging.error('Error at %s', 'division', exc_info=e)
            client.close()
            break


def write():
    while True:
        message = input()
        message = message.encode('utf8')
        # client.send(message)

        crypted_msg = rsa.encrypt(message, server_key)
        client.send(crypted_msg)


write_thread = threading.Thread(target=write)
write_thread.start()
receive_thread = threading.Thread(target=receive)
receive_thread.start()
