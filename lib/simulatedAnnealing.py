from random import random, choice
from statistics import mode


from lib.graph import Graph
from lib.node import Node

class simulatedAnnealing:
    def __init__(self, graph: Graph, data: map, param: map) -> None:
        if(graph == None or data == None or     param == None):
            raise Exception("Terjadi kesalahan input param atau processing graph")

        self.graph = graph
        self.allNode = self.graph.getGraph()
        self.data = data
        self.param = param
        self.command = []

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

    def sisaEachStation(self, station: int, listNode: list):
        ct = self.data['ct']
        mapping = {}
        done = []
        sisa = {}

        allParent = self.getAllParent(listNode)
            
        if(len(allParent) == 0):
            raise Exception("Terdapat kesalahan pada graf untuk stasiun {}, tidak ada parent Node".format(station))

        for parent in allParent:
            resource = parent.getResource()
            allModel = parent.getModel()
    
            """
            !! Belum kehanlde, kalau misal waktusisanya dah 0 gimana?
            """

            save = True

            if(resource == 1 or resource == 2):
                for model in allModel.keys():
                    minimum = self.findMinimum(ct, resource, model, mapping, 1)

                    mapping["{}{}".format(resource, model)] = minimum - allModel[model][0]
                    
                    if(minimum < allModel[model][0]):
                        save = False
                    else: 
                        sisa[model] = minimum - allModel[model][0]


            else:
                for model in allModel.keys():
                    minimum = self.findMinimum(ct, resource, model, mapping, 2)
                    mapping["1{}".format(resource, model)] = minimum - allModel[model][0]
                    mapping["2{}".format(resource, model)] = minimum - allModel[model][0]
                    
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
                            minimum = self.findMinimum(checkbef, resource, model, mapping, 1)      

                            if(minimum < allModel[model][0]):
                                save = False
                            else:
                                mapping["{}{}".format(resource, model)] = minimum - allModel[model][0]
                                sisa[model] = mapping["{}{}".format(resource, model)]
                    else:
                        for model in allModel.keys():
                            checkbef = before.getWaktuSisa(model)

                            minimum = self.findMinimum(checkbef, resource, model, mapping, 2)

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


    def setSisa(self):
        stations = self.data['stations']

        for station in stations:
            self.sisaEachStation(station, self.stas[station])
            
    
    def trySwap(self, node) -> bool:
        resourceBefore = node.resource
        allResource = self.data['resources']

        
        self.getByStasiun()
        
        if(self.sisaEachStation(node.station, self.stas[node.station])):
            return True
        else:
            for resource in allResource.keys() and resource != resourceBefore:
                node.resource = resource

                if(self.sisaEachStation(node.station, self.stas[node.station])):
                    return True
            
            node.resource = resourceBefore
                
            return False


    # Main job untuk loop one
    def tukarTugas(self) -> bool:
        r2 = choice(list(self.data['task']))


        nodeR2 : Node = self.graph.findNode(r2) 

        stas = nodeR2.stasiun

        start = -1
        end = -1

        if(stas > 3):
            start = stas - 1
        
        if(stas < len(self.data['stations']) - 2):
            end = stas - 1

        for key in self.stas.keys():
            if(key != stas and key >= start and key <= end):
                thisNode = self.stas[key]

                for node in thisNode:
                    if(not node.isPrecedence(r2) and not nodeR2.isPrecedence(node.id)):
                        temp = node.station
                        node.station = nodeR2.station
                        nodeR2.station = temp

                        if(self.trySwap(node) and self.trySwap(nodeR2)):
                            self.command.append({
                                "job" : 1,
                                "node1" : node.id,
                                "node2": nodeR2.id
                            })

                            return True
                        else:
                            nodeR2.station = node.station
                            node.station = temp                        
        return False

    #Main job untuk loop two
    def tukarResource(self) -> bool:
        r4 = choice(list(self.data['task']))
        
        
        s1 = choice(list(self.data['resources'].keys()))

        node4 : Node = self.graph.findNode(r4)

        if(node4.getResource() == s1):
            return False
        else:
            before = node4.resource
            node4.resource = s1

            if(not self.sisaEachStation(node4.stasiun, self.stas[node4.stasiun])):
                node4.resource = before
                return False
            
            self.command.append({
                "job": 2,
                "node" : node4.id,
                "before" : before,
                "after": s1,
            })
            return True

    def countTotalSisa(self, model : str) -> map:
        sisa = {}

        
        ct = self.data['ct']

        for station in self.data['stations']:
            this = self.stas[station]
            sum = 0
            
            for node in this:
                allModel = node.getModel()
                sum += allModel[model][0]
                
            sisa[station] = ct - sum
        
        return sorted(sisa.values())

    #Main job untuk loop three  
    def minimStas(self, stasiun : int, totalWaktu: map, model : str) -> bool:
        this = self.stas[stasiun]
        idThis = []

        ct = self.data['ct']
        count = 0

        for node in this:
            idThis.append(node.getId())
        

        for node in self.allNode:
            if(node.getId() not  in idThis):
                before = node.stasiun
                node.stasiun = stasiun
                if(self.trySwap()):
                    self.command.append({
                        "job" : 3,
                        "node" : node.id,
                        "stasiun" : 1,
                    })
                    return True
                else:
                    node.stasiun = before

        return False


    def removeUnusedStation(self):
        stations = self.data['stations']

        for i in range(len(stations)):
            if(len(self.stas[self.data[stations[i]]]) == 0):
                stations.pop(i)
            


    def solve(self, mode):
        if(mode == 1):
            self.loopOne()
        elif(mode == 2):
            self.loopTwo()
        elif(mode == 3):
            self.loopThree()
        else:
            raise Exception("Terdapat kesalahan mode")

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
                p = 1

                success = self.minimStas(p, totalWaktu)
                    
                if(success):
                    can = True
                    self.removeUnusedStation()
                    break
                else:
                    c += 1
                    p += 1
            
            if(not can):
                self.command.append({
                    "job" : -1,

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

    def revertChanges(self):
        
        for i in range(3):
            
    def printAll(self):

        for node in self.allNode:
            node.printNode() 