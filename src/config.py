'''
File berisi data config yang digunakan
'''

import sys
from pathlib import Path

sys.path.insert(0, str(Path(Path(__file__).parent).parent))

from data.input.dataex import dataSource as d1
from data.input.data1 import dataSource as d2
from data.input.data2 import dataSource as d3
from data.input.data3 import dataSource as d4
from data.input.data4 import dataSource as d5
from data.input.data5 import dataSource as d6

fileCSV = "solution5"
dataInput = d6

#Parameter loop
P = [0.5, 0.5, 0.5]
A = 2
B = 2
C = 2
#Jumlah Pengulangan
I = 3
M = 5
N = 5
ALPHA = 0.5
T0 = 10000

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