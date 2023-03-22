#Graph File Parse
#2 Files
#Start with the simple one

f = open("graphData.txt", "r")
f = str(f.read())
# print(type(f))
linesArray = f.split("\n")
print(linesArray)

vertexNames = []
doneVertex = False

edges = []
vertexCount = 0

for i in range(0,len(linesArray)):
	line = linesArray[i]
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

print(edges)
