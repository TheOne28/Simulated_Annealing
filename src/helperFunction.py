from distutils.command.config import config
from config import *

def validateResources(resource: str) -> bool:
    return resource in RESOURCES

def validateWaktu(waktu: int) -> bool:
    return waktu <= CT