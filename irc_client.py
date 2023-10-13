import threading 
import socket 


nickname = input("Choose a nick: ")

bind_addr = ('127.0.0.1', 6841)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(bind_addr)

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print('error')
            client.close()
            break
        
    
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode())

receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)
receive_thread.start()
write_thread.start()
