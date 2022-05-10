

class Node:
    def __init__(self, id:int) -> None:
        self.id = id
        self.connection = []
    
    def getId(self) -> int:
        return self.id
    
    def addConnection(self, friendNode):
        self.connection.append(friendNode)
    