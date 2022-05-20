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

CI = [500, 3500]
CO = [1500, 300]

CT = 20
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
    'resources' : RESOURCES
}