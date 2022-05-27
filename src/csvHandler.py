from lib.node import Node
from helperFunction import validateResources, validateWaktu, validateStation, validateTask

import csv
from pathlib import Path


def readFile(filename: str, config: dict) -> list | None:
    
    filePath = str(Path(Path(__file__).parent).parent) + "/data/" + filename
    csvFile = open(filePath, 'r')
    csvData = None

    try:
        csvData = csv.reader(csvFile)
    except Exception as e:
        print(e)
        print("Error saat membaca file CSV")

    line = 0
    dictNode : dict[int, Node] = {} 

    for data in csvData:
        if(line == 0):
            #Kasus membaca header
            line += 1
        else:
            station = data[0]
            id = data[1]
            model = data[2]
            resource = data[3]
            waktu = data[4]

            if(not validateResources(resource, config['resources'])):
                raise("Masukan resource tidak valid pada element dengan ID {} dan Model {}", id, model)

            if(not validateWaktu(waktu, config['ct'])):
                raise("Masukan waktu tidak valid pada element dengan ID {} dan Model {}", id, model)

            if(not validateTask(id, config['task'])):
                raise("Masukan task tidak valid dengan ID {}", id)

            if(not validateStation(station, config['stations'])):
                raise("Masukan station tidak valid pada element dengan ID {}", id)

            if(id in dictNode.keys):
                if(resource not in dictNode[id].getModel().values):
                    raise("Masukan model tidak valid pada element dengan ID {}".format(id))
                
                dictNode[id].addModel(model, [resource, waktu])
            else:
                newModel = {model: [resource, waktu]}
                newNode = Node(id, station, newModel)
                dictNode[id] = newNode
    
    return dictNode.values