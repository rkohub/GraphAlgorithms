import math

class Point:
    def __init__(self, xIn = None, yIn = None, rIn = None, angleIn = None):
        if(xIn == None and yIn == None):
            self.x = rIn * math.cos(angleIn) #radians
            self.y = rIn * math.sin(angleIn)
            self.r = rIn
            self.angle = angleIn
        else:
            self.r = math.sqrt( ((yIn) ** 2) + ((xIn) ** 2) )
            self.angle = math.atan2(yIn, xIn)
            self.x = xIn
            self.y = yIn

    def toString(self):
        return f"({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def round(self, places = 5):
        #Round X and Y variables
        self.x *= (10 ** places)
        self.y *= (10 ** places)
        self.x = int(self.x)
        self.y = int(self.y)
        self.x /= (10 ** places)
        self.y /= (10 ** places)
        return self

    def nearestUnit(self,num, gridUnit):
        # print(gridUnit, num)
        mult = math.floor(num/gridUnit)
        lowBound = mult * gridUnit
        # print(mult, lowBound)
        retVal = (lowBound + gridUnit) if (num - lowBound > (gridUnit / 2)) else lowBound
        # print(f"Ret {retVal}")
        return retVal

    def snapGridPos(self, gridUnit):
        return Point(self.nearestUnit(self.x,gridUnit), self.nearestUnit(self.y, gridUnit))

    def distanceTo(self, p2):
        x2 = p2.x
        y2 = p2.y
        return math.sqrt( ((y2-self.y) ** 2) + ((x2-self.x) ** 2) )

    def add(self, p2): #Keep me the same type as I was before
        self.x += p2.x
        self.y += p2.y
        #DOESNT UPDATE MAG!!
        #return self

    @staticmethod    
    def sum(p1, p2): #Whatever they are, make a Point
        return Point(xIn = (p1.x + p2.x), yIn = (p1.y + p2.y))

    def tuple(self):
        return (self.x, self.y)

    def drawTuple(self, height):
        return (self.x, height-self.y)

    @staticmethod
    def distance(p1,p2):
        return p1.distanceTo(p2)

    def angleTo(self, p2):
        return math.atan2(p2.y - self.y, p2.x - self.x)

class Vector(Point):
    #Could Store as Complex numbers
    #Still Contemplating which methods should return a vector and which should self modify.
        #Ok Jusr return self
    def __init__(self, xIn = None, yIn = None, magnitudeIn = None, angleIn = None):
        Point.__init__(self, xIn, yIn, magnitudeIn, angleIn)
        #Just making copy variables for better names
        self.magnitude = self.r

    @staticmethod    
    def sum(p1, p2): #Whatever they are, make a Vector
        return Vector(xIn = (p1.x + p2.x), yIn = (p1.y + p2.y))

    def normalize(self):
        return Vector(xIn = (self.x / self.magnitude), yIn = (self.y / self.mag))

    def toString(self):
        return f"{self.x} i, {self.y} j -- Mag: {self.magnitude}, Angle: {self.angle * 180 / math.pi}"

    def __str__(self):
        return f"{self.x} i, {self.y} j -- Mag: {self.magnitude}, Angle: {self.angle * 180 / math.pi}"

    def scalarMultiplication(self, scalar):
        self = Vector(magnitudeIn = self.magnitude * scalar, angleIn = self.angle)
        return self

    
        
# p1 = Point(5,5)
# p2 = Vector(-2,5)
# p1 = Point(rIn = 5, angleIn = math.pi)
# p1 = Point(rIn = 5*math.sqrt(2), angleIn = -math.pi/4)
# print(p1.x,p1.y,p1.r,p1.angle)
# print(p1.toString())
# print(p1.round().toString())
# print(p1.toString())
# print(p1.distanceTo(p2))
# p3 = Vector.sum(p1,p2)
# p3 = Vector.sum(p1,p2)
# print(p3.toString())
# print(p1.toString())
# p1.add(p2)
# print(p1.toString())
