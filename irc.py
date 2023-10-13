import threading 
import socket 
import logging
from dataclasses import dataclass

# @dataclass
# class User:
#     client_addr: str
#     nick: str
#     user: str
#     channels: list
    
log = logging.getLogger(__name__)

bind_addr = ('127.0.0.1', 6841)
server = socket.socket()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(bind_addr)
server.listen()

nicks = []
clients = []


def message_handle(client):
    while True:
        try:
            message = client.recv(1024)
            
            # TODO: implement IRC feeatures
        except:
            # TODO: remove client and nick 
            client.close()
            


def connection_handler():
    while 1:
        client, addr = server.accept()
        log.info(f"a new client from {addr[0]}:{addr[1]} just connected")
        log.info("waiting for message...")
        
        client.send('NICK'.encode())
        nickname = client.recv(1024).decode()
        # TODO: add a checker for dupe nicks, make it a loop and anothe func
        nicks.append(nickname)
        clients.append(client)
        
        thread = threading.Thread(target=message_handle, args=(client,))
        thread.start()
        
        
        



# def nick_func():
#     if ! nick in verified_nicks