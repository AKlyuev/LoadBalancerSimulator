import random
import matplotlib.pyplot as plt
import numpy as np

'''
num_clients = 80
packets_per_client = 10
num_load_balancers = 2
num_servers = 4
processing_time = 0.005 # time per packet
'''
num_clients = 1000
packets_per_client = 10
num_load_balancers = 10
num_servers = 100
processing_time = 0.01 # time per packet

assignment_methods = ["RandomAssignment", "ConsistentHashing", "PowersOfTwoNoMemory", "PowersOfTwoWithMemory"]

#class defining a client/host
class Client:
	def __init__(self, address):
		self.id = address

#class defining the load balancer
class LoadBalancer:
	def __init__(self, address):
		self.id = address
		self.connection_table = {}

	def assign_server_random(self, packet, _):
		packet_id = packet.clientid
		return random.randint(0, num_servers - 1)

	def assign_server_hashing(self, packet, _):
		return hash(str(packet.clientid)) % num_servers

	def assign_server_power_of_2_choices_no_memory(self, packet, servers):

		#pick 2 servers randomly
		first_query_server = random.randint(0, num_servers - 1)
		second_query_server = random.randint(0, num_servers - 1)

		#ensure 2nd server is different from 1st
		while (first_query_server == second_query_server):
			second_query_server = random.randint(0, num_servers - 1)

		#get loads of both servers
		first_query_load = servers[first_query_server].get_load(packet.time_sent)
		second_query_load = servers[second_query_server].get_load(packet.time_sent)

		#pick server with least load 
		if first_query_load < second_query_load:
			return first_query_server
		return second_query_server

	def assign_server_power_of_2_choices_with_memory(self, packet, servers):
		#check this is a new flow by checking client id 
		if packet.clientid in self.connection_table:
			return self.connection_table[packet.clientid]

		#pick 2 servers randomly
		first_query_server = random.randint(0, num_servers - 1)
		second_query_server = random.randint(0, num_servers - 1)

		#ensure 2nd server is different from 1st
		while (first_query_server == second_query_server):
			second_query_server = random.randint(0, len(servers) - 1)

		#get loads of both servers
		first_query_load = servers[first_query_server].get_load(packet.time_sent)
		second_query_load = servers[second_query_server].get_load(packet.time_sent)

		#pick server with least load, and store it in the connection table to ensure future consistency
		if first_query_load < second_query_load:
			self.connection_table[packet.clientid] = first_query_server
			return first_query_server
		self.connection_table[packet.clientid] = second_query_server
		return second_query_server

	def __repr__(self):
		return "Load Balancer id: " + str(self.id)	

#class defining a backend server clients are making requests to 
class Server:
	def __init__(self, address):
		self.id = address
		self.packet_history = []

	def add_packet(self, packet):
		self.packet_history.append(packet)

	def clear_packets(self):
		self.packet_history.clear()

	#calculate the amount of time until the queue is theoretically free
	def get_load(self, current_time):
		if len(self.packet_history) == 0:
			return 0
		TTF = 0
		t = 0
		i = 0
		while t < current_time:
			if i >= len(self.packet_history):
				break
			packet_i = self.packet_history[i]
			if packet_i.time_sent > current_time:
				break
			if TTF > 0:
				TTF -= (packet_i.time_sent - t)
				if TTF < 0:
					TTF = 0
			TTF += processing_time
			t = packet_i.time_sent
			i += 1
		TTF -= (current_time - t)
		if TTF < 0:
			TTF = 0
		return TTF

	def __repr__(self):
		string = ""
		for packet in self.packet_history:
			string += str(round(packet.time_sent,3)) + " "
		return "Server id: " + str(self.id) +"\n" + "Packet arrival times: " + string

#class defining a packet
class Packet:
	def __init__(self, clientid, time_sent):
		self.clientid = clientid
		self.time_sent = time_sent

	def __repr__(self):
		return "Packet from client: " + str(self.clientid) + " @time: " + str(round(self.time_sent,3))

def run_plotter(servers, assignment_method):
	# Post-Simulation Analysis
	for server in servers:
		#print(server)
		times = []
		loads = []
		for t in [x/100 for x in range(1, 100)]:
			load = server.get_load(t)
			# print("Load at time", t, "is", round(load, 3))
			times.append(t)
			loads.append(load)

		
		plt.plot(np.array([x for x in times]), np.array([y for y in loads]), label = server.id) # , s=5
		plt.xlabel('Time')
		plt.ylabel('Load (Time til finish)')
		plt.title('Load vs. Time for Servers')

	plt.savefig('plots/BiggerSystem/' + assignment_method + '/LoadVsTimeForServers.png')
	plt.clf()

def run_consistency_check(servers):
	perFlowConsistent = True
	for server in servers:
		for otherServer in servers:
			if server.id != otherServer.id:
				for packet in server.packet_history:
					if packet.clientid in [pckt.clientid for pckt in otherServer.packet_history]:
						perFlowConsistent = False
						break
	if perFlowConsistent:
		print("Per-Flow Consistency Maintained")
	else:
		print("Per-Flow Consistency Not Maintained")


def run_simulation(assignment_method):
	print("running simulation for " + assignment_method)

	# Initialization Steps
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

	# Main Simulation Processing Loop
	for packet in packets:
		lb_id = packet.clientid % num_load_balancers
		load_balancer = load_balancers[lb_id]
		switcher = {
			"RandomAssignment": load_balancer.assign_server_random,  # No per-flow consistency :(
			"ConsistentHashing": load_balancer.assign_server_hashing, # Per-flow consistency :)
			"PowersOfTwoNoMemory": load_balancer.assign_server_power_of_2_choices_no_memory, # No Per-flow consistency :( + Congestion control :)
			"PowersOfTwoWithMemory": load_balancer.assign_server_power_of_2_choices_with_memory # Per-flow consistency :) + Congestion control :) 
		}
		func = switcher.get(assignment_method, lambda: "Invalid assignment method")
		server_id = func(packet, servers)
		server = servers[server_id]
		server.add_packet(packet)
		#print("Load Balancer " + str(lb_id) + " sent packet from client " + str(packet.clientid) + " to server " + str(server_id))

	run_plotter(servers, assignment_method)
	run_consistency_check(servers)


for method in assignment_methods:
	run_simulation(method)


	


