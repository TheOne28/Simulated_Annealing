from lib.node import Node

class Graph:
    def __init__(self) -> None:
        self.graph : list[Node]= []

    def getGraph(self) -> list[Node]:
        return self.graph

    def addNode(self, node: Node):
        self.graph.append(node)
    
    def isNodeExist(self, id: int) -> bool:
        for node in self.graph:
            if(node.getId() == id):
                return True
        return False

    def findNode(self, id: int) -> Node | None:
        if(self.isNodeExist(id)):
            for node in self.graph:
                if(node.getId() == id):
                    return node
        
        return None
    
    '''
        addEdge akan menambahkan jalur dari node1 ke node2
        Ini berarti node2 akan ada dalam connection node1
    '''
    def addEdge(self, node1: Node, node2: Node):
        if(not self.isNodeExist(node1.getId())):
            self.addNode(node1)
        
        if(not self.isNodeExist(node2.getId())):
            self.addNode(node2)
        
        node1.addConnection(node2)

