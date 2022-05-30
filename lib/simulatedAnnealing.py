from random import Random
from re import I

from lib.graph import Graph
from lib.node import Node

class simulatedAnnealing:
    def __init__(self, graph: Graph, data: map) -> None:
        self.graph = graph
        self.allNode = self.graph.getGraph()
        self.data = data

    def getByStasiun(self, allNode) -> dict:
        stas = {}

        for node in allNode:
            stasiun = node.getStasiun()

            if(stasiun in stas.keys()):
                stas[stasiun].append(node)
            else:
                stas[stasiun] = [node]
        return stas

    def getAllParent(self, allNode) -> list | None:
        parent = []

        for node in allNode:
            if(node.isParent(allNode)):
                parent.append(node)
        
        return parent
    
    def findMinimum(self, before, resource, model, mapping, mode) -> int:
        minimum = before
        
        if(mode == 1):
            if(resource == 1 and "1{}".format(model) in mapping.keys()):
                minimum = min(minimum, mapping["1{}".format(model)])
            elif(resource == 2 and "2{}".format(model) in mapping.keys()):
                minimum = min(minimum, mapping["2{}".format(model)])
        else:
            if(resource == 1 and "1{}".format(model) in mapping.keys()):
                minimum = min(minimum, mapping["1{}".format(model)])
            if(resource == 2 and "2{}".format(model) in mapping.keys()):
                minimum = min(minimum, mapping["2{}".format(model)])

        return minimum

    def setSisa(self):
        stations = self.data['stations']

        stas = self.getByStasiun(self.allNode)
        ct = self.data['ct']
        mapping = {}

        for station in stations:
            current : list[Node] = stas[station]
            done = []
            sisa = {}
            allParent = self.getAllParent(current)
            
            if(len(allParent) == 0):
                raise("Terdapat kesalahan pada graf untuk stasiun {}, tidak ada parent Node".format(station))

            for parent in allParent:
                resource = parent.getResource()
                allModel = parent.getModel()
    
                """
                !! Belum kehanlde, kalau misal waktusisanya dah 0 gimana?
                """
                if(resource == 1 or resource == 2):
                    for model in allModel.keys():
                        minimum = self.findMinimum(ct, resource, model, mapping, 1)

                        mapping["{}{}".format(resource, model)] = minimum - allModel[model][0]
                        sisa[model] = minimum - allModel[model][0]
                else:
                    for model in allModel.keys():
                        minimum = self.findMinimum(ct, resource, model, mapping, 2)
                        mapping["1{}".format(resource, model)] = minimum - allModel[model][0]
                        mapping["2{}".format(resource, model)] = minimum - allModel[model][0]
                        sisa[model] = minimum - allModel[model][0]

                done.append(parent.getId())
                parent.setWaktuSisa(sisa)

            for parent in allParent:
                allConnect = [parent]
                
                while(True):
                    if(len(allConnect) == 0):
                        break
                    
                    before = allConnect[0]
                    connection = before.getConnection()
                    allConnect.pop(0)

                    for each in connection:
                        if(each.getStasiun() != station or each.getId() in done):
                            continue
                        
                        resource = each.getResource()
                        allModel = each.getModel()

                        if(resource == 1 or resource == 2):
                            for model in allModel.keys():
                                checkbef = before.getWaktuSisa(model)
                                minimum = self.findMinimum(checkbef, resource, model, mapping, 1)                                
                                mapping["{}{}".format(resource, model)] = minimum - allModel[model][0]
                                sisa[model] = mapping["{}{}".format(resource, model)]
                        else:
                            for model in allModel.keys():
                                checkbef = before.getWaktuSisa(model)

                                minimum = self.findMinimum(checkbef, resource, model, mapping, 2)

                                mapping["1{}".format(model)] = minimum - allModel[model][0]
                                mapping["2{}".format(model)] =  mapping["1{}".format(model)]
                                sisa[model] = mapping["1{}".format(model)]
                    
                        done.append(each.getId())
                        each.setWaktuSisa(sisa)
                        allConnect.append(each)
            
            mapping.clear()
            
    def loopOne(self):
        
        pass
    
    def loopTwo(self):
        pass

    def loopThree(self):
        pass
    
    def countRes(self):
        done = []
        alpha, ro = 0, 0
        b2, b3 = 0,0

        for node in self.allNode:
            id = node.getId()
            stasiun = node.getStasiun()
            resource = node.getResource()

            if("{}{}".format(stasiun, resource) not in done):
                if(resource == 1):
                    ro += 1
                    done.append("{}1".format(stasiun))
                elif(resource == 2):
                    alpha += 1
                    done.append("{}2".format(stasiun))
                elif(resource == 3 and "{}1".format(stasiun) not in done and "{}2".format(stasiun) not in done):
                    ro += 1
                    alpha += 1
                    done.append("{}1".format(stasiun))
                    done.append("{}2".format(stasiun))
            
            if(resource == 1):
                b2 += self.data['saving'][id][0]
            elif(resource == 3):
                b3 += self.data['saving'][id][1]
        
        return alpha, ro, b2, b3

    def findTau(self) -> int:
        minimum = self.data['ct']

        for node in self.allNode:
            minimum = min(minimum, node.getWaktuSisa('X'), node.getWaktuSisa('Y'))
        
        return self.data['ct'] - minimum

    def objectiveFunction(self):
        alpha, ro, b2, b3 = self.countRes()

        # print("alpha ", alpha)
        # print("ro ", ro)
        # print("b2 ", b2)
        # print("b3 ", b3)

        ci = self.data['ci']
        co = self.data['co']
        d = self.data['d']

        #Ini ct belum dicari
        tau = self.findTau()
        
        investasi = ci[0] * alpha + ci[1] * ro
        operasional = (co[0] * alpha + co[1] * ro) * d * tau
        val = investasi + operasional - b2 -  b3

        return val

    def printAll(self):

        for node in self.allNode:
            node.printNode()