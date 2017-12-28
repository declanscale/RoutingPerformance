#!/usr/bin/python

import sys, re, math
from graph import *
from routingAlgo import *
#from routingAlgo import *

networkType = sys.argv[1]
routingType = sys.argv[2]
topologyF = sys.argv[3]
workloadF = sys.argv[4]
packetRate = float(sys.argv[5])

myGraph = graph()

with open(topologyF) as fp:
	lines = fp.readlines()

for line in lines:
	#print line
	lineComps = line.rstrip().split(' ')
	nodeFrom = lineComps[0]
	nodeTo = lineComps[1]
	delay = lineComps[2]
	capacity = lineComps[3]
	newEdge = edge(nodeFrom, nodeTo, delay, capacity)
	myGraph.newVertex(nodeFrom, nodeTo, newEdge)
	myGraph.newVertex(nodeTo, nodeFrom, newEdge)

#myGraph.printGraph()

workloadList = []

with open(workloadF) as fp:
	wlLines = fp.readlines()

for line in wlLines:
	lineComps = line.rstrip().split(' ')
	#print lineComps
	workloadList.append(lineComps)
	#lineComps[0] == startTime
	#lineComps[1] == source
	#lineComps[2] == dest
	#lineComps[3] == duration

circuitRouting(workloadList, routingType, myGraph, packetRate)
printPerformance()
