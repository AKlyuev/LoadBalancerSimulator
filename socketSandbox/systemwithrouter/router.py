import socket
import time

#make one socket that will be trying to connect to the server
router = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
router.bind(("localhost", 8100)) #im not sure why we need to bind this one to a port. 

#make a second socket that can listen for clients
router_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
router_send.bind(("localhost", 8200))


server = ("localhost", 8000)

#tell this sending socket to listen for clients
router_send.listen(4)


clientConnection = None
while clientConnection == None:
    clientConnection, address = router_send.accept()
    if(clientConnection != None):
        print(clientConnection)
        break

#tell this socket to try connect to the socket (socket.gethostname(), 8000).
router.connect(server) 


while True:
    received_message = router.recv(1024)
    received_message = received_message.decode("utf-8")
    if len(received_message) > 0:
        print("\nMessage: " + received_message)
        
        destinationSocket = clientConnection
        destinationSocket.send(bytes(received_message, "utf-8"))
    time.sleep(2)