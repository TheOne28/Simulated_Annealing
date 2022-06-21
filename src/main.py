from timeit import timeit
from config import fileCSV, dataInput, Parameter
from lib.graph import Graph
from lib.simulatedAnnealing import simulatedAnnealing
from ioHandler import readFile

from helperFunction import createGraph, inProb


def main():
    print("Here")
    data = readFile(fileCSV, dataInput)
    graph = createGraph(data, dataInput['precedences'])
    sa = simulatedAnnealing(graph, dataInput, Parameter)
    
    start = timeit()
    best = sa.objectiveFunction()
    allObjective = [best]


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
                allObjective.append(current)
            else:
                if(inProb(T, best - current)):
                    allObjective.append(current)
                else:
                    sa.revertChanges()
            
            n += 1
            
        T -= Parameter['ALPHA'] * T

    
    end = timeit()
    

if(__name__ == "__main__"):
    main()