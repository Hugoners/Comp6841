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
    2048)  # change to 2048 later
# RSA can only encrypt messages that are smaller than the key the byte I was sending was too big
pub_key_send = public_key.save_pkcs1(format='DER')


def receive():
    while True:
        try:
            # if message == 'EW!#&@*!(&#(*!@CREATE_KEY_NOW_PLEASE@!#!@#@!%@!*$&@!#@!':
            #     public_key, private_key = rsa.newkeys(
            #         512)  # change to 2048 later
            #     priv_key = private_key
            #     pub_key = public_key
            #     public_key = public_key.save_pkcs1(format='DER')
            #     client.send(pub_key)
            # else:
            message = client.recv(1024)
            # print(message)
            # if priv_key is None:
            #     print('error')
            #     client.close()
            #     break
            # else:
            message = rsa.decrypt(message, private_key)
            print(message.decode('utf8'))
            # print(message)
        except Exception as e:
            logging.error('Error at %s', 'division', exc_info=e)
            # print('error')
            client.close()
            break


def write():
    client.send(pub_key_send)
    while True:
        message = input()
        client.send(message.encode('utf8'))


write_thread = threading.Thread(target=write)
write_thread.start()
receive_thread = threading.Thread(target=receive)
receive_thread.start()
