from config import *

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

def getInput(mode) -> bool:
    answer = ""

    while(answer.lower() != 'y' and answer.lower() != 'n'):
        answer = input(question[mode] + "(y/n) ")

    if(answer.lower() == 'y'):
        return True
    
    return False
