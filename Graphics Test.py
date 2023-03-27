import pygame
import sys
import time
import math
from Body import Body, System
from Point import Point, Vector
from ClassyGraph import ClassyGraph
from networkx.algorithms import isomorphism

#TODO !!!
#Graph Export to file
#Graph to Lib Graph

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


def parseSoftCSV():
    f = open("L1Nodes.csv", "r")
    f = str(f.read())
    linesArray = f.split("\n")
    positions = []
    xMinMinus = 1500
    yMinMinus = 750

    for i in range(0,len(linesArray)):
        line = linesArray[i]
        # print(line)
        lineArr = line.split(",")
        # print(lineArr)
        if(len(lineArr) > 1):
            if(i == 0):
                labels = lineArr
            else:
                positions.append(Point((int(lineArr[1])-xMinMinus) * scaleFactor,(int(lineArr[2])-yMinMinus) * scaleFactor))
    return positions

def makeSoftGraph():
    nodeCount = 46
    f = open("L1Nodes.csv", "r")
    fstr = str(f.read())
    linesArray = fstr.split("\n")
    names = []
    for i in range(0,len(linesArray)):
        line = linesArray[i]
        # print(line)
        lineArr = line.split(",")
        # print(lineArr)
        if(len(lineArr) > 1):
            names.append(lineArr[0])

    f.close()

    f = open("L1Edges.csv", "r")
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
            v1 = lineArr[1]
            v2 = lineArr[2]
            v1Ind = names.index(v1)
            v2Ind = names.index(v2)
            graph.addEdge(v1Ind,v2Ind)
            pass

    return graph




white = [255,255,255]
black = [0,0,0]
brown = [190,130,65]
grey  = [200,200,200]
red   = [200,50,50]
blue  = [50,50,200]

scaleFactor = 1#1/2


size = width, height = 750,750#1500,1750
#size = width, height = int(1500 * scaleFactor),int(1750 * scaleFactor)
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

world = System(Vector(0,0))

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

gridUnits = 25 * scaleFactor

ballR = 15 * scaleFactor


#0 = Mouse Left, 2 = Mouse Right, assuming then 1 = Mouse middle
mouseLast    = (False,False,False)
mouseNow     = (False,False,False)
mousePressed = (False,False,False)


bodyColors = [red, brown]

grabbed = False
dragging = -1

grabTolerance = ballR * 2

keysLast = pygame.key.get_pressed()
keysNow = pygame.key.get_pressed()

keysArray = [pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z]

characterSequence = []
charAdd = False


def drawWorld(world):
    pass


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


def drawGraph(graph, positions):

    #Draw All Edges
    for v1 in range(0,len(graph.adj)):
        for j in range(0,len(graph.adj[v1].iterable())):
            col = graph.eColorNums[v1].iterable()[j].value
            v2 = graph.adj[v1].iterable()[j].value

            # if(graph.edgeExists(v1,v2)):
               
                # print("call")
            rect = rectPoints(positions[v1].position,positions[v2].position,lineT,drawTupleVersion = False)

            pygame.draw.polygon(screen, bodyColors[col], rect)

    #Draw All Nodes
    for i in range(0,graph.v):
        if(dragging == i):
            positions[i].position = pos

        bodyPos = positions[i].position.tuple()

        pygame.draw.circle(screen, bodyColors[graph.vColorNums[i]], bodyPos, ballR)
        # print(i)

        #A=65
        if pygame.font:
            font = pygame.font.Font(None, 30)

            text1 = font.render(chr(65+i),1,black)
            textpos1 = text1.get_rect(x=bodyPos[0] + 20,y=bodyPos[1] - 20)
            screen.blit(text1, textpos1)

newGraph = createGraphFromFile("graphData.txt")
newGraph2 = createGraphFromFile("graphExport2.txt")

G1 = newGraph.makeGraphLib()
G2 = newGraph2.makeGraphLib()

GM = isomorphism.GraphMatcher(G1, G2)
print(f"ISO: {GM.is_isomorphic()}")

raidalPoints = genRadialPoints(newGraph.v)

softGraph = makeSoftGraph()
softPoints = parseSoftCSV()

softBodies = [None] * softGraph.v
for i in range(softGraph.v):
    softBodies[i] = Body(1, softPoints[i], Vector(0,0))



#print(raidalPoints)
bodies = [None] * newGraph.v
for i in range(newGraph.v):
    # print(i, raidalPoints[i])
    center = Point(width/2, height/2)
    raidalPoints[i].add(center)
    bodies[i] = Body(1, raidalPoints[i], Vector(0,0))


# world.graph.matPlotShow()

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(white)


    # world.stepAll()
    # pygame.draw.circle(screen, grey , (width/2, height/2), width/4, width = 1)

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
            for i in range(0,world.N):
                dist = (world.bodies)[i].position.distanceTo(pos)
                if (dist < grabTolerance):
                    print("Grab")
                    grabbed = True
                    dragging = i

        if(not grabbed):
            snapPos = pos.snapGridPos(gridUnits)
            # print(type(snapPos))
            # print(snapPos)
            # print(snapPos.toString())
            addVertex(snapPos);
            

    if(mouseReleased[0] and not dragging == -1):
        (world.bodies)[dragging].position = pos.snapGridPos(gridUnits)
        dragging = -1

    keysLast = keysNow
    keysNow = pygame.key.get_pressed()
    keysPressed = [not keysLast[i] and keysNow[i] for i in range(0,len(keysNow))]

    if(any(keysPressed)):
        for i in range(0,len(keysArray)):
            if(keysPressed[keysArray[i]]):
                #VD,VC,ED,EC
                if(i == 21): #V = Vertex  
                    #Start vertex stuff
                    print("E")
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

                if(i == 3 and not charAdd): #D = Display  
                    #Export Graph To File
                    print("D")
                    world.graph.matPlotShow()

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

    # drawGraph(world.graph, world.bodies)
    # drawGraph(newGraph2, bodies)

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

