#this is a server that will send a message to any client that connects to it. We can use this example of the end servers that 
#the hosts are trying to connect to. We'll know the have connected when they recieve the message.

import socket

#creates a socket. 
#AF_INET = use address family: internet (IPv4), SOCK_STREAM = type of socket 
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#binds the socket to the host name and port number, in this case port 8000 on our computer (I think)
connection.bind((socket.gethostname(), 8000))

#Defines the server by telling the socket to listen for clients. 5 is the number of connections that can be in the queue at once
connection.listen(5)

while True:
	connectedsocket, address = connection.accept()
	print("Connection from {address} established".format(address = address))
	connectedsocket.send(bytes("First message", "utf-8"))

	