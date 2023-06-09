from Data import Data
from LinkedList import LinkedList
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import isomorphism

class ClassyGraph():
    def __init__ (self, vIn = 0, adjIn = -1, dataIn = -1, vColorNumsIn = -1, eColorNumsIn = -1):
        self.v = vIn
        if(adjIn == -1):
            self.adj = [None] * self.v
            for i in range(self.v):
                self.adj[i] = LinkedList()
        else:
            self.adj = adjIn

        if(dataIn == -1):
            self.data = [None] * self.v
            for i in range(self.v):
                self.data[i] = Data()
        else:
            self.data = dataIn

        if(vColorNumsIn == -1):
            self.vColorNums = [None] * self.v
            for i in range(self.v):
                self.vColorNums[i] = 0
        else:
            self.vColorNums = vColorNumsIn

        if(eColorNumsIn == -1):
            self.eColorNums = [None] * self.v
            for i in range(self.v):
                self.eColorNums[i] = LinkedList()
        else:
            self.eColorNums = eColorNumsIn
    

    def export(self, file = "graphExport.txt"):
        print("EXPORTED!")
        f = open(file, "w+")
        uen = self.usedEdgeNums()
        #print(uen)
        graphStr = ""
        for i in range(len(uen)):
            val = uen[i]
            graphStr += (chr(65+val) + "\n")
        # print(f"GS: {graphStr}")
        # print("")
        graphStr += "\n"

        for i in range(self.v):
            itt = self.adj[i].iterable()
            for j in itt:
                val = j.value
                graphStr += (chr(65+i) + " " + chr(65+val) + "\n")

        f.write(graphStr)
        f.close()

    def clearGraph(self):
        self = self.__init__()

    def usedEdgeNums(self):
        used = []
        for i in range(self.v):
            itt = self.adj[i].iterable()
            leng = len(itt)
            if(leng > 0):
                if(i not in used):
                    used.append(i)
                for j in itt:
                    val = j.value
                    # print(f"V {val}")
                    if(val not in used):
                        used.append(val)
        used.sort()
        return used

    def vertexExists(self, v):
        return v >= 0 and v < self.v

    def edgeExists(self, vTo, vFrom):
        return self.vertexExists(vTo) and self.adj[vTo].contains(vFrom)

    def addDirectedEdge(self, vTo, vFrom):
        if not(self.vertexExists(vTo)) or not(self.vertexExists(vFrom)):
            print("Cant make a edge to or from a vertex that isn't in the graph")
            return
        self.eColorNums[vTo].add(1)
        self.adj[vTo].add(vFrom)

    def addEdge(self, vTo, vFrom):
        self.addDirectedEdge(vTo, vFrom)

    def removeEdge(self, vTo, vFrom):
        if(self.edgeExists(vTo,vFrom)):
            #convert to str, because key is str version of value which is a number
            self.adj[vTo].remove(str(vFrom))
        else:
            print("Edge Doesn't Exist!")

    def addBidirectedEdge(self, v1, v2):
        self.addDirectedEdge(v1, v2)
        self.addDirectedEdge(v2, v1)

    def toString(self):
        for i in range(self.v):
            #print(f"Vertex {i} with adacent Edges {g.adj[i].iterable()}")
            print(f"Vertex {i} with adacent Edges {self.adj[i].values()}")

    def __str__(self):
        for i in range(self.v):
            #print(f"Vertex {i} with adacent Edges {g.adj[i].iterable()}")
            print(f"Vertex {i} with adacent Edges {self.adj[i].values()}")

    def makeGraphLib(self):
        G = nx.Graph()
        for i in range(self.v):
            itt = self.adj[i].iterable()
            for j in itt:
                val = j.value
                G.add_edge(chr(65+i), chr(65+val))
        return G

    def matPlotShow(self):
        G1 = self.makeGraphLib()
        nx.draw(G1, with_labels=True, font_weight='bold')
        plt.show()

    def isTree(self):
        G = self.makeGraphLib()
        return nx.is_tree(G)


# g = ClassyGraph(5)
# g.addEdge(2,3)
# # g.addEdge(2,1)
# # g.addEdge(2,4)
# g.addEdge(4,0)
# g.toString()
# print(g.edgeExists(0,4))
# print(g.edgeExists(5,0))
# print(g.edgeExists(2,3))
# g.removeEdge(2,3)
# g.toString()