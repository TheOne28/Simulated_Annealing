from timeit import timeit
from config import fileCSV, dataInput, Parameter
from lib.simulatedAnnealing import simulatedAnnealing
from ioHandler import readFile, writeFileCSV, writeFileObj, writeCommand

from helperFunction import createGraph, inProb


def main():
    data = readFile(fileCSV, dataInput)
    graph = createGraph(data, dataInput['precedences'])
    sa = simulatedAnnealing(graph, dataInput, Parameter)
    
    start = timeit()
    best = sa.objectiveFunction()
    toCompare = best
    indBest = -1
    iterasi = 1

    allObjective = [[0,best]]
    allCommand = []

    m = 0
    T = Parameter['T0']
    sa.printAll()
    
    while(m < Parameter['M']):
        n = 0

        while(n < Parameter['N']):
            for i in range(1, 4):
                sa.solve(i)
            
            current = sa.objectiveFunction()
            print(current)
            if(current < toCompare):
                indBest = iterasi
                best = current
                toCompare = current
                allObjective.append([1,current])
                allCommand.append([1, sa.command])
            else:
                if(inProb(T, abs(toCompare - current))):
                    toCompare = current
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

    
    end = timeit()
    writeFileCSV(sa, fileCSV)
    writeCommand(allCommand, fileCSV)
    writeFileObj(allObjective, fileCSV)
    print("Waktu yang dibutuhkan", start - end)
    print("Minimal objective function pada iterasi ke {} dengan nilai {}".format(indBest, best))

if(__name__ == "__main__"):
    main()