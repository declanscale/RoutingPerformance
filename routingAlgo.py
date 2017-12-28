#routing algo, SHP, SDP, LLP

import sys, math, random
from graph import *


totalPackets = 0
successPackets = 0
successCircuit = 0
totalHops = 0
totalDelay = 0
totalRequest = 0

def circuitRouting (wlLines, routingType, myGraph, packetRate):

	global totalPackets
	global successPackets
	global successCircuit

	for wlLine in wlLines:
		#print wlLine
		packets = int(math.floor(packetRate * float(wlLine[3])))
		#print packets
		totalPackets += packets
		if routingType == "SHP" :
			result = shp(str(wlLine[1]), str(wlLine[2]), float(wlLine[0]), float(wlLine[0])+float(wlLine[3]), myGraph)
		if routingType == "SDP" :
			result = sdp(str(wlLine[1]), str(wlLine[2]), float(wlLine[0]), float(wlLine[0])+float(wlLine[3]), myGraph)
		if routingType == "LLP" :
			result = llp(str(wlLine[1]), str(wlLine[2]), float(wlLine[0]), float(wlLine[0])+float(wlLine[3]), myGraph)
		successPackets += (result * packets)
		successCircuit += result

def checkAvailablity(myGraph, startTime, nodeFrom, nodeTo):
	free = 0
	for time in myGraph.vertices[nodeFrom][nodeTo].timeList:
		if time <= startTime:
			free += 1
	return (float(myGraph.vertices[nodeFrom][nodeTo].load) - float(free)) / float(myGraph.vertices[nodeFrom][nodeTo].capacity)

def shp (source, target, startTime, endTime, myGraph):

	global totalHops
	global totalDelay
	global totalRequest
	
	totalRequest += 1 #every time enter this function means have a new request
	
	## Dijkstra Algorithem
	
	vertex_set = {}
	dist = {}
	prev = {}
	dist[source] = 0
	prev[source] = "UNDEFINED"
	#print source
	for vertex in myGraph.vertices.keys():
		if vertex != source :
			dist[vertex] = sys.maxsize # set to infinit
			prev[vertex] = "UNDEFINED"
		vertex_set[vertex] = dist[vertex]

	#print vertex_set
	cur_node = source
	target_node = target

	while cur_node != target_node :
		vertex_set.pop(cur_node)
		connect_to_cur = myGraph.vertices.get(cur_node)
		for vertex in connect_to_cur.keys():
			alt = dist[cur_node] + 1
			if (alt < dist[vertex]):
				dist[vertex] = alt
				prev[vertex] = cur_node
				vertex_set[vertex] = dist[vertex]
		cur_node = sorted(vertex_set, key = vertex_set.get)[0]
	
	block = 1
	circuitDelay = 0
	circuitDistance = 0
	backword = target_node
	while (prev[backword] != "UNDEFINED") :
		if checkAvailablity(myGraph, startTime, prev[backword], backword) == 1:
			block = 0
		#print prev[backword], backword
		circuitDelay += myGraph.vertices.get(prev[backword]).get(backword).delay
		circuitDistance += 1
		backword = prev[backword]

	backword = target_node
	while (prev[backword] != "UNDEFINED" and block == 1) :
		myGraph.vertices.get(prev[backword]).get(backword).updateEdge(startTime, endTime-startTime)
		backword = prev[backword]

	totalHops += (block * circuitDistance)
	totalDelay += (block * circuitDelay)
	return block
	
def sdp(source, target, startTime, endTime, myGraph):
	global totalHops
	global totalDelay
	global totalRequest
	
	totalRequest +=1
	
	#Dijastra algorithem
	
	vertex_set = {}
	#dist = {} #store the number of hops
	prev = {}
	delay_set = {} # store the total delay
	
	delay_set[source] = 0
	prev[source] = "UNDEFINED"
	
	for vertex in myGraph.vertices.keys():
		if vertex != source:
			#dist[vertex] = sys.maxsize
			delay_set[vertex] = sys.maxsize
			prev[vertex] = "UNDEFINED"
		vertex_set[vertex] = delay_set[vertex]
		
	cur_node = source
	target_node = target
	
	while cur_node != target_node:
		vertex_set.pop(cur_node)
		connect_to_cur = myGraph.vertices.get(cur_node)
		for vertex in connect_to_cur.keys():
			alt = delay_set[cur_node] + connect_to_cur.get(vertex).delay
			if(alt < delay_set[vertex]):
				delay_set[vertex] = alt
				prev[vertex] = cur_node
				vertex_set[vertex] = delay_set[vertex]
		cur_node = sorted(vertex_set, key = vertex_set.get)[0]
		
	block = 1
	circuitDelay = 0
	circuitDistance = 0
	backword = target_node
	while(prev[backword] != "UNDEFINED"):
		if checkAvailablity(myGraph, startTime, prev[backword], backword) == 1:
			block = 0
			
		circuitDelay += myGraph.vertices.get(prev[backword]).get(backword).delay
		circuitDistance += 1
		backword = prev[backword]
		
	backword = target_node
	while(prev[backword] != "UNDEFINED" and block == 1):
		myGraph.vertices.get(prev[backword]).get(backword).updateEdge(startTime,endTime - startTime)
		backword = prev[backword]
		
	totalHops += (block * circuitDistance)
	totalDelay += (block * circuitDelay)
	return block
	
def llp(source, target, startTime, endTime, myGraph):
	
	global totalHops
	global totalDelay
	global totalRequest
	
	totalRequest+=1
	
	load = {}
	prev = {}
	vert = {}	

	load[source] = 0
	prev[source] = "UNDEFINED"
	
	for vertex in myGraph.vertices.keys():
		if vertex != source:
			load[vertex] = 2
			prev[vertex] = "UNDEFINED"
		vert[vertex] = load[vertex]

	curr = source
	targ = target

	while (	curr != targ ) :
		vert.pop(curr)
		toVisit = myGraph.vertices.get(curr)
		for vertex in toVisit:
			ratio = myGraph.vertices.get(curr).get(vertex).getLoadRatio(startTime)
			if load[vertex] > max(ratio, load[curr]) :
				load[vertex] = max(ratio, load[curr])
				prev[vertex] = curr
				vert[vertex] = load[vertex]
		curr = sorted(vert, key = vert.get)[0]
	
	backword = targ
	if(load[backword] == 1):
		return 0
	
	circuitDelay = 0
	circuitDistance = 0
	
	while(prev[backword] != "UNDEFINED"):
		circuitDelay += myGraph.vertices.get(prev[backword]).get(backword).delay
		circuitDistance += 1
		backword = prev[backword]
		
	backword = target
	while(prev[backword] != "UNDEFINED"):
		myGraph.vertices.get(prev[backword]).get(backword).updateEdge(startTime,endTime - startTime)
		backword = prev[backword]
		
	totalHops += circuitDistance
	totalDelay += circuitDelay
	return 1
					

def printPerformance() :
	print "Total number of virtual circuit requests: %d" % totalRequest
	print "Total number of packets: %d" % totalPackets
	print "Number of successfully routed packets: %d" % successPackets
	print "Percentage of successfully routed packets: %0.2f" % float(float(successPackets)/float(totalPackets)*100)
	print "Number of blocked packets: %d" % int(totalPackets - successPackets)
	print "Percentage of blocked packets: %0.2f" % (float(1-(float(successPackets)/float(totalPackets)))*100)
	print "Average number of hops per circuit: %0.2f" % (float(totalHops)/float(successCircuit))
	print "Average cumulative propagation delay per circuit: %0.2f" % (float(totalDelay)/float(successCircuit))
	
