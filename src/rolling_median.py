# Coded by Aman Kochhar
# amanskochhar@gmail.com
# For insight fellowship coding challenge 
# Please read the adjoining readme to see how this works, 
# Also the code is heavily commented to explain what purpose each function serves

import time
import statistics
import sys
import os.path

# starts at the bottom 
############################################################################
# 2. PROCESSING/TIDYING DATA
# this function parses each line to the required format
# IN - lines from .txt file; OUT - timeTracker()
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
	#print("Removed special characters: ",line)
	# changing line to a list datatype for further processing
	line = line.split(" ")
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
# IN - formatLines(); OUT - addNodesEdges(), removeNodesEdges()
############################################################################
# timeLineList to store the times and subsequently, remove "out of window" times from edges dict() and timeLineList
timeLineList = []
# flag for the first run 
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
			#print("Person to remove: ", first)
			for i in edges:
				if remvTimeLine in edges[i]:
					personToRemv = i
					#print("Person to remove: ", personToRemv)
					removeNodesEdges(remvTimeLine, personToRemv)
			# removing all occurences of the timeLine from the timeLineList
			timeLineList = [x for x in timeLineList if x != remvTimeLine]
			# adding the latest transaction
			addNodesEdges(timeLine, firstPerson, secondPerson)
	else:
		timeTrackerSwitch = False
		addNodesEdges(timeLine, firstPerson, secondPerson)

############################################################################
# 4. ADDING NODES/EDGES
# this adds the reqd nodes and edges in the edges dict with there timeLine
# IN - timeTracker(); OUT - medianDegree()
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
	#print("secondPerson", secondPerson,": ", edges[secondPerson])
	
	medianDegree(firstPerson, secondPerson)
	
############################################################################
# 5. REMOVING NODES/EDGES
# this removes the reqd nodes/edges and all its occurences in the edges dict
# IN - timeTracker(); OUT - timeTracker()
############################################################################
def removeNodesEdges(remvTimeLine, personToRemv):
	#uncomment below to see output
	#print("TimeLine out of window: ", remvTimeLine)
	#print("Person to remove values: ", edges[personToRemv])
	misc = len(edges[personToRemv])
	
	if len(edges[personToRemv]) == 2:
		edges[personToRemv].pop()
		edges[personToRemv].pop()
	else:
		for i in range (0, len(edges[personToRemv])):
			if remvTimeLine in edges[personToRemv]:
				index = edges[personToRemv].index(remvTimeLine)
				del edges[personToRemv][index - 1]
				del edges[personToRemv][index - 1]
	
############################################################################
# 6. Calculates median degree of nodes
# this counts degree of a node and saves it in array
# IN - addNodesEdges(); OUT - writeData()
############################################################################
# using dict to make sure we update the previous entry of the person instead of creating a new entry 
medianDegreeDict = {}
# list save the degree of each node to sort and calculate median
medianDegreeList = []
def medianDegree(firstPerson, secondPerson):
		# dividing by 2 to remove the double length of each entry due to timeLine values
		medianDegreeDict[firstPerson] = int(len(edges[firstPerson])/2)
		medianDegreeDict[secondPerson] = int(len(edges[secondPerson])/2)
		medianDegreeList = list(medianDegreeDict.values())
		medianDegreeList.sort()
		
		# ANSWER - for the problem
		#print("{0:.2f}".format(statistics.median(medianDegreeList)))
		
		writeData(medianDegreeList)
	
############################################################################
# 7. WRITING DATA
# this writes median degree in to output.txt
# IN - medianDegree(); OUT - output.txt
############################################################################
def writeData(medianDegreeList):
	output = open("./venmo_output/output.txt", 'a')
	output.write("{0:.2f}".format(statistics.median(medianDegreeList)))
	output.write("\n")
	output.close()
	
############################################################################
# 1. READING DATA/ PREPPING OUTPUT.TXT
# the program starts here
# this preps the output.txt and reads the files and sends it for further processing
# IN - .txt file; OUT - formatLines()
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
	
# open the input file and send lines to formatLines()
with open("./venmo_input/venmo-trans.txt", 'r') as fileToRead:
	line = fileToRead.read()
	
	#print("Raw input:", line)
	
	formatLines(line)