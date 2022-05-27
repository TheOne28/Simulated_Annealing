from distutils.command.config import config
from config import *

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

def getInput():
    pass