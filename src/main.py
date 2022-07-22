from time import time
from copy import deepcopy
from config import fileCSV, dataInput, Parameter
from lib.simulatedAnnealing import simulatedAnnealing
from ioHandler import readFile, writeFileCSV, writeFileObj, writeCommand

from helperFunction import createGraph, inProb


def main():
    data = readFile(fileCSV, dataInput)
    graph = createGraph(data, dataInput['precedences'])
    sa = simulatedAnnealing(graph, dataInput, Parameter)
    
    start = time()
    best = sa.objectiveFunction()
    toCompare = deepcopy(best)
    indBest = 0
    iterasi = 1

    allObjective = [[0,best]]
    allCommand = []

    m = 0
    T = Parameter['T0']
    sa.printAll()
    
    while(m < Parameter['M']):
        n = 0

        while(n < Parameter['N']):
            sa.solve()

            current = sa.objectiveFunction()
            # print(current)
            if(current < toCompare):
                
                if(current < best):
                    indBest = iterasi
                    best = deepcopy(current)
                    
                toCompare = deepcopy(current)
                allObjective.append([1,current])
                allCommand.append([1, sa.command])
            else:
                if(inProb(T, abs(toCompare - current))):
                    toCompare = deepcopy(current)
                    allCommand.append([1, sa.command])
                    allObjective.append([1,current])
                else:
                    allObjective.append([-1, current])
                    allCommand.append([-1, sa.command])
                    sa.revertChanges()
            
            n += 1
            iterasi += 1
            
        T -= (Parameter['ALPHA'] * T)
        m += 1

    
    end = time()

    writeFileCSV(sa, fileCSV)
    writeCommand(allCommand, fileCSV)
    writeFileObj(allObjective, fileCSV)
    print("Waktu yang dibutuhkan", end - start)
    print("Ada {} stasiun yang dihapus".format(len(sa.removedStasiun)))

    if(len(sa.removedStasiun) != 0):
        print("Stasiun yang dihapus: ")

        for i in range(len(sa.removedStasiun)):
            print(sa.removedStasiun[i], end="\n")

    print("Minimal objective function pada iterasi ke {} dengan nilai {}".format(indBest, best))

if(__name__ == "__main__"):
    main()