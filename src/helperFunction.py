from lib.graph import Graph
from random import random

question = {
    1 : "Apakah menjalankan inner loop penukaran tugas?",
    2 : "Apakah menjalankan inner loop penukaran Resource?",
    3 : "Apakah menjalankan inner loop minimalisasi jumlah stasiun kerja?"
}

def validateResources(resource: str, res: dict) -> int:
    if resource in res.keys():
        return res[resource]
    else:
        return -1

def validateWaktu(waktu: int, CT: int) -> bool:
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

def inProb(T: int) -> bool:
    r = random()

    probFunc = T

    if(probFunc > r):
        return True
    
    False