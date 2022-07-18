

class Node:
    def __init__(self, id:int, stasiun: int, model: dict, resource: int ) -> None:
        self.id = id
        self.connection = []
        self.precedence = []
        self.stasBefore = []
        self.stasiun = stasiun
        self.model = model
        self.resource = resource

    def setWaktuSisa(self, waktuSisa: map):
        for key in waktuSisa.keys():
            if(len(self.model[key]) == 1):
                self.model[key].append(waktuSisa[key])
            else:
                self.model[key][1] = waktuSisa[key]

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

    def getWaktuSisa(self, model) -> float:
        return float(self.model[model][1])

    def addModel(self, key: str, value: list):
        self.model[key] = value

    def updateStasBefore(self):
        newStas = []
        
        for node in self.precedence:
            if(node.stasiun not in newStas):
                newStas.append(node.stasiun)
        
        self.stasBefore = newStas


    def addConnection(self, friendNode):
        self.connection.append(friendNode)

        if(len(self.precedence) != 0):
            for precend in self.precedence:
                friendNode.precedence.append(precend)
        
        friendNode.precedence.append(self)

        friendNode.updateStasBefore()

    def isParent(self, listNode: list) -> bool:

        for node in listNode:
            if(node.id in self.precedence):
                return False
        
        return True
    
    def isPrecedence(self, id: int) -> bool:
        for node in self.precedence:
            if(node.id == id):
                return True
        
        return False

    def toList(self) -> list:
        val = []

        for model in self.model.keys():
            row = [self.stasiun, self.id, model, self.resource, self.model[model][0], self.model[model][1]]
            val.append(row)
        
        return val

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