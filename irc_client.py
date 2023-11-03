import threading
import socket
import rsa

print("Please register a nick using the command NICK nickname (Must not include space)")
# nickname = input()

bind_addr = ('127.0.0.1', 6841)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(bind_addr)


def receive():
    # private_key = client.recv(1024)
    # print(private_key)
    while True:
        try:
            message = client.recv(1024).decode('utf8')
            # if message == 'NICK':
            #     client.send(nickname.encode())
            # else:
            print(message)
        except:
            print('error')
            client.close()
            break


def write():
    pub_key, privateKey = rsa.newkeys(2048)

    pub_key = pub_key.save_pkcs1()
    client.send(pub_key)

    while True:
        message = input()
        client.send(message.encode('utf8'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
