class Data():
    def __init__ (self, keyIn = None, valueIn = None):
        self.key   = keyIn
        self.value = valueIn

    def __repr__(self) -> str:
        return f"K: {self.key}, V: {self.value}"

class DataLinked(Data):
    #If no init, does parents. otherwise does this one
    def __init__ (self, dataIn = None, nextIn = None, prevIn = None, keyIn = None, valueIn = None):
        self.next = nextIn
        self.prev = prevIn
        if(not(dataIn == None)):
            Data.__init__(self, dataIn.key, dataIn.value)
        else:
            Data.__init__(self, keyIn, valueIn)

    def unlink(self):
        return Data(self.key, self.value)
