from Point import Point, Vector
import math
from ClassyGraph import ClassyGraph

class Body:
    def __init__(self, massIn, posIn, velIn = None):
        if(velIn == None):
            self.velocity = Vector(0,0)
        else:
             self.velocity = velIn
        self.position = posIn
        self.acceleration = Vector(0,0)
        self.mass = massIn

    #Physics Step
    def step(self, systemAccelIn = Vector(0,0)):
        #print("")
        #print(f"Mass: {self.mass}\tAccel: {self.acceleration.toString()}\t Velocity: {self.velocity.toString()}")
        self.position.add(self.velocity)
        ADD = Vector.sum(self.acceleration, systemAccelIn)
        #print("ADD: " + ADD.toString())
        self.velocity.add(ADD)
        #STATIC IT MAKES ALL THE VARIABLE STATIC
        #print("V: " + self.velocity.toString())

    def checkEdges(self, width = 750, height = 750, radius = 20):
        if(self.position.x + radius > width):
            self.position.x = width - radius
            self.velocity.x *= -1
        if(self.position.x - radius < 0):
            self.position.x = radius
            self.velocity.x *= -1
        if(self.position.y + radius > height):
            self.position.y = height - radius
            self.velocity.y *= -1
        if(self.position.y - radius < 0):
            self.position.y = radius
            self.velocity.y *= -1

class System:
    def __init__(self, systemAccelIn = Vector(0,0)):
        self.v = 26
        self.bodies = [Body(1, Point(0,0), Vector(0,0))] * self.v
        self.N = 0
        self.systemAccel = systemAccelIn
        self.gravitationalConstant = 0.001#100#100#0.001
        self.graph = ClassyGraph(self.v)
    
    #Fg = G m1m2/r^2
    #Ag = C mOTHER/R^2
    def addGravityAccel(self):
        for i in range(len(self.bodies)):
            self.bodies[i].acceleration = Vector(0,0)
        for i in range(len(self.bodies)):
            for j in range(len(self.bodies)):
                if(not(i == j)):
                    #FORCE OF I ON J 
                    #print(i,j)
                    #if(i==0 and j==1):
                    #print("FORCE")
                    b1 = self.bodies[i]
                    b2 = self.bodies[j]
                    distance = Point.distance(b1.position, b2.position)
                    gAccel = (self.gravitationalConstant * b1.mass) / (distance ** 2)#OTHER MASS
                    #print(f"g {gAccel}")
                    rHat = Vector(magnitudeIn = 1, angleIn = b2.position.angleTo(b1.position))
                    #print(f"{i} on {j} R is {rHat.toString()}")
                    rHat = rHat.scalarMultiplication(gAccel)
                    #print(f"R is {rHat.toString()}")
                    b2.acceleration.add(rHat)# = rHat
                    #print(b1.acceleration.toString())
                    #print(b2.acceleration.toString())

    #SI units
        #Distance = Pixel
        #Time     = Step/Tick

    def stepAll(self, useSystemAccel = True):
        self.addGravityAccel()
        for body in self.bodies:
            #print(f"Mass: {body.mass}\tAccel: {body.acceleration.toString()}\t Velocity: {body.velocity.toString()}")
            #print(f"POs: {body.position.toString()}")
            #if(not(body.mass == 1)):
            body.step(systemAccelIn = self.systemAccel if useSystemAccel else Vector(0,0))
            body.checkEdges()

    def polyPoints(self, body1Index, body2Index, rectWidth, screenHeight = 750, drawTupleVersion = True):
        # return [(50,50),(60,40),(80,70),(70,90)]
        b1 = self.bodies[body1Index].position
        b2 = self.bodies[body2Index].position
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
        if(drawTupleVersion):
            return [Point(-w*p/2 + b1.x,w*n/2 + b1.y).drawTuple(screenHeight),Point(w*p/2 + b1.x,-w*n/2 + b1.y).drawTuple(screenHeight),Point(w*p/2 + n + b1.x,-w*n/2 + p + b1.y).drawTuple(screenHeight),Point(-w*p/2 + n + b1.x,w*n/2 + p + b1.y).drawTuple(screenHeight)]
        else:
            return [Point(-w*p/2 + b1.x,w*n/2 + b1.y).tuple(),Point(w*p/2 + b1.x,-w*n/2 + b1.y).tuple(),Point(w*p/2 + n + b1.x,-w*n/2 + p + b1.y).tuple(),Point(-w*p/2 + n + b1.x,w*n/2 + p + b1.y).tuple()]
        

    
    def addBody(self, bodyIn):
        self.bodies[self.N] = bodyIn
        self.N += 1
