# Coded by Aman Kochhar
# For insight fellowship coding challenge 
# Please read the adjoining readme to see how this works, 
# also the code is heavily commented to expalian what purpose each function serves

import time
import statistics
import sys
import os.path

# starts at the bottom 
############################################################################
# 2. PROCESSING/TIDYING DATA
# this function parses each line to the required format
# IN - line form .txt file; OUT - timeTracker()
############################################################################
def formatLines (line):
	# removing special characters and unnecessary data from the file
	line = line.replace("{","")
	line = line.replace('"',"")
	line = line.replace("created_time","")
	line = line.replace(",","")
	line = line.replace("target","")
	line = line.replace("actor","")
	line = line.replace("}","")
	line = line.replace(": ","")
	line = line.replace("\n"," ")
	# uncomment below to see output
	#print("Removed special characters: ",line)
	# changing line to a list datatype for further processing
	line = line.split(" ")
	# uncomment below to see output
	#print("Line converted to list datatype: ", line)
	i = 0
	z = len(line) - 3
	while(i <= z):
		timeLine = (line[i])	
		# stripping time for further calculations
		timeLine = timeLine.replace("T"," ")
		timeLine = timeLine.replace("Z"," ")
		timeLine = timeLine.strip()
		#print("Before stripping time: ", timeLine)
		timeLine = time.strptime(timeLine, "%Y-%m-%d %H:%M:%S")
		timeLine = int(time.mktime(timeLine))
		#print("After stripping time: ", timeLine)
		firstPerson = (line[i+1])
		secondPerson = (line[i+2])
		i += 3
		
		timeTracker(timeLine, firstPerson, secondPerson)
		
############################################################################
# 3. HANDLING TIME
# calculates the time and makes sure the 60 sec window is being followed
# IN - called by addNodesEdges; OUT - PROCESSOR()
############################################################################
# timeLineList to store the times and subsequently remove out of window times from edges dict() and timeLineList as well
timeLineList = []
# toggle for the first run 
timeTrackerSwitch = True 
def timeTracker(timeLine, firstPerson, secondPerson):
	global timeTrackerSwitch
	global timeLineList
	timeLineList.append(timeLine)
	timeLineList.sort()
	if timeTrackerSwitch == False:
		lastValIndex = len(timeLineList) - 1
		last = timeLineList[lastValIndex]
		first = timeLineList[0]
		window = last - first
		if window <= 59 and window >= 0:
			addNodesEdges(timeLine, firstPerson, secondPerson)
		else:
			remvTimeLine = first
			#print("remvTimeLine: ", first)
			for i in edges:
				if remvTimeLine in edges[i]:
					personToRemv = i
					#print("personToRemv: ", personToRemv)
					removeNodesEdges(remvTimeLine, personToRemv)
			timeLineList = [x for x in timeLineList if x != remvTimeLine]
			# adding the latest transaction
			addNodesEdges(timeLine, firstPerson, secondPerson)
	else:
		timeTrackerSwitch = False
		addNodesEdges(timeLine, firstPerson, secondPerson)
	
	#print(firstPerson)
	#print(secondPerson)

############################################################################
# 4. ADDING NODES/EDGES
# this adds the reqd nodes and edges in the edges dict
# IN - PROCESSOR(); OUT - PROCESSOR()
############################################################################
edges = dict()
def addNodesEdges (timeLine, firstPerson, secondPerson):
	if firstPerson in edges:
		if secondPerson not in (edges[firstPerson]):
			edges[firstPerson].append(secondPerson)
			edges[firstPerson].append(timeLine)
	else:
		edges[firstPerson] = [secondPerson, timeLine]

	if secondPerson in edges:
		if firstPerson not in (edges[secondPerson]):
			edges[secondPerson].append(firstPerson)
			edges[secondPerson].append(timeLine)
	else:
		edges[secondPerson] = [firstPerson, timeLine]
	
	#uncomment below to see output
	#print("firstPerson", firstPerson,": ", edges[firstPerson])
	#print(len(edges[firstPerson])/2)
	#print("secondPerson", secondPerson,": ", edges[secondPerson])
	#print(len(edges[secondPerson])/2)
	
	medianDegree(firstPerson, secondPerson)
	
############################################################################
# 5. REMOVING NODES/EDGES
# this removes the reqd nodes/edges and all its occurences in the edges dict and timeLineList
# IN - PROCESSOR(); OUT - PROCESSOR()
############################################################################
def removeNodesEdges(remvTimeLine, personToRemv):
	#print("remvTimeLine as is: ", remvTimeLine)
	#print("personToRemv as is: ", personToRemv)
	#print("personToRemv as is values: ", edges[personToRemv])
	
	global timeLineList
	misc = len(edges[personToRemv])
	
	if len(edges[personToRemv]) == 2:
		edges[personToRemv].pop()
		edges[personToRemv].pop()
		# key remains with length zero which will be handled in medianDegree()
	else:
		for i in range (0, len(edges[personToRemv])):
			if remvTimeLine in edges[personToRemv]:
				index = edges[personToRemv].index(remvTimeLine)
				del edges[personToRemv][index - 1]
				del edges[personToRemv][index - 1]
				# key remains with length zero which will be handled in medianDegree()
	
	#uncomment below to see output
	#print("personToRemv", personToRemv,": ", edges[personToRemv])
	#print(len(edges[personToRemv])/2)
	
############################################################################
# 6. Calculates median degree of nodes
# this counts edges of a node and saves it in array
# IN - PROCESSOR(); OUT - PROCESSOR()
############################################################################
# using dict to make sure we update the previous entry of the person instead of creating a new one 
medianDegreeDict = {}
# list save the degree of each node to sort and calculate median
medianDegreeList = []
def medianDegree(firstPerson, secondPerson):
		medianDegreeDict[firstPerson] = int(len(edges[firstPerson])/2)
		medianDegreeDict[secondPerson] = int(len(edges[secondPerson])/2)
		
		# print("firstPerson", firstPerson,": ", edges[firstPerson])
		# print(len(edges[firstPerson])/2)
		# print("secondPerson", secondPerson,": ", edges[secondPerson])
		# print(len(edges[secondPerson])/2)
	
		# uncomment below to see output
		#print(medianDegreeDict)
		medianDegreeList = list(medianDegreeDict.values())
		medianDegreeList.sort()
		# uncomment below to see output
		#print(medianDegreeList)
		print("{0:.2f}".format(statistics.median(medianDegreeList)))
		
		writeData(medianDegreeList)
	
############################################################################
# 7. WRITING DATA
# this writes median degree in to output.txt
# IN - PROCESSOR(); OUT - output.txt
############################################################################
# to clean the previous output file and make sure the program runs on both the shell
# and on the normal execution of the code 
try:
	output = open("./venmo_output/output.txt", 'w')
	output.close()
except:
	os.chdir("../")
	output = open("./venmo_output/output.txt", 'w')
	output.close()
def writeData(medianDegreeList):
	output = open("./venmo_output/output.txt", 'a')
	output.write("{0:.2f}".format(statistics.median(medianDegreeList)))
	output.write("\n")
	output.close()
	
############################################################################
# 1. READING DATA
# this reads the files and sends it for further processing
# IN - .txt file; OUT - formatLines()
############################################################################
# open the input file and send lines to formatLines()
with open("./venmo_input/venmo-trans.txt", 'r') as fileToRead:
	line = fileToRead.read()
	# uncomment below to see output
	#print("Raw read line output:", line)
	
	formatLines(line) 
