TASK = (1,2,3,4,5,6,7,8,9,10,11)
STATIONS = [1,2,3,4]
MODEL = ['X','Y']

PRECEDENCES = [
    (1,2), (1,3), (1,4), (1,8),
    (2,7),
    (3,7),
    (4,5),
    (5,6),
    (6,7),
    (7,11),
    (8,9),
    (9,10),
    (10,11),
]

TIME_TAKEN = {
(1, 'X'): (1000,1,1000),
(1, 'Y'): (1000,1,1000),
(2, 'X'): (6.25,5,3.35),
(2, 'Y'): (0,0,0),
(3, 'X'): (1000,4,1000),
(3, 'Y'): (1000,4,1000),
(4, 'X'): (1000,0,1000),
(4, 'Y'): (1000,1,1000),
(5, 'X'): (0,0,1000),
(5, 'Y'): (6.25,5,1000),
(6, 'X'): (0,0,1000),
(6, 'Y'): (7.5,6,1000),
(7, 'X'): (1000,2,1000),
(7, 'Y'): (1000,2,1000),
(8, 'X'): (5,4,1000),
(8, 'Y'): (0,0,1000),
(9, 'X'): (1000,3,2.01),
(9, 'Y'): (1000,3,2.01),
(10, 'X'): (1000,0,0),
(10, 'Y'): (1000,5,3.35),
(11, 'X'): (1000,3,1000),
(11, 'Y'): (1000,3,1000),
}

SAVING = {
    1: (0,0),
    2: (1341,2593),
    3: (0,0),
    4: (0,0),    
    5: (2422,0),
    6: (2568,0),    
    7: (0,0),
    8: (1359,0),
    9: (0,0),
    10: (0,1932),
    11: (0,0),
}

CI = [500, 3500]
CO = [0.15625,0.02232]


CT = 10
D = 960

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
    'model' : MODEL
}