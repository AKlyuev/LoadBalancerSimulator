
#class defining a client/host
class Client:

	def __init__(self, address):
		self.id = address




class LoadBalancer:

	def __init__(self, address):
		self.id = address



	def __repr__(self):
		return "Load Balancer id: " + str(self.address)	


#class defining a backend server clients are making requests to 
class Server:

	def __init__(self, address):
		self.id = address

	def __repr__(self):
		return "Server id: " + str(self.address)	

class Packet:

	def __init__(self, clientid):
		self.clientid = clientid



	def __repr__(self):
		return "Packet from client: " + str(self.clientid)