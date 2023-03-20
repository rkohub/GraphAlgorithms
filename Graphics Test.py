import pygame
import sys
import time
from Body import Body, System
from Point import Point, Vector

#TODO !!!
#Look at other doc for todo and reecompile list
#Click a key to change color of tool.
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


white = [255,255,255]
black = [0,0,0]
brown = [190,130,65]
grey  = [200,200,200]
red   = [200,50,50]
blue  = [50,50,200]

size = width, height = 750,750
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

gridUnits = 50

ballR = 20


#0 = Mouse Left, 2 = Mouse Right, assuming then 1 = Mouse middle
mouseLast    = (False,False,False)
mouseNow     = (False,False,False)
mousePressed = (False,False,False)


bodyColors = [red, brown]

grabbed = False
dragging = False

grabTolerance = 50

keysLast = pygame.key.get_pressed()
keysNow = pygame.key.get_pressed()

keysArray = [pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z]

characterSequence = []
charAdd = False

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
            addVertex(pos);
            

    if(mouseReleased[0] and not dragging == -1):
        (world.bodies)[dragging].position = pos
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

                if(i == 16): #Q = Quit  
                    #Start Edge Creation
                    print("Q")
                    pygame.quit()
                    sys.exit()

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
            print(col, )
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

    

    
    #Update Display
    pygame.display.flip()

    # time.sleep(1)
    # print("STEP")

