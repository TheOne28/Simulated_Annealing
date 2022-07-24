from operator import rshift
from os import stat
from random import random, choice

from lib.graph import Graph
from lib.node import Node

class simulatedAnnealing:
    def __init__(self, graph: Graph, data: map, param: map) -> None:
        if(graph == None or data == None or param == None):
            raise Exception("Terjadi kesalahan input param atau processing graph")

        self.graph = graph
        self.allNode = self.graph.getGraph()
        self.data = data
        self.param = param
        self.command = []
        self.removedStasiun = []

        self.getByStasiun()

        self.setSisa()

    def getByStasiun(self):
        self.stas = {}

        for node in self.allNode:
            stasiun = node.getStasiun()

            if(stasiun in self.stas.keys()):
                self.stas[stasiun].append(node)
            else:
                self.stas[stasiun] = [node]

    def getAllParent(self, allNode) -> list:
        parent = []

        # print("L")
        # for each in allNode:
        #     print(each.id)

        for node in allNode:
            if(node.isParent(allNode)):
                parent.append(node)

        return parent
    
    def findMinimum(self, before, resource, model, mapping) -> int:
        
        if(resource == 1):
            if("1{}".format(model) in mapping.keys()):
                minimum = min(before, mapping["1{}".format(model)])
            else: 
                minimum = before
        elif(resource == 2):
            if("2{}".format(model) in mapping.keys()):
                minimum = min(before, mapping["2{}".format(model)])
            else:
                minimum = before
        else:
            minimum = before

            if("1{}".format(model) in mapping.keys()):
                minimum = min(minimum, mapping["1{}".format(model)])
            if("2{}".format(model) in mapping.keys()):
                minimum = min(minimum, mapping["2{}".format(model)])

        return minimum

    def sisaEachStation(self, station: int, listNode: list):
        ct = self.data['ct']
        mapping = {}
        done = []
        sisa = {}

        allParent = self.getAllParent(listNode)
        
        # print()
        # print("S")
        # print(station)

        # for each in allParent:
        #     print(each.id)


        if(len(allParent) == 0):
            raise Exception("Terdapat kesalahan pada graf untuk stasiun {}, tidak ada parent Node".format(station))

        for parent in allParent:
            resource = parent.resource
            allModel = parent.model
    
            save = True

            if(resource == 1 or resource == 2):
                for model in allModel.keys():
                    minimum = self.findMinimum(ct, resource, model, mapping)

                    if(minimum < allModel[model][0]):
                        save = False
                    else: 
                        mapping["{}{}".format(resource, model)] = minimum - allModel[model][0]
                        sisa[model] = minimum - allModel[model][0]


            else:
                for model in allModel.keys():
                    minimum = self.findMinimum(ct, resource, model, mapping)
                    mapping["1{}".format(model)] = minimum - allModel[model][0]
                    mapping["2{}".format(model)] = minimum - allModel[model][0]
                    
                    if(minimum < allModel[model][0]):
                        save = False
                    else:
                        sisa[model] = minimum - allModel[model][0]

            if(not save):
                return False

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
                    
                    save = True

                    resource = each.getResource()
                    allModel = each.getModel()

                    if(resource == 1 or resource == 2):
                        for model in allModel.keys():
                            checkbef = before.getWaktuSisa(model)
                            minimum = self.findMinimum(checkbef, resource, model, mapping)      

                            if(minimum < allModel[model][0]):
                                save = False
                            else:
                                mapping["{}{}".format(resource, model)] = minimum - allModel[model][0]
                                sisa[model] = mapping["{}{}".format(resource, model)]
                    else:
                        for model in allModel.keys():
                            checkbef = before.getWaktuSisa(model)

                            minimum = self.findMinimum(checkbef, resource, model, mapping)

                            if(minimum < allModel[model][0]):
                                save = False
                            else:
                                mapping["1{}".format(model)] = minimum - allModel[model][0]
                                mapping["2{}".format(model)] =  mapping["1{}".format(model)]
                                sisa[model] = mapping["1{}".format(model)]
                    
                    if(not save):
                        return False
    
                    done.append(each.getId())
                    each.setWaktuSisa(sisa)
                    allConnect.append(each)
        return True


    def checkPrecendence(self, node1: Node, node2: Node):
        return node1.isPrecedence(node2.id) or node2.isPrecedence(node1.id)


    def setSisa(self):
        stations = self.data['stations']

        self.getByStasiun()
        for station in stations:
            self.sisaEachStation(station, self.stas[station])
            
    
    def trySwap(self, node) -> bool:
        resourceBefore = node.resource
        allResource = self.data['resources']

        
        self.getByStasiun()

        
        if(self.sisaEachStation(node.stasiun, self.stas[node.stasiun])):
            return True
        else:
            for resource in allResource.keys():
                resource = allResource[resource]
                if(resource != resourceBefore):
                    node.resource = resource

                    for each in self.data['model']:
                        combine = (node.id, each)
                        node.model[each][0] = self.data['timetaken'][combine][node.resource - 1]
                    
                    if(self.sisaEachStation(node.stasiun, self.stas[node.stasiun])):
                        return True
            
            node.resource = resourceBefore
            
            for each in self.data['model']:
                        combine = (node.id, each)
                        node.model[each][0] = self.data['timetaken'][combine][node.resource - 1]
            return False


    # Main job untuk loop one
    def tukarTugas(self) -> bool:
        r2 = choice(list(self.data['task']))


        nodeR2 : Node = self.graph.findNode(r2) 

        sts = nodeR2.stasiun

        start = -1
        end = -1

        if(sts > 3):
            start = sts - 2
        else:
            start = max(sts - 2, 1)
        
        if(sts < len(self.data['stations']) - 2):
            end = sts - 1
        else:
            end = min(sts +  2, len(self.data['stations']))

        for key in self.stas.keys():
            if(key != sts and key >= start and key <= end):
                
                # print("k")
                # print(sts)
                # print(key)
                # print("")
                thisNode = self.stas[key]
                
                # print("N")
                # for node in thisNode:

                #     print(node.id, end = " ")

                for node in thisNode:
                    if(not self.checkPrecendence(node, nodeR2) and node.id != r2):
                        # print("Y")
                                        
                        # for inKey in self.stas.keys():
                        #     print(inKey)
                        #     for masing in self.stas[inKey]:
                        #         print(masing.id, end = " ")
                        #     print()
                        
                        # print()
                        can = True

                        for stat in node.stasBefore:
                            if(stat > nodeR2.stasiun):
                                can = False
                                break
                        
                        for stat in nodeR2.stasBefore:
                            if(stat > node.stasiun):
                                can = False
                                break
                        

                        for each in self.allNode:
                            if(each.isPrecedence(node.id)):
                                if(each.stasiun < nodeR2.stasiun):
                                    can = False
                                    break
                                
                            if(each.isPrecedence(nodeR2.id)):
                                if(each.stasiun < node.stasiun):
                                    can = False
                                    break

                        if(can):
                            temp = node.stasiun
                            node.stasiun = nodeR2.stasiun
                            nodeR2.stasiun = temp

                            # print("W")
                            # print(temp)
                            # print(node.stasiun)
                            # print(nodeR2.stasiun)
                            if(self.trySwap(node) and self.trySwap(nodeR2)):
                                # print("Z")
                                # print(node.stasiun)
                                # print(nodeR2.stasiun)
                                # print()
                                # print("I")
                                # print(node.id)
                                # print(nodeR2.id)

                                # print("X")
                                
                                # for inKey in self.stas.keys():
                                #     print(inKey)
                                #     for masing in self.stas[inKey]:
                                #         print(masing.id, end = " ")
                                #     print()

                                self.command.append({
                                    "job" : 1,
                                    "node1" : node.id,
                                    "node2": nodeR2.id
                                })

                                return True
                            else:
                                nodeR2.stasiun = node.stasiun
                                node.stasiun = temp  
                                self.getByStasiun()      
                                # print("Q")
                                # print(nodeR2.stasiun)
                                # print(node.stasiun)                
        return False

    #Main job untuk loop two
    def tukarResource(self) -> bool:
        r4 = choice(list(self.data['task']))
        
        
        s1 = choice(list(self.data['resources'].keys()))

        s1 = self.data['resources'][s1]
        node4 : Node = self.graph.findNode(r4)

        if(node4.resource == s1):
            return False
        else:
            before = node4.resource
            node4.resource = s1
            
            for each in self.data['model']:
                combine = (node4.id, each)
                node4.model[each][0] = self.data['timetaken'][combine][node4.resource - 1]

            if(not self.sisaEachStation(node4.stasiun, self.stas[node4.stasiun])):
                node4.resource = before

                for each in self.data['model']:
                    combine = (node4.id, each)
                    node4.model[each][0] = self.data['timetaken'][combine][node4.resource - 1]
                return False
            
            self.command.append({
                "job": 2,
                "node" : node4.id,
                "before" : before,
                "after": s1,
            })
            return True

    def countTotalSisa(self, model : str) -> list:
        sisa = {}

        
        ct = self.data['ct']

        for station in self.data['stations']:
            this = self.stas[station]
            sum = 0
            
            for node in this:
                allModel = node.getModel()
                sum += allModel[model][0]
                
            sisa[station] = ct - sum
        
        orderStasiun = sorted(sisa.items(), key= lambda kv: (kv[1], kv[0]))
        return orderStasiun

    #Main job untuk loop three  
    def minimStas(self, stasiun : int) -> bool:
        this = self.stas[stasiun]
        idThis = []


        for node in this:
            idThis.append(node.id)

        for node in self.allNode:
            if(node.getId() not in idThis):
                
                can = True
                for check in this:
                    if(self.checkPrecendence(node, check)):
                        can = False
                        break
                
                for stas in node.stasBefore:
                    if(stas > stasiun):
                        can = False
                        break
                
                stas = node.stasiun
                
                for checkNode in self.allNode:
                    if(checkNode.isPrecedence(node.id) and checkNode.stasiun < stasiun):
                        can = False
                        break
            

                if(can):
                    before = node.stasiun
                    node.stasiun = stasiun
                    if(self.trySwap(node)):
                        self.command.append({
                            "job" : 3,
                            "node" : node.id,
                            "stasiun" : stasiun,
                        })
                        node.updateStasBefore()
                        return True
                    else:
                        node.stasiun = before

        return False


    def removeUnusedStation(self):
        stations = self.data['stations']

        toPop = -1
        for i in range(len(stations)):
            stas = stations[i]
            
            if(not stas in self.stas.keys()):
                self.removedStasiun.append(stas)
                self.command[2]["delete"] = stas
                toPop = i
        
        if(toPop != -1):
            stations.pop(toPop)

        self.data['stations'] = stations
            


    def solve(self):
        self.command = []

        self.loopOne()
        self.loopTwo()
        self.loopThree()

    def loopOne(self):
        r1 = random()

        self.getByStasiun()

        if(r1 < self.param['P'][0]):
            i = 0
            can = False

            while(i < self.param['I']):
                a = 0
                while(a < self.param['A']):
                    success = self.tukarTugas()
                    
                    if(success):
                        can = True
                        break
                    else:
                        a += 1
                if(can):
                    break
                
                i += 1
            
            if(not can):
                self.command.append({
                    "job" : 1,
                    "node1": -1,
                    "node2" : -1,
                })
        else:
            self.command.append({
                "job" : -1
            })
    
    def loopTwo(self):
        r3 = random()

        self.getByStasiun()

        if(r3 < self.param['P'][1]):
            i = 0
            can = False
            while(i < self.param['I']):
                b = 0

                while(b < self.param['B']):
                    success = self.tukarResource()
                    """
                        success 
                            True -> Penukaran berhasil
                            False -> Penukaran Gagal karena resource
                    """
                    if(success):
                        can = True
                        break

                if(can):
                    break

                i += 1
            
            if(not can):
                self.command.append({
                    "job" : 2,
                    "node": -1,
                    "before": -1,
                    "after" : -1
                })
        else:
            self.command.append({
                "job" : -1
            })

    def loopThree(self):
        r5 = random()

        self.getByStasiun()

        if(r5 < self.param['P'][2]):
            selectedModel = choice(self.data['model'])
            c = 0
            can = False

            totalWaktu = self.countTotalSisa(selectedModel)

            while(c < self.param['C']):
                p = 0

                success = self.minimStas(totalWaktu[p][0])
                    
                if(success):
                    can = True
                    self.getByStasiun()
                    self.removeUnusedStation()
                    break
                else:
                    c += 1
                    p += 1
            
            if(not can):
                self.command.append({
                    "job" : 3,
                    "node" : -1,
                    "stasiun": -1
                })
        else:
            self.command.append({
                "job" : -1
            })
    
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
                elif(resource == 3):
                    if("{}1".format(stasiun) not in done):
                        ro += 1
                        done.append("{}1".format(stasiun))  
                    
                    if("{}2".format(stasiun) not in done):
                        alpha += 1
                        done.append("{}2".format(stasiun))
            
            if(resource == 1):
                b2 += self.data['saving'][id][0]
            elif(resource == 3):
                b3 += self.data['saving'][id][1]
        print(done)
        return alpha, ro, b2, b3

    def findTau(self) -> int:
        minimum = self.data['ct']

        for node in self.allNode:
            
            for model in self.data['model']:
                key = f"{node.stasiun}{model}"
                if(key in self.allCT.keys()):
                    self.allCT[key][0] = min(self.allCT[key][0], node.getWaktuSisa(model))
                    self.allCT[key][1] = self.data['ct'] - self.allCT[key][0] 
                else:
                    self.allCT[key] = [node.getWaktuSisa(model)]
                    self.allCT[key].append(self.data['ct'] - self.allCT[key][0])

                minimum = min(minimum, node.getWaktuSisa(model))

        return self.data['ct'] - minimum

    def objectiveFunction(self):
        self.allCT = {}
        alpha, ro, b2, b3 = self.countRes()

        print("alpha ", alpha)
        print("ro ", ro)
        print("b2 ", b2)
        print("b3 ", b3)

        ci = self.data['ci']
        co = self.data['co']
        d = self.data['d']

        #Ini ct belum dicari
        self.tau = self.findTau()
        
        investasi = ci[0] * alpha + ci[1] * ro
        operasional = (co[0] * alpha + co[1] * ro) * d * self.tau
        val = investasi + operasional - b2 -  b3

        return val

    def revertOne(self, node1: Node, node2: Node):
        temp = node1.stasiun
        node1.stasiun = node2.stasiun
        node2.stasiun = temp

        self.getByStasiun()

        self.sisaEachStation(node1.stasiun, self.stas[node1.stasiun])
        self.sisaEachStation(node2.stasiun, self.stas[node2.stasiun])

    def revertTwo(self, node: Node, before: str):
        node.resource = before

        self.sisaEachStation(node.stasiun, self.stas[node.stasiun])

    def revertThree(self, node: Node, stasiun: int):
        if(stasiun not in self.data['stations']):
            self.data['stations'].append(stasiun)
        
        self.removedStasiun.pop(len(self.removedStasiun) - 1)
        before = node.stasiun
        node.stasiun = stasiun

        self.getByStasiun()

        self.sisaEachStation(stasiun, self.stas[stasiun])
        self.sisaEachStation(before, self.stas[before])


    def revertChanges(self):
        loopone = self.command[0]
        looptwo = self.command[1]
        loopthree = self.command[2]

        if(loopone['job'] != -1):
            if(loopone["node1"] != -1):
                self.revertOne()

        if(looptwo['job'] != -1):
            if(looptwo["node"] != -1):
                self.revertTwo()        
        
        if(loopthree['job'] != -1):
            if(loopthree["node"] != -1):
                self.revertThree()

    def printAll(self):

        for node in self.allNode:
            node.printNode() 