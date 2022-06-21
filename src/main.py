from timeit import timeit
from config import fileCSV, dataInput, Parameter
from lib.graph import Graph
from lib.simulatedAnnealing import simulatedAnnealing
from ioHandler import readFile

from helperFunction import createGraph, inProb


def main():
    data = readFile(fileCSV, dataInput)
    graph = createGraph(data, dataInput['precedences'])
    sa = simulatedAnnealing(graph, dataInput, Parameter)
    
    start = timeit()
    best = sa.objectiveFunction()
    allObjective = [[1,best]]
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

            if(current > best):
                best = current
                allObjective.append([1,current])
                allCommand.append([1, sa.command])
            else:
                if(inProb(T, best - current)):
                    allCommand.append([1, sa.command])
                    allObjective.append([1,current])
                else:
                    allObjective.append([-1, current])
                    allCommand.append([-1, sa.command])
                    sa.revertChanges()
            
            n += 1
            
        T -= (Parameter['ALPHA'] * T)

    
    end = timeit()
    print("Waktu yang dibutuhkan", start - end)

if(__name__ == "__main__"):
    main()