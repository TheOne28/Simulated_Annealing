

class Node:
    def __init__(self, id:int, stasiun: int, model: dict ) -> None:
        self.id = id
        self.connection = []
        self.stasiun = stasiun
        self.model = model
    
    def getId(self) -> int:
        return self.id
    
    def getStasiun(self) -> int:
        return self.stasiun

    def getModel(self) -> dict:
        return self.model

    def addModel(self, key: str, value: list):
        self.model[key] = value

    def addConnection(self, friendNode):
        self.connection.append(friendNode)
    