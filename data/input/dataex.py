#EXAMPLE DATA, BASED ON initialSolutionEx

TASK = (1,2,3,4,5,6,7,8,9,10)
STATIONS = (1,2,3,4)

PRECEDENCES = [
    (1,2), (1,5),
    (2,7),
    (3,4),
    (4,5),
    (5,6),
    (6,8),
    (7,8),
    (8,9),
    (9,10),
]

TIME_TAKEN = {
    (1, 'X'): (13, 8, 100),
    (1, 'Y'): (4, 12, 100),
    (2, 'X'): (100, 10, 6),
    (2, 'Y'): (100, 6, 7),    
    (3, 'X'): (4, 3, 100),
    (3, 'Y'): (7, 5, 100),    
    (4, 'X'): (100, 0, 6),
    (4, 'Y'): (100, 5, 9),
    (5, 'X'): (9, 8, 100),
    (5, 'Y'): (7, 4, 100),
    (6, 'X'): (100, 9, 5),
    (6, 'Y'): (100, 5, 6),
    (7, 'X'): (100, 7, 8),
    (7, 'Y'): (100, 4, 5),
    (8, 'X'): (5, 8, 100),
    (8, 'Y'): (3, 2, 100),
    (9, 'X'): (8, 7, 100),
    (9, 'Y'): (5, 9, 100),
    (10, 'X'): (100, 3, 6),
    (10, 'Y'): (100, 2, 4), 
}

SAVING = {
    1: (3000, 0),
    2: (3500, 4350),
    3: (2800, 0),
    4: (3700, 4000),    
    5: (3000, 0),
    6: (2500, 3800),    
    7: (3100, 3400),
    8: (2500, 0),
    9: (2600, 0),
    10: (2400, 3500),
}

CI = [500, 3500]
CO = [1500, 300]


CT = 20
D = 2000

RESOURCES = {"R" : 1, "H" : 2, "HRC": 3}   

'''
Dictionary untuk eksport data input
'''
dataSource = {
    'task' : TASK,
    'stations' : STATIONS,
    'precedences'  : PRECEDENCES,
    'ci' : CI,
    'co' : CO,
    'ct' : CT,
    'resources' : RESOURCES,
    'timetaken' : TIME_TAKEN,
    'saving' : SAVING,
    'd' : D,
}