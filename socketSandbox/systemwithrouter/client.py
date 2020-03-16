#this is a client that connects to a server based on the port number and gets data from it. 

import socket
import time

#creates a socket. 
#AF_INET = use address family: internet (IPv4), SOCK_STREAM = type of socket 
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


time.sleep(1)
#tell this socket to try connect to the socket (localhost, 8200). Counterpart of listen()
connection.connect(("localhost", 8200))

while True:

	#recieves any data the server might send
	message = connection.recv(1024)
	print(message.decode("utf-8"))