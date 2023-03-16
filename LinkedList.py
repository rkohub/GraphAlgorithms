from Data import Data, DataLinked

#Create something like sub classes in here that are like stack and queue
#also 

#Linked list, double pointed, using sentinels
class LinkedList():
    def __init__ (self):
        self.head = DataLinked(keyIn = "Sentinel Head")
        self.tail = DataLinked(keyIn = "Sentinel Tail")
        self.head.next = self.tail
        self.tail.prev = self.head
        self.N = 0
        
    def addData(self, dataIn):
        added = DataLinked(dataIn)
        added.next = self.tail
        added.prev = self.tail.prev
        self.tail.prev.next = added
        self.tail.prev = added
        self.N += 1

    def add(self, valueIn):
        data = Data(str(valueIn), valueIn)
        self.addData(data)

    def remove(self, keyIn):
        print(f"remove {keyIn}")
        if(self.containsKey(keyIn)):
            curr = self.head

            while(not keyIn == curr.key):
                curr = curr.next

            curr.prev.next = curr.next
            curr.next.prev = curr.prev
            self.N -= 1
        else:
            print("No remove, because key not in list!")

    def iterable(self):
        arr = [None] * self.N
        pos = self.head.next
        for i in range(len(arr)):
            arr[i] = pos.unlink()
            pos = pos.next
        return arr

    def keys(self):
        arr = [None] * self.N
        itt = self.iterable()
        for i in range(0,len(itt)):
            arr[i] = itt[i].key
        return arr

    def values(self):
        arr = [None] * self.N
        itt = self.iterable()
        for i in range(0,len(itt)):
            arr[i] = itt[i].value
        return arr

    def copy(self):
        newLL = LinkedList()
        itt = self.iterable()
        for i in range(0,len(itt)):
            newLL.addData(itt[i])
        return newLL

    #def containsData(self, data):

    def containsValue(self, value):
        return value in self.values() 

    def containsKey(self, key):
        return key in self.keys() 

    def contains(self, value):
        return self.containsValue(value)
            

# ll = LinkedList()
# print(ll.head.key)
# print(ll.tail.key)
# print(ll.tail.prev.key)

# d = Data("K","V")
# print(d.value)
# ll.addData(d)
# ll.addData(d)
# print(ll.head.key)
# print(ll.iterable())
# print(ll.keys())
# print(ll.values())


