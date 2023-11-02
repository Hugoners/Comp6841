import threading
import socket

print("Please register a nick using the command NICK nickname (Must not include space)")
# nickname = input()

bind_addr = ('127.0.0.1', 6441)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(bind_addr)


def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            # if message == 'NICK':
            #     client.send(nickname.encode())
            # else:
            print(message)
        except:
            print('error')
            client.close()
            break


def write():
    while True:
        message = input()
        client.send(message.encode())


receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
