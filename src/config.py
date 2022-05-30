'''
File berisi data config yang digunakan
'''

import sys
from pathlib import Path

sys.path.insert(0, str(Path(Path(__file__).parent).parent))

from data.input.dataex import dataSource as d1

fileCSV = "initialSolutionEx"
dataInput = d1

