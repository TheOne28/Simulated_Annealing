from random import random, choice

from lib.graph import Graph
from lib.node import Node

class simulatedAnnealing:
    def __init__(self, graph: Graph, data: map, param: map) -> None:
        if(self.graph == None or self.data == None or self.param == None):
            raise("Terjadi kesalahan input param atau processing graph")

        self.graph = graph
        self.allNode = self.graph.getGraph()
        self.data = data
        self.param = param

        self.setSisa()

    def getByStasiun(self) -> dict:
        stas = {}

        for node in self.allNode:
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

        stas = self.getByStasiun()
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
    

    def tukarTugas(self, exclude : list) -> bool:
        r2 = choice(list(self.data['task']))

        while(r2 in exclude):
            r2 = choice(list(self.data['task']))

        nodeR2 : Node = self.graph.findNode(r2)
        
        for node in self.allNode:
            if(node.getId() == r2):
                continue
            else:
                if(not node.isPrecedence(r2)):
                    temp = nodeR2.getStasiun()
                    nodeR2.setStasiun(node.getStasiun())
                    node.setStasiun(temp)
                    
                    print("Menukar tugas {} dan {}".format(r2, node.getId()))

                    self.setSisa()
                    return 0
        return r2

    def tukarResource(self, exclude) -> bool:
        r4 = choice(list(self.data['task']))
        
        while(r4 in exclude):
            r4 = choice(list(self.data['task']))
        
        s1 = choice(list(self.data['resources'].keys()))

        node4 : Node = self.graph.findNode(r4)

        if(node4.getResource() == s1):
            return False
        else:
            node4.setResource(s1)
            print("Menukar resource tugas {} dengan {}".format(r4, s1))

            self.setSisa()

            return True

    def countTotalSisa(self) -> map:
        sisa = {}

        self.stas = self.getByStasiun()
        
        ct = self.data['ct']
        count = 0

        for station in self.data['stations']:
            this = self.stas[station]
            sum = 0
            
            for node in this:
                allModel = node.getModel()
                count = len(allModel)
                for model in allModel.keys():
                    sum += allModel[model][0]
                
            sisa[station] = (count * ct) - sum
        
        return sorted(sisa.values())

    def minimStas(self, stasiun : int, totalWaktu: map) -> bool:
        this = self.stas[stasiun]
        idThis = []

        ct = self.data['ct']
        count = 0
        for node in this:
            idThis.append(node.getId())
        
        for node in self.allNode:
            if(node.getId() not  in idThis):
                allModel = node.getModel()
                count = len(allModel)

                sum = 0
                for model in allModel:
                    sum += allModel[model][0]
                
                if(totalWaktu[stasiun] + sum <= (count * ct)):
                    node.setStasiun(stasiun)

                    return True
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
            raise("Terdapat kesalahan mode")

    def loopOne(self):
        r1 = random()

        if(r1 < self.param['P'][0]):
            i = 0

            while(i < self.param['I']):
                a = 0
                exclude = []
                while(a < self.param['A']):
                    success = self.tukarTugas(exclude)
                    
                    """
                        success
                            0 -> Penukaran berhasil
                            r2 -> gagal karena Tugas r2 tidak bisa ditukar
                    """
                    if(success == 0):
                        break
                    else:
                        exclude.append(success)
                        a += 1
                i += 1
        else:
            print("Penukaran tugas tidak dilakukan karena r1 > p1")
    
    def loopTwo(self):
        r3 = random()

        if(r3 < self.param['P'][1]):
            i = 0
            
            while(i < self.param['I']):
                b = 0
                exclude = []

                while(b < self.param['B']):
                    success = self.tukarResource(exclude)
                    """
                        success 
                            True -> Penukaran berhasil
                            False -> Penukaran Gagal karena resource
                    """
                    if(success):
                        break

                i += 1
        else:
            print("Penukaran resource tidak dilakukan karena r3 > p2")

    def loopThree(self):
        r5 = random()

        if(r5 < self.param['P'][2]):
            
            c = 0
            """
            !! Asumsi sisa waktu -> Sisa X + Sisa Y
            """
            totalWaktu = self.countTotalSisa()

            while(c < self.param['C']):
                p = 1

                success = self.minimStasiun(p, totalWaktu)
                    
                if(success):
                    self.removeUnusedStation()
                    break
                else:
                    c += 1
                    p += 1

        else:
            print("Minimalisasi Stasiun Kerja tidak dilakukan karena r5 > p3")
    
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