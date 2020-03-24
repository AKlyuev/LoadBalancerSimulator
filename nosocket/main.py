import random

'''
from classes import Packet
from classes import LoadBalancer
from classes import Server
'''

num_clients = 8
packets_per_client = 5

num_load_balancers = 2

num_servers = 4

#class defining a client/host
class Client:

	def __init__(self, address):
		self.id = address


class LoadBalancer:

	def __init__(self, address):
		self.id = address

	def assign_server_random(self, packet, version):
		packet_id = packet.clientid
		return random.randint(0, num_servers)


	def assign_server_hashing(self, packet):
		return hash(str(packet.clientid)) % num_servers


	def __repr__(self):
		return "Load Balancer id: " + str(self.id)	


#class defining a backend server clients are making requests to 
class Server:

	#time per packet
	processing_time = 0.1

	def __init__(self, address):
		self.id = address
		self.arrival_times = []
		self.wait_time = 0

	def add_packet(self, packet):
		self.arrival_times.append(packet.time_sent)

	#calculate the amount of time until the queue is theoretically free
	def get_load(self, current_time):
		temp = 0
		i = 0
		while temp < current_time:
			temp = arrival_times[i]
			i++
			self.wait_time += processing_time
			



	def __repr__(self):
		string = ""
		for time in self.arrival_times:
			string += str(round(time,3)) + " "

		return "Server id: " + str(self.id) +"\n" + "Packet arrival times: " + string


class Packet:

	def __init__(self, clientid, time_sent):
		self.clientid = clientid
		self.time_sent = time_sent

	def __repr__(self):
		return "Packet from client: " + str(self.clientid) + " @time: " + str(round(self.time_sent,3))


packets = []
for i in range(num_clients):
	for j in range(packets_per_client):
		packet = Packet(i, random.random())
		packets.append(packet)

packets.sort(key=lambda x: x.time_sent, reverse=False)


load_balancers = []
for i in range(num_load_balancers):
	load_balancer = LoadBalancer(i)
	load_balancers.append(load_balancer)


servers = []
for i in range(num_servers):
	server = Server(i)
	servers.append(server)


for packet in packets:
	lb_id = packet.clientid % num_load_balancers
	load_balancer = load_balancers[lb_id]
	server_id = load_balancer.assign_server_hashing(packet)
	server = servers[server_id]
	server.add_packet(packet)
	print("Load Balancer " + str(lb_id) + " sent packet from client " + str(packet.clientid) + " to server " + str(server_id))

print()

for server in servers:
	print(server)


