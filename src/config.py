'''
File berisi data config yang digunakan
'''

import sys
from pathlib import Path

sys.path.insert(0, str(Path(Path(__file__).parent).parent))

from data.input.dataex import dataSource as d1

fileCSV = "initialSolutionEx"
dataInput = d1

#Parameter loop
P = [0.5, 0.5, 0.5]
A = 1
B = 1
C = 1

#Jumlah Pengulangan
I = 1

PARAMETER = {
    'P' : P,
    'A' : A,
    'B' : B,
    'C' : C,
    'I' : I,
}