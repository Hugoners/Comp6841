# import threading 
# import socket 
# import logging

# log = logging.getLogger(__name__)

# class IRCServer():
#     server = socket.socket()
     
#     def __init__(self, bind_addr):
#         self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server.bind(bind_addr)
        
#     def connection_handler(self):
#         while 1:
#             client, address = self.server.accept()
#             log.info(f"a new client from {address} just connected")
            

            
            

    

# # def new_client():
# #     while True:
# #         client, address = server.accept()

# def main():
#     bind_addr = ('127.0.0.1', 6841)
#     server = IRCServer(bind_addr)
        
# if __name__ == '__main__':
#     main()
