from lib.graph import Graph
from random import random

E = 2.718281828459045

def validateResources(resource: str, res: dict) -> int:
    if resource in res.keys():
        return res[resource]
    else:
        return -1

def validateWaktu(waktu: float, CT: float) -> bool:
    return waktu <= CT

def validateStation(stat: int, station: tuple):
    return stat in station

def validateTask(task: int, alltask: tuple):
    return task in alltask

def createGraph(data: dict, precedence: list) -> Graph:
    graph = Graph()

    for pair in precedence:

        graph.addEdge(data[pair[0]], data[pair[1]])

    return graph

def inProb(T: float, deltaE: float) -> bool:
    r = random()

    print("DeltaE", deltaE)
    print("T", T)

    try:
        probFunc = E ** (deltaE / T)
    except OverflowError:
        probFunc = 1

    if(probFunc > r):
        return True
    
    return False