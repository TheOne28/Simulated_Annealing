from timeit import timeit
from config import fileCSV, dataInput, Parameter
from lib.graph import Graph
from lib.simulatedAnnealing import simulatedAnnealing
from csvHandler import readFile

from helperFunction import createGraph, inProb


def main():
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
        allObjective.append(current)

        T -= Parameter['ALPHA'] * T

        if(current > best and not inProb(Parameter['T'])):
            break

    end = timeit()
    print("Objective Function Before Inner Loop: ", current[0])
    print("Objective Function After Inner Loop: ", current[len(current) - 1])
    

if(__name__ == "__main__"):
    main()