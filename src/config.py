'''
File berisi data config yang digunakan
'''

from re import M
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
M = 1
N = 1
ALPHA = 1
T0 = 1

Parameter = {
    'P' : P,
    'A' : A,
    'B' : B,
    'C' : C,
    'I' : I,
    'M' : M,
    'N' : N,
    'ALPHA' : ALPHA,
    'T0' : T0,
}