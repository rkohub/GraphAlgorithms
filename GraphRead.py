from Point import Point, Vector

#Graph File Parse
#2 Files
#Start with the simple one

f = open("L1Nodes.csv", "r")
fstr = str(f.read())
# print(type(f))
linesArray = fstr.split("\n")
# print(linesArray)


# xCords = []
# yCords = []

names = []

# xMinMinus = 1500
# yMinMinus = 750


for i in range(0,len(linesArray)):
	line = linesArray[i]
	# print(line)
	lineArr = line.split(",")
	print(lineArr)
	if(len(lineArr) > 1):
		names.append(lineArr[0])

f.close()

f = open("L1Edges.csv", "r")
fstr = str(f.read())
# print(type(f))
linesArray = fstr.split("\n")


for i in range(0,len(linesArray)):
	line = linesArray[i]
	# print(line)
	lineArr = line.split(",")
	print(lineArr)
	if(len(lineArr) > 1):
		# names.append(lineArr[0])
		pass


		'''
		if(i == 0):
			labels = lineArr
		else:
			xCords.append(int(lineArr[1]))#-xMinMinus)
			yCords.append(int(lineArr[2]))#-yMinMinus)
			# positions.append(Point(int(lineArr[1])-xMinMinus,int(lineArr[2])-yMinMinus))
			positions.append(Point(int(lineArr[1]),int(lineArr[2])))
		#'''

	'''
	if(line == ''):
		if(doneVertex):
			break
		doneVertex = True
		vertexCount = len(vertexNames)
		for i in range(vertexCount):
			edges.append([0] * vertexCount)
		continue
	if(not doneVertex):
		vertexNames.append(line)
	else:
		vxs = line.split()
		v1 = vxs[0]
		v2 = vxs[1]
		v1Ind = vertexNames.index(v1)
		v2Ind = vertexNames.index(v2)
		edges[v1Ind][v2Ind] += 1
	#'''

# print(edges)

'''
# print(xCords[2],yCords[2])
minX = min(xCords)
maxX = max(xCords)
minY = min(yCords)
maxY = max(yCords)

print(positions[2])
# print(len(positions))

print(minX, maxX, maxX-minX)#1133, Min = 1637, 1500,(1500), 3000
print(minY, maxY, maxY-minY)#1461, Min = 799, 750, (1750), 2500
#'''