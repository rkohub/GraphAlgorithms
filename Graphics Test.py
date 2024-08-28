import pygame
import sys
import time
import math
import os
from Body import Body, System
from Point import Point, Vector
from ClassyGraph import ClassyGraph
from networkx.algorithms import isomorphism
import networkx as nx
import matplotlib.pyplot as plt

from networkx.generators.nonisomorphic_trees import _layout_to_graph, _next_rooted_tree
from networkx.generators import nonisomorphic_trees


#TODO !!!
#Labels Array
#Anim to Iso's
#Prufer sequence
#Laplatian matrix

#Look at other doc for todo and reecompile list
#Click a key to change color of tool.
#Not perfect Grabbing if close
#UI
#Add arrows to lines
#Vertecess Lower Case
#Edge labels
#Snap To grid?
#Curved Edges (3 point spline, Dragable?)
#BFS, DFS, A*, Dikstra...

#https://networkx.org/documentation/stable/reference/generators.html
#https://pallini.di.uniroma1.it/Introduction.html
#https://pallini.di.uniroma1.it/
#https://stackoverflow.com/questions/42796175/understanding-nauty-algorithm
#https://users.cecs.anu.edu.au/~bdm/papers/orderly.pdf

#Errors
#Cant remove vertecies
#If try to make edge between non existant nodes, the drawing of the edge will crash the program


def addVertex(position):
    ball = Body(1, position, Vector(0,0))
    world.addBody(ball)
    # bodyColors.append(color)
    # world.graph.vertexMade[world.N] = 1

def removeVertex(letter):
    print(F"Delete Vertex {letter}")

def addEdge(letterA, letterB):
    print(F"Make edge {letterA} to {letterB}")
    index1 = ord(letterA) - 65
    index2 = ord(letterB) - 65
    world.graph.addEdge(index1,index2)
    #world.graph.toString()

def removeEdge(letterA, letterB):
    print(F"Remove edge {letterA} to {letterB}")
    index1 = ord(letterA) - 65
    index2 = ord(letterB) - 65
    world.graph.removeEdge(index1,index2)

def createGraphFromFile(fileName):
    f = open(fileName, "r")
    print(f"FN {fileName}")
    f = str(f.read())
    # print(type(f))
    linesArray = f.split("\n")

    graph = None#ClassyGraph()

    #print(linesArray)

    vertexNames = []
    doneVertex = False

    # edges = []
    vertexCount = 0

    for i in range(0,len(linesArray)):
        line = linesArray[i]
        if(line == ''):
            if(doneVertex):
                break
            doneVertex = True
            vertexCount = len(vertexNames)
            graph = ClassyGraph(vertexCount)
            # for i in range(vertexCount):
            #     edges.append([0] * vertexCount)
            continue
        if(not doneVertex):
            vertexNames.append(line)
        else:
            vxs = line.split()
            v1 = vxs[0]
            v2 = vxs[1]
            v1Ind = vertexNames.index(v1)
            v2Ind = vertexNames.index(v2)
            # edges[v1Ind][v2Ind] += 1
            graph.addEdge(v1Ind,v2Ind)


    #print(edges)
    return graph

def genRadialPoints(n):
    r = 200
    points = []
    for i in range(n):
        num = (2 * i * math.pi / n) #+ math.pi/4)
        x = r * math.cos(num)
        y = r * math.sin(num)
        points.append(Point(x,y))
    return points
    
def makeSoftGraph():
    

    f = open("Node.csv", "r")
    fstr = str(f.read())
    linesArray = fstr.split("\n")

    positions = []
    xMinMinus = 1500
    yMinMinus = 750
    names = []

    n = 0

    xPos = []
    yPos = []

    # floors = []
    # buildings = []
    groups = []
    #['L1, 45 Francis', 'L2, Tower', 'L1, Tower', 'L2, 45 Francis', '2, 15 Francis', '2, 45 Francis', '1, 45 Francis', '1, Tower', '2, BTM', '3, BTM', '1, BTM', 'L2, BTM', '1, Shapiro', '2, Shapiro', '3, Shapiro', 'L1, Shapiro', 'L2, Shapiro', '2, Tower', '3, Tower', '3, 45 Francis']

    for i in range(0,len(linesArray)):
        line = linesArray[i]
        # print(line)
        lineArr = line.split(",")
        # print(lineArr)
        if(len(lineArr) > 1):
            if(i == 0):
                pass
            else:
                # combo = lineArr[3] + ", " + lineArr[4]
                # if(combo not in groups):
                #     groups.append(combo)
                
                if(lineArr[3] == "L1"):#and lineArr[4] == "45 Francis"):
                # if(True):
                    # print("N")
                    names.append(lineArr[0])
                    
                    xPos.append(int(lineArr[1]))
                    yPos.append(int(lineArr[2]))
                    n += 1

    margin = 50
    minX = min(xPos) - margin
    minY = min(yPos) - margin
    # print(, min(yPos))
    for i in range(0, len(xPos)):
        positions.append(Point((int(xPos[i]) - minX) * scaleFactor,(int(yPos[i]) - minY) * scaleFactor))


    # print(groups)

    f.close()



    nodeCount = n

    f = open("Edge.csv", "r")
    fstr = str(f.read())
    # print(type(f))
    linesArray = fstr.split("\n")

    graph = ClassyGraph(nodeCount)

    for i in range(0,len(linesArray)):
        line = linesArray[i]
        # print(line)
        lineArr = line.split(",")
        # print(lineArr)
        if(len(lineArr) > 1 and i > 0):
            # names.append(lineArr[0])
            v1 = lineArr[0]
            v2 = lineArr[1]
            try:
                v1Ind = names.index(v1)
                v2Ind = names.index(v2)
                graph.addEdge(v1Ind,v2Ind)
            except:
                pass
    return graph, positions, names


def generateSimpleGraph(n, seed):
    #Seed goes up to #(N-1) * (N-2) / 2
    #seed is a number that, as a binary number represents, an n by n adjacency matrix
    # x,1,1,1
    # x,x,1,1
    # x,x,x,1
    # x,x,x,x (3 * (3-1)/2)

    #10, 001010
    #AC BC
    c = 0
    graph = ClassyGraph(n)
    for i in range(n):
        for j in range(i+1,n):
            if(not i == j):
                val = seed >> c
                if(val % 2):
                    graph.addEdge(i,j)
                # print(i,j)
                c += 1
    return graph


white = [255,255,255]
black = [0,0,0]
brown = [190,130,65]
grey  = [140,140,140]
red   = [200,50,50]
blue  = [100,80,240]
green = [70,200,40]
purple = [80,10,180]
yellow = [200, 200, 50]
orange = [255, 120, 0]
darkBrown = [110,80,70]

scaleFactor = 1#1/2


size = width, height = 1400,750#1500,1750#750,750
# size = width, height = int(1500 * scaleFactor),int(750 * scaleFactor)
screen = pygame.display.set_mode(size)
pygame.init()
#screen.fill(white)

'''
world = System(Vector(0,0))
ball1 = Body(1, Point(width/4, height/2), Vector(0,-1.25))
ball2 = Body(300000, Point(width/2, height/2))
world.addBody(ball1)
world.addBody(ball2)

ballR = 20
#'''

#(0,0) is the bottom Right corner of the screen
#NO DECELRATION

num = 1.366 * 200
q = 0.788675 * 200

'''
ball1 = Body(1,Point(width/4,height/2), Vector(0,-1))#
ball2 = Body(300000, Point(width/2, height/2), Vector(0,0))
ball3 = Body(1,Point(width/2,height/4), Vector(-1,0))
# ball4 = Body(1,Point(width/4,height/4), Vector(0,-2))
world.addBody(ball1)
world.addBody(ball2)
world.addBody(ball3)
# world.addBody(ball4)
#'''

gridUnits = 10#25 * scaleFactor

ballR = 15 * scaleFactor


#0 = Mouse Left, 2 = Mouse Right, assuming then 1 = Mouse middle
mouseLast    = (False,False,False)
mouseNow     = (False,False,False)
mousePressed = (False,False,False)


bodyColors = [red, brown, blue, green, orange, purple, yellow, darkBrown, grey]

grabbed = False
dragging = -1
worldDragging = -1

grabTolerance = ballR * 2

keysLast = pygame.key.get_pressed()
keysNow = pygame.key.get_pressed()

keysArray = [pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z]

characterSequence = []
charAdd = False


def drawWorld(world):
    drawGraph(world.graph, world.bodies, world.id)


lineT = 8 * scaleFactor

def lineCoords(endPoint, pointOffset):
    #Assuming a start at the orign, and the @param, endPoint, describes the positive y direction
    #Make a new point at the @param pointOffset Cooridnates from that new definedY and X Axis's

    b1 = Point(0,0)
    b2 = endPoint

    dy = b2.y - b1.y #Point one at origin (0,0)
    dx = b2.x - b1.x
    l = b1.distanceTo(b2)
    theta = b1.angleTo(b2)
    #https://www.desmos.com/calculator/b9us5sxof2
    #l = length

    w = lineT/l

    p = l * math.sin(theta) #y
    n = l * math.cos(theta) #x

    # print(f"P {p}, N {n}")
    # print(f"PO {pointOffset}")

    xO =  ((pointOffset.x * p) / (2*l)) + ((pointOffset.y * n) / l)
    yO = -((pointOffset.x * n) / (2*l)) + ((pointOffset.y * p) / l)



    # print(f"x0 {xO}, y0 {yO}")

    return Point(xO,yO)

def rectPoints(body1Pos, body2Pos, rectWidth, screenHeight = 750, drawTupleVersion = True):
    # return [(50,50),(60,40),(80,70),(70,90)]
    b1 = body1Pos
    b2 = body2Pos
    # print(f"P {b1},{b2}")
    dy = b2.y - b1.y
    dx = b2.x - b1.x
    l = b1.distanceTo(b2)
    theta = b1.angleTo(b2)
    #https://www.desmos.com/calculator/b9us5sxof2
    w = rectWidth/l
    #l = length
    p = l * math.sin(theta) #y
    n = l * math.cos(theta) #x

    #-wp/2, wp/2, -wp/2 +n, wp/2 +n (Xcords of points)
    #wn/2, -wn/2, wn/2 +p, -wn/2 +p (Ycords of points)

    arrowOut = 20

    topArrow = l - ballR - 2

    arrowL = 20


    offsetRect = [Point(rectWidth,0),Point(rectWidth,l),Point(-rectWidth,l),Point(-rectWidth,0)]
    # offsetRect = [Point(rectWidth,0), Point(rectWidth,topArrow - arrowL),Point(rectWidth + arrowOut,topArrow - arrowL), Point(0,topArrow), Point(-rectWidth - arrowOut,topArrow - arrowL), Point(-rectWidth,topArrow - arrowL), Point(-rectWidth,0)]

    # offsetRect = [Point(rectWidth,0), Point(0,l * 0.9), Point(-rectWidth,0)]

    # print(f"1 {lineCoords()} 2 {()}")

    secondDer = []
    for i in range(0,len(offsetRect)):
        # print(f"P {b1},{b2}")
        newB2 = Point(b2.x, b2.y)
        newB2.subtract(b1)
        # print(f"B2 {newB2}")
        val = lineCoords(newB2, offsetRect[i])
        # val = lineCoords(newB2, Point(10,l/2))
        #print(f"V: {val}")
        val.add(b1)
        # print(f"V{i}: {val}")
        if(drawTupleVersion):
            secondDer.append(val.drawTuple())
        else:
            secondDer.append(val.tuple())

    # print(f"SD: {secondDer}")

    return secondDer

    # ret = []
    # if(drawTupleVersion):
    #     ret = [Point(-w*p/2 + b1.x,w*n/2 + b1.y).drawTuple(screenHeight),Point(w*p/2 + b1.x,-w*n/2 + b1.y).drawTuple(screenHeight),Point(w*p/2 + n + b1.x,-w*n/2 + p + b1.y).drawTuple(screenHeight),Point(-w*p/2 + n + b1.x,w*n/2 + p + b1.y).drawTuple(screenHeight)]
    # else:
    #     ret = [Point(-w*p/2 + b1.x,w*n/2 + b1.y).tuple(),Point(w*p/2 + b1.x,-w*n/2 + b1.y).tuple(),Point(w*p/2 + n + b1.x,-w*n/2 + p + b1.y).tuple(),Point(-w*p/2 + n + b1.x,w*n/2 + p + b1.y).tuple()]
        
    # print(f"RET {ret}")
    # return ret


def drawGraph(graph, positions, worldId):

    #Draw All Edges
    c = -1
    # colors = [7,7,1,1,7,1,7,1,7,3,3,3,3,3,1]
    for v1 in range(0,len(graph.adj)):
        for j in range(0,len(graph.adj[v1].iterable())):
            col = graph.eColorNums[v1].iterable()[j].value
            v2 = graph.adj[v1].iterable()[j].value
            # c += 1

            # if(graph.edgeExists(v1,v2)):
               
                # print("call")n
            rect = rectPoints(positions[v1].position,positions[v2].position,lineT,drawTupleVersion = False)

            pygame.draw.polygon(screen, bodyColors[col], rect)
            # pygame.draw.polygon(screen, bodyColors[c%5 + 2], rect)
            # pygame.draw.polygon(screen, bodyColors[colors[c]], rect)

    #Draw All Nodes
    for i in range(0,graph.v):
        if(dragging == i and worldDragging == worldId):
            # print(f"WID: {worldDragging}, E: {i}")
            positions[i].position = pos

        bodyPos = positions[i].position.tuple()

        pygame.draw.circle(screen, bodyColors[graph.vColorNums[i]], bodyPos, ballR)
        # print(i)

        #A=65
        if pygame.font:
            font = pygame.font.Font(None, 30)

            # text1 = font.render(chr(65+i),1,black)
            text1 = font.render(graph.labels[i],1,black)
            textpos1 = text1.get_rect(x=bodyPos[0] + 20,y=bodyPos[1] - 20)
            screen.blit(text1, textpos1)

def exportGen():
    #/GraphExports/
    fileStr = f"./GraphExports/g{genNum}.txt"
    genGraph.export(file = fileStr)

def checkGenEquivalence():
    folderName = "./GraphExports/"
    genLib = genGraph.makeGraphLib()
    for fileName in os.listdir(folderName):
        if("DS" not in fileName):
            fullName = folderName + fileName
            print(f"FN: {fullName}")
            g = createGraphFromFile(fullName).makeGraphLib()

            #Check other things to equivalnec. (Degree sequence)

            iso = isomorphism.GraphMatcher(genLib,g).is_isomorphic()
            if(iso):
                return True
    return False

def addAllNonIsos(n):
    global genNum, genGraph
    nums = int(((n) * (n-1)) / (2))#int(((n-1) * (n-2)) / (2))
    numGraphs = (2 ** nums)
    for i in range(numGraphs):
        # print(i)

        genLib = genGraph.makeGraphLib()

        deg = genLib.degree
        #print(len(deg))
        #print(deg,type(deg))
        degList = [ deg[i] for i in genLib.nodes()]
        #print(degList,type(degList))
        all3 = True
        for v in degList:
            all3 = all3 and (v == 3)

        # print()

        # if(nx.is_empty(genLib) or nx.is_connected(genLib) and all3):
        # if(nx.is_empty(genLib) or nx.is_connected(genLib)):
        # if(True):
        if((not nx.is_empty(genLib)) and nx.is_connected(genLib) and nx.number_of_nodes(genLib) == 5):
            # print(f"{i}")
            seenB4 = checkGenEquivalence()
            # print(f"seenB4: {seenB4}")
            if(not seenB4):
                print(f"{i}")
                exportGen()

        genNum += 1
        genGraph = generateSimpleGraph(n,genNum)

def getGraphFoler(fileNum):
    folderName = "./GraphExports/"
    # genLib = genGraph.makeGraphLib()
    #print(os.listdir(folderName))
    #print(fileNum)
    fileList = os.listdir(folderName)
    fileCount = len(fileList)
    fileName = fileList[fileNum%fileCount]
    fullName = folderName + fileName
    if("DS" not in fileName):
        g = createGraphFromFile(fullName)
        return g
    else:
        return -1

def setWorldPositions(worldIn, positionsIn):
    bodies = [None] * genGraph.v
    for i in range(genGraph.v):
        bodies[i] = Body(1, positionsIn[i], Vector(0,0))
    worldIn.setBodies(bodies)

def setPosToRadialPoints(worldIn, center):
        # raidalPoints = genRadialPoints(genGraph.v)
        raidalPoints = genRadialPoints(n)
        # raidalPoints = genRadialPoints(10)

        for i in range(genGraph.v):
            # print(i, raidalPoints[i])
            
            raidalPoints[i].add(center)

        setWorldPositions(worldIn,raidalPoints)

def ltg(layout):
    G = nx.Graph()
    stack = []
    for i in range(len(layout)):
        i_level = layout[i]
        if stack:
            j = stack[-1]
            '''
            j_level = layout[j]
            print(f"st0: {stack}, j {j}, J_l {j_level}")
            while j_level >= i_level:
                print(f"st1: {stack}")
                stack.pop()
                print(f"st2: {stack}")
                j = stack[-1]
                #print(j)
                j_level = layout[j]
            #'''
            # G.add_edge(i, j)
            print(i,j)
        stack.append(i)
    return

def _st(layout):
    """Returns a tuple of two layouts, one containing the left
    subtree of the root vertex, and one containing the original tree
    with the left subtree removed."""

    one_found = False
    m = None
    for i in range(len(layout)):
        if layout[i] == 1:
            if one_found:
                m = i
                break
            else:
                one_found = True

    if m is None:
        m = len(layout)

    left = [layout[i] - 1 for i in range(1, m)]
    rest = [0] + [layout[i] for i in range(m, len(layout))]
    return (left, rest)

n = 8
genNum = 0

treeGen = nonisomorphic_trees(n)

# genGraph = generateSimpleGraph(n,genNum)
# genGraph = ClassyGraph.classGraphToGraph(nx.cubical_graph())
genGraph = getGraphFoler(0)

'''
newGraph = createGraphFromFile("./GraphExports/g3.txt")
newGraph2 = createGraphFromFile("./GraphExports/g7.txt")

G1 = newGraph.makeGraphLib()
G2 = newGraph2.makeGraphLib()

GM = isomorphism.GraphMatcher(G1, G2)
print(f"ISO: {GM.is_isomorphic()}")
#'''

world = System()
world.id = 0
world2 = System()
world2.id = 1

worlds = [world,world2]


importWorlds = [1,1]#1 == File/Gen #2 = Soft Enge
canAddVertex = 1

numWorlds = 2;


for i in range(numWorlds):
    importWorld = importWorlds[i]

    if(importWorld == 1):

        canAddVertex = 0

        worlds[i].setGraph(genGraph)

        setPosToRadialPoints(worlds[i], Point(width * ((i * 2) + 1)/4, height/2))   

    if(importWorld == 2):

        canAddVertex = 0

        softGraph, softPoints, labels = makeSoftGraph()

        softBodies = [None] * softGraph.v
        for i in range(softGraph.v):
            softBodies[i] = Body(1, softPoints[i], Vector(0,0))

        world.setGraph(softGraph)
        world.setBodies(softBodies)
        world.graph.setLabels(labels)

# colors = [LinkedList()] * n

linePoints = [0] * n
linePoints2 = [0] * n
linePoints3 = [0] * n

# #C,A,B,D,E
# xs = [100,200,0,300,400]

ret = [(375, 50), (630, 240), (100, 240), (210, 550), (540, 550), (375, 200), (240, 280), (500, 280), (290, 440), (450, 440)]

ret2 = [(530, 120), (590, 300), (420, 190), (420, 410), (530, 480), (170, 120), (60, 190), (240, 300), (60, 410), (170, 480)]

ret3 = [(250, 90), (270, 390), (520, 90), (500, 390), (380, 310), (120, 320), (650, 320), (520, 550), (250, 550), (380, 190)]

ret4 = [(310, 60), (480, 130), (150, 130), (410, 190), (210, 190), (310, 530), (80, 300), (540, 300), (480, 460), (150, 460)]

ret5 = [(340, 100), (520, 170), (170, 170), (440, 630), (250, 630), (340, 370), (80, 330), (610, 330), (580, 510), (110, 510)]

ret6 = [(330, 160), (480, 160), (550, 550), (400, 550), (250, 550), (250, 290), (630, 420), (560, 290), (400, 380), (180, 420)]

ret7 = [(120, 320), (310, 50), (310, 580), (620, 480), (620, 150), (390, 150), (230, 260), (560, 260), (290, 460), (500, 460)]


cube = [(110, 590), (590, 590), (430, 430), (270, 430), (110, 110), (270, 270), (430, 270), (590, 110)]

bip = [(520, 240), (520, 500), (390, 240), (390, 500), (100, 500), (100, 240), (250, 500), (250, 240)]


rets = [cube, bip, ret,ret2,ret3,ret4,ret5,ret6,ret7]

retNum = 1

def rToLP(retNum):
    lp = [0] * n
    for i in range(n):
        lp[i] = Point(rets[retNum][i][0], rets[retNum][i][1])
    return lp



for i in range(n):
    # linePoints[i] = Point(width/2 + 100 + xs[i], height/2)
    linePoints[i] = Point(width/2 + ret[i][0],ret[i][1])
    linePoints3[i] = Point(ret[i][0],ret[i][1])
    linePoints2[i] = Point(ret2[i][0],ret2[i][1])

setWorldPositions(world, rToLP(0))
# setWorldPositions(world2, linePoints)


target = rToLP(1)

# world.graph.eColorNums = colors
# world2.graph.eColorNums = colors

# world.graph.matPlotShow()

# addAllNonIsos(n)
genNum = 0
# genGraph = getGraphFoler(0)

#3,2,0/1,5,8,9,7,4,(Dis),6,10

#9

labels = ["1","2","3","4","5","6"]

# world.graph.setLabels(labels)


start = time.time()

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(white)


    # if(time.time() < start + 20):
    if(True):
        world.stepAll() 
        world.checkIfCloseToTarget(target)
        pygame.draw.circle(screen, grey , (width/2, height/2),20)
    

    #pygame.draw.circle(screen, grey , (width/2, height/2), width/4, width = 1)

    '''
    world.stepAll()
    

    # res = world.polyPoints(0,2, 10, height);
    # print(res)
    # pygame.draw.polygon(screen, black, res)
    
    pygame.draw.circle(screen, brown, ball1.position.drawTuple(height), ballR)
    pygame.draw.circle(screen, grey , ball2.position.drawTuple(height), ballR)
    # pygame.draw.circle(screen, red  , ball3.position.drawTuple(height), ballR)
    # pygame.draw.circle(screen, blue , ball4.position.drawTuple(height), ballR)
    pygame.draw.circle(screen, grey , (width/2, height/2), width/4, width = 1)
    #pygame.draw.circle(screen, black , ball1.position.drawTuple(height), 2)
    # pygame.draw.circle(screen, black , (width/2, height - (height/2 + num - q)), 2)
    #'''
    
    # print(world.polyPoints(1,0))


    #Draw center Line
    th = 6
    l = (width/2) - th/2
    r = (width/2) + th/2
    rect = [Point(l,0).tuple(),Point(l,height).tuple(),Point(r,height).tuple(),Point(r,0).tuple()]
    pygame.draw.polygon(screen, black, rect)


    mouseLast = mouseNow
    mouseNow = pygame.mouse.get_pressed()
    
    mousePressed = [not mouseLast[i] and mouseNow[i] for i in range(0,3)]
    mouseReleased = [mouseLast[i] and not mouseNow[i] for i in range(0,3)]
    #print(mouseLast,mouseNow,mousePressed)

    pos = pygame.mouse.get_pos()
    pos = Point(pos[0], pos[1])

    if(mousePressed[0]):
        grabbed = False

        #Check Distance to all Points and move if close. 
        if(dragging == -1):
            for j in range(len(worlds)):
                curWorld = worlds[j]
                for i in range(0,curWorld.N):
                    dist = (curWorld.bodies)[i].position.distanceTo(pos)
                    # print(f"I {i}, dist {dist}")
                    if (dist < grabTolerance):
                        print("Grab")
                        grabbed = True
                        dragging = i
                        worldDragging = j
                        print(f"WD: {worldDragging}")

        if(not grabbed and canAddVertex):
            snapPos = pos.snapGridPos(gridUnits)
            # print(type(snapPos))
            # print(snapPos)
            # print(snapPos.toString())
            addVertex(snapPos);
            

    if(mouseReleased[0] and not dragging == -1):
        (worlds[worldDragging].bodies)[dragging].position = pos.snapGridPos(gridUnits)
        dragging = -1
        worldDragging = -1

    keysLast = keysNow
    keysNow = pygame.key.get_pressed()
    keysPressed = [not keysLast[i] and keysNow[i] for i in range(0,len(keysNow))]

    if(any(keysPressed)):
        for i in range(0,len(keysArray)):
            if(keysPressed[keysArray[i]]):
                #VD,VC,ED,EC
                if(i == 21): #V = Vertex  
                    #Start vertex stuff
                    print("V")
                    charAdd = True
                    pass

                if(i == 4): #E = Edge  
                    #Start Edge Creation
                    print("E")
                    charAdd = True
                    pass

                if(i == 16 and not charAdd): #Q = Quit  
                    #Start Edge Creation
                    print("Q")
                    pygame.quit()
                    sys.exit()

                if(i == 23 and not charAdd): #X = Export  
                    #Export Graph To File
                    print("X")
                    world.graph.export()
                    # seenB4 = checkGenEquivalence()
                    # print(f"seenB4: {seenB4}")    
                    # if(not seenB4):
                    #     exportGen()

                if(i == 3 and not charAdd): #D = Display  
                    #Export Graph To File
                    print("D")
                    world.graph.matPlotShow()

                if(i == 2 and not charAdd): #C = Copy over
                    #Export Graph To File
                    print("C")
                    world2.graph = world.graph

                if(i == 11 and not charAdd): #L = Layout
                    #Show layout graph
                    print("L")
                    l1 = [0, 1, 2, 1, 2] #Path
                    l2 = [0, 1, 2, 1, 1] #1 Vertex deg 3, rest 2
                    l3 = [0, 1, 1, 1, 1] #1 vertex degree 4

                    # print(_st(l1), _st(l2), _st(l3))

                    ln = _next_rooted_tree(l1)
                    print(l1)
                    G1 = _layout_to_graph(l1)
                    ltg(l1)
                    nx.draw(G1, with_labels=True, font_weight='bold')
                    plt.show()

                if(i == 0 and not charAdd): #A = Animage
                    #Export Graph To File
                    print("A")
                    world.setAnimationSpeed(target)


                if(i == 19 and not charAdd): #T = Tree  
                    #Check if is tree
                    print("T")
                    print(world.graph.isTree())

                if(i == 15 and not charAdd): #P = Position
                    print("P")
                    for b in world.bodies:
                        print(b.position)
                    # print(world.bodies)

                if(i == 13 and not charAdd): #N = Next  
                    #Next Generated Graph
                    print("N")

                    # retNum = (retNum + 1) % 7
                    genNum += 1

                    target = rToLP(genNum % 2)

                    # 
                    # genGraph = getGraphFoler(genNum)
                    # if(genGraph == -1):
                    #     genNum += 1
                    #     genGraph = getGraphFoler(genNum)

                    # genGraph = ClassyGraph.classGraphToGraph(next(treeGen))
                    # # for i in range(numWorlds):
                    # for i in range(1):
                    #     worlds[i].setGraph(genGraph)
                    #     setPosToRadialPoints(worlds[i], Point(width * ((i * 2) + 1)/4, height/2))
                    # genGraph = generateSimpleGraph(n,genNum)
                    

                if(charAdd):
                    characterSequence.append(chr(65+i))
                    print(characterSequence)
                    #print(chr(65+i))
                    if(characterSequence[0] == "E" and len(characterSequence) >= 4):
                        if(characterSequence[1] == "C"):
                            addEdge(characterSequence[2],characterSequence[3])
                            charAdd = False
                            characterSequence = []
                        elif(characterSequence[1] == "D"):
                            removeEdge(characterSequence[2],characterSequence[3])
                            charAdd = False
                            characterSequence = []
                        else:
                            print("Invalid Edge Work")
                            charAdd = False
                            characterSequence = []
                    elif(characterSequence[0] == "V" and len(characterSequence) >= 3):
                        if(characterSequence[1] == "D"):
                            removeVertex(characterSequence[2])
                            charAdd = False
                            characterSequence = []
                        else:
                            print("Invalid Vertex Work")
                            charAdd = False
                            characterSequence = []

    

    drawWorld(world)
    # drawWorld(world2)


    # drawGraph(genGraph, bodies)

    # drawGraph(softGraph, softBodies)
    '''
    #Draw All Edges
    for v1 in range(0,len(world.graph.adj)):
        for j in range(0,len(world.graph.adj[v1].iterable())):
            col = world.graph.eColorNums[v1].iterable()[j].value
            v2 = world.graph.adj[v1].iterable()[j].value
            #print(f"E {v1} to {v2}")
            #print(world.polyPoints(v1,v2,10,height))
            rect = world.polyPoints(v1,v2,10,drawTupleVersion = False)
            # print(res)
            # print(f"it {}")
            # print(col, )
            pygame.draw.polygon(screen, bodyColors[col], rect)

    #Draw All Nodes
    for i in range(0,world.N):
        if(dragging == i):
            (world.bodies)[i].position = pos

        bodyPos = (world.bodies)[i].position.tuple()

        pygame.draw.circle(screen, bodyColors[world.graph.vColorNums[i]], bodyPos, ballR)
        # print(i)

        #A=65
        if pygame.font:
            font = pygame.font.Font(None, 30)

            text1 = font.render(chr(65+i),1,black)
            textpos1 = text1.get_rect(x=bodyPos[0] + 20,y=bodyPos[1] - 20)
            screen.blit(text1, textpos1)
    #'''
    

    
    #Update Display
    pygame.display.flip()

    # time.sleep(1)
    # print("STEP")

