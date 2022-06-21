from lib.node import Node
from lib.simulatedAnnealing import simulatedAnnealing
from helperFunction import validateResources, validateWaktu, validateStation, validateTask

import csv
from pathlib import Path


def readFile(filename: str, config: dict) -> dict | None:
    
    filePath = str(Path(Path(__file__).parent).parent) + "\\data\\input\\" + filename + '.csv'
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
            station = int(data[0])
            id = int(data[1])
            model = data[2]
            resource = data[3]
            waktu = int(data[4])
            
            # print(station)
            # print(id)
            # print(model)
            # print(resource)
            # print(waktu)
            if(not validateResources(resource, config['resources'])):
                raise Exception("Masukan resource tidak valid pada element dengan ID {} dan Model {}", id, model)
            
            resource = config['resources'][resource]


            if(not validateWaktu(waktu, config['ct'])):
                raise Exception("Masukan waktu tidak valid pada element dengan ID {} dan Model {}", id, model)

            if(not validateTask(id, config['task'])):
                raise Exception("Masukan task tidak valid dengan ID {}", id)

            if(not validateStation(station, config['stations'])):
                raise Exception("Masukan station tidak valid pada element dengan ID {}", id)

            if(id in dictNode.keys()):
                res = dictNode[id].getResource()
                if(resource != res):
                    raise("Masukan model tidak valid pada element dengan ID {}".format(id))
                
                dictNode[id].addModel(model,  [waktu])
            else:
                newModel = {model: [waktu]}
                newNode = Node(id, station, newModel, resource)
                dictNode[id] = newNode
    
    return dictNode


def writeFileCSV(sa: simulatedAnnealing, suffix: str):
    filePath = str(Path(Path(__file__).parent).parent) + "\\data\\output\\" + "finalSolution-" + suffix + '.csv'
    header = ['Station', 'Element', 'Model', 'Resource', 'Waktu', 'Waktu Sisa']

    try:
        with open(filePath, 'w', encoding="UTF8", newline='') as file:
            writer = csv.writer(file)

            writer.writerow(header)

            graph = sa.graph

            for node in graph.graph:
                this = node.toList() 

                writer.writerows(this)
    except Exception as e:
        print("Error saat menulis file")

def writeFileObj(allObj: list, suffix: str):
    filePath = str(Path(Path(__file__).parent).parent) + "\\data\\output\\" + "listObjFunction-" + suffix + '.txt'

    file = open(filePath, 'w')

    for i in range(len(allObj)):
        if(allObj[i][0] == -1):
            file.write(f"Iterasi ke {i + 1}: Tidak dipakai\nNilai yang didapatkan: {allObj[i][1]}")
        else:
            file.write(f"Iterasi ke {i + 1}: {allObj[i][1]}")

def writeCommand(allCommand: list, suffix: str):
    filePath = str(Path(Path(__file__).parent).parent) + "\\data\\output\\" + "listCommand-" + suffix + '.txt'

    file = open(filePath, 'w')

    for i in range(len(allCommand)):
        if(allCommand[i][0] == -1):
            file.write(f"Iterasi ke {i+1}, command tidak dipakai")
        else:
            file.write(f"Iterasi ke {i + 1}, command dipakai")
        
        file.write("Command: ")

        loopOne = allCommand[i][1][0]
        loopTwo = allCommand[i][1][1]
        loopThree = allCommand[i][1][2]

        if(loopOne['job'] == -1):
            file.write("Loop pertama tidak dilakukan")
        else:
            if(loopOne['node1'] == -1):
                file.write("Loop pertama dilakukan, tetapi tidak ada tugas yang berhasil ditukar")
            else:
                file.write(f"Loop pertama menukar tugas {loopOne['node1']} dengan tugas {loopOne['node2']}")
        
        if(loopTwo['job'] == -1):
            file.write("Loop kedua tidak dilakukan")
        else:
            if(loopTwo['node'] == -1):
                file.write("Loop kedua dilakukan, tetapi tidak ada tugas yang behasil diganti resourcesnya")
            else:
                file.write(f"Loop kedua menukar resource tugas {loopTwo['node']} dari {loopTwo['before']} menjadi  {loopTwo['nafter']}")

        if(loopThree['job'] == -1):
            file.write("Loop ketiga tidak dilakukan")
        else:
            if(loopThree['node'] == -1):
                file.write("Loop ketiga dilakukan, tetapi tidak ada minimasi stasiun yang berhasil dilakukan")
            else:
                file.write(f"Loop ketiga memindahkan tugas {loopThree['node']} ke stasiun {loopThree['stasiun']}")