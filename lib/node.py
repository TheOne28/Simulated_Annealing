

class Node:
    def __init__(self, id:int, stasiun: int, model: dict, resource: int ) -> None:
        self.id = id
        self.connection = []
        self.precedence = []
        self.stasiun = stasiun
        self.model = model
        self.resource = resource

    def __init__(self, otherNode):
        self.id = otherNode.id
        self.connection = otherNode.connection
        self.precedence = otherNode.precedence
        self.stasiun = otherNode.stasiun
        self.model = otherNode.model
        self.resource = otherNode.resource  

    def setWaktuSisa(self, waktuSisa: map):
        for key in waktuSisa.keys():
            self.model[key].append(waktuSisa[key])

    def setStasiun(self, stasiun : int):
        self.stasiun = stasiun

    def setResource(self, resource: int):
        self.resource = resource

    def getConnection(self) -> list:
        return self.connection

    def getId(self) -> int:
        return self.id
    
    def getStasiun(self) -> int:
        return self.stasiun

    def getModel(self) -> dict:
        return self.model

    def getResource(self) -> int:
        return self.resource

    def getWaktuSisa(self, model) -> int:
        return self.model[model][1]

    def addModel(self, key: str, value: list):
        self.model[key] = value

    def addConnection(self, friendNode):
        self.connection.append(friendNode)

        if(len(friendNode.precedence) != 0):
            for precend in friendNode.precedence:
                self.precedence.append(precend)
        
        self.precedence.append(friendNode.id)
    
    def isParent(self, listNode: list) -> bool:

        for node in listNode:
            if(node.id in self.precedence):
                return False
        
        return True
    
    def isPrecedence(self, id: int) -> bool:
        return id in self.precedence

    def printNode(self):
        print("id: {}".format(self.id))
        print("Stasiun: {}".format(self.stasiun))
        print("Resource: {}".format(self.resource))
        for i in range(1, len(self.connection) + 1):
            print("Connection{}: {}".format(i, self.connection[i - 1].getId()))
        
        for key in self.model.keys():
            print("Model {}".format(key))
            print("Waktu: {}".format(self.model[key][0]))
            print("Waktu Sisa: {}".format(self.model[key][1]))
        
        print("\n")