class graph:
	def __init__(self):
		self.vertices = {}

	def newVertex(self, vertex, vertex2, edge):
		if vertex not in self.vertices:
			self.vertices[vertex] = {}
		self.vertices[vertex][vertex2] = edge
	#	print self.vertices[vertex]
	def printGraph(self):
		for vertex in self.vertices:
			for vertex2 in self.vertices[vertex]:
				print self.vertices[vertex][vertex2]


class edge:
	def __init__(self, vertexFrom, vertexTo, delay, capacity):
		self.nodeFrom = vertexFrom
		self.nodeTo = vertexTo
		self.delay = float(delay)
		self.capacity = int(capacity)
		self.load = 0
		#endTime list for used edge
		self.timeList = []
		#print self.nodeFrom + self.nodeTo + str(self.delay) + str(self.capacity) + str(self.load)
		#print self.timeList
	def updateEdge(self, startTime, duration):
		for time in self.timeList:
			if time <= startTime:
				self.timeList.pop(self.timeList.index(time))
				self.load -= 1
				#print "pop one\n"
		endTime = startTime + duration
		self.timeList += [endTime]
		self.load += 1
		#print "update one\n"

	def getLoadRatio(self, startTime):
		inUse = 0
		for time in self.timeList:
			if time > startTime:
				inUse += 1
		return float(inUse)/float(self.capacity)

	def __str__(self):
		return str(self.nodeFrom) + str(self.nodeTo) + str(self.delay) + str(self.capacity) + str(self.load)


