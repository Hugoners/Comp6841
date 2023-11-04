# Comp6841
COMP6841 IRC chat 

Wanted to find a way to have true end to end encryption i.e. client sends some encrypted bytes to the server and the server just sends it to the recipient without the server itself processing the message at all

currently this way works in the way where:

Server: pub, priv key pair

ClientA: pub, priv key pair

ClientB: pub, priv key pair

ClientA joins server -> server sends pub key to clientA for client to communicate to the server through encryption using server pub key and client sends server client pub key

if ClientA wants to send ClientB a message:
clientA sends serverpubkey encrypted message -> server, server decrypts using serverprivkey -> server processes -> server sends clientA's message encrypted in clientB pubkey -> clientB unlocks it with clientB priv key

The goal is still find a way whereby client can go through one client to another without actually getting its contents read at all
However, I felt that given the time invested just in getting server and client working and researching RSA and encryption on top on course material and applying RSA encryption to client server is still pretty cool.
