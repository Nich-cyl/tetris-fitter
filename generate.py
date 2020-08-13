"""GENERATES PROBLEM & SOLUTION BOARDS"""

import pyglet

"""(0,0) is in top left corner; +ve x = right; +ve y = down"""
I0 = ((1, 0), (2, 0), (3, 0))
I1 = ((0, 1), (0, 2), (0, 3))
O1 = ((0, 1), (1, 0), (1, 1))
T1 = ((1, 0), (2, 0), (1, 1))
T2 = ((0, 1), (0, 2), (-1, 1))  # -ve x
T3 = ((-1, 1), (0, 1), (1, 1))  # -ve x
T4 = ((0, 1), (0, 2), (1, 1))
L1 = ((1, 0), (2, 0), (0, 1))
L2 = ((1, 0), (1, 1), (1, 2))
L3 = ((1, 0), (2, 0), (2, -1))  # -ve y
L4 = ((0, 1), (0, 2), (1, 2))
J1 = ((1, 0), (2, 0), (2, 1))
J2 = ((0, 1), (0, 2), (-1, 2))  # -ve x
J3 = ((0, 1), (1, 1), (2, 1))
J4 = ((1, 0), (0, 1), (0, 2))
Z1 = ((1, 0), (1, 1), (2, 1))
Z2 = ((1, 0), (1, -1), (0, 1))  # -ve y
S1 = ((1, 0), (0, 1), (-1, 1))  # -ve x
S2 = ((0, 1), (1, 1), (1, 2))

blocks = {1:I0, 2:I1, 3:O1, 4:T1, 5:T4, 6:L1, 7:L2, 8:L4, 9:J1, 10:J3, 11:J4, 12:Z1, 13:S2,
          14:T2, 15:T3, 16:J2, 17:S1,  # -ve x
          18:L3, 19:Z2}                # -ve y

def print_block(entry_no, origin, increment, holding_arr, batch):
    global blocks
    holding_arr.append(pyglet.shapes.Rectangle(origin[0],
                                               origin[1],
                                               increment,increment,
                                               color=(0,0,255),
                                               batch=batch))
    for tile in blocks[entry_no]:
        holding_arr.append(pyglet.shapes.Rectangle(origin[0]+tile[0]*increment,
                                                   origin[1]-tile[1]*increment,
                                                   increment,increment,
                                                   color=(0,0,255),
                                                   batch=batch))

def gen(size, prbmat, solmat):
    pass
