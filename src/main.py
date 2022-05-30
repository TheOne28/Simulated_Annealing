from timeit import timeit
from config import fileCSV, dataInput, PARAMETER
from lib.graph import Graph
from lib.simulatedAnnealing import simulatedAnnealing
from csvHandler import readFile
from helperFunction import getInput

def createGraph(data: dict) -> Graph:
    graph = Graph()

    for pair in dataInput['precedences']:

        graph.addEdge(data[pair[0]], data[pair[1]])

    return graph

def main():
    data = readFile(fileCSV, dataInput)
    graph = createGraph(data)
    sa = simulatedAnnealing(graph, dataInput, PARAMETER)
    
    start = timeit()
    before = sa.objectiveFunction()

    sa.printAll()

    for i in range(1, 4):
        doing = getInput(i)
        
        if(doing):
            sa.solve(i)

    after = sa.objectiveFunction()

    end = timeit()
    print("Objective Function Before Inner Loop: ", before)
    print("Objective Function After Inner Loop: ", after)
    

if(__name__ == "__main__"):
    main()