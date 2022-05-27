from random import Random

from graph import Graph
from node import Node

class simulatedAnnealing:
    def __init__(self, graph: Graph, ci: list, co: list, ct: int, d: int, tau: int, saving: map, timeTaken: map) -> None:
        self.graph = graph
        self.ci = ci
        self.co = co
        self.ct = ct
        self.saving = saving
        self.timeTaken = timeTaken
        self.d = d
        self.tau = tau

    
    def loopOne(self):
        
        pass
    
    def loopTwo(self):
        pass

    def loopThree(self):
        pass
    
    def countRes(self, allNode):
        done = []
        alpha, ro = 0, 0
        b2, b3 = 0,0

        for node in allNode:
            id = node.getId()
            resource = node.getResource()

            if("{}{}".format(id, resource) not in done):
                if(resource == 1):
                    ro += 1
                    done.append("{}1".format(id))
                elif(resource == 2):
                    alpha += 1
                    done.append("{}2".format(id))
                elif(resource == 3):
                    ro += 1
                    alpha += 1
                    done.append("{}1".format(id))
                    done.append("{}2".format(id))
            
            if(resource == 1):
                b2 += self.saving[id][0]
            elif(resource == 3):
                b3 += self.saving[id][1]
        
        return alpha, ro, b2, b3

    def objectiveFunction(self):
        allNode = self.graph.getGraph()
        alpha, ro, b2, b3 = self.countRes(allNode)

        #Ini ct belum dicari
        ct = 19
        
        investasi = self.ci[0] * alpha + self.ci[1] * ro
        operasional = (self.co[0] * alpha + self.co[1] * ro) * self.d * self.tau
        val = investasi + operasional - b2 -  b3

        return val

    