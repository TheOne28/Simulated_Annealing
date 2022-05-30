from config import fileCSV, dataInput
from lib.graph import Graph
from lib.simulatedAnnealing import simulatedAnnealing
from csvHandler import readFile

def createGraph(data: dict) -> Graph:
    graph = Graph()

    for pair in dataInput['precedences']:

        graph.addEdge(data[pair[0]], data[pair[1]])

    return graph

def main():
    data = readFile(fileCSV, dataInput)
    graph = createGraph(data)
    sa = simulatedAnnealing(graph, dataInput)
    sa.setSisa()
    sa.printAll()

    print("Obejctive Function: ", sa.objectiveFunction())
    
    

if(__name__ == "__main__"):
    main()