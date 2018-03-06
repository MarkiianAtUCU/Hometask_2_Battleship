import os
import random
from itertools import chain
import timeit


def field_to_str(data):
    x = """
       A B C D E F G H I J
     1 {} {} {} {} {} {} {} {} {} {}
     2 {} {} {} {} {} {} {} {} {} {}
     3 {} {} {} {} {} {} {} {} {} {}
     4 {} {} {} {} {} {} {} {} {} {}
     5 {} {} {} {} {} {} {} {} {} {}
     6 {} {} {} {} {} {} {} {} {} {}
     7 {} {} {} {} {} {} {} {} {} {}
     8 {} {} {} {} {} {} {} {} {} {}
     9 {} {} {} {} {} {} {} {} {} {}
    10 {} {} {} {} {} {} {} {} {} {}
    """
    return x.format(*["_" if i == 0 else "O" for i in chain(*data)])


def shift_i(coord, offset):
    return (chr(ord(coord[0]) + offset[0]), coord[1] + offset[1])


def create_borders(coord, length, v):
    res = []
    if v == "horizontal" or v == "central":
        coord = shift_i(coord, (-1, -1))
        for i in range(3):
            for j in range(length + 2):
                res.append(shift_i(coord, (j, i)))
    elif v == "vertical":
        coord = shift_i(coord, (-1, -1))
        for i in range(3):
            for j in range(length + 2):
                res.append(shift_i(coord, (i, j)))
    res_u = [i if (i[0] not in ["@", "K"]) and (
        i[1] not in [0, 11]) else -1 for i in res]

    return list(filter((-1).__ne__, res_u))


def check_ship(coord, length, v):
    if v == "horizontal":
        if ord(coord[0])+length > 74:
            return False
    else:
        if coord[1]+length > 10:
            return False
    return True


def check_available(all_p, other):
    if len(set(all_p).intersection(set(other))) == len(other):
        return list(set(all_p)-(set(other)))
    else:
        return False


def create_ship(coord, length, v):
    res = []
    if v == "horizontal":
        for j in range(length):
            res.append(shift_i(coord, (j, 0)))
    else:
        for j in range(length):
            res.append(shift_i(coord, (0, j)))
    return res


def generate_field():
    ships = []
    occ = []
    all_p = [(x, j) for x in "ABCDEFGHIJ" for j in range(1, 11)]
    for i in [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:
        x = True
        while x:
            rand_ship = (random.choice(all_p), i,
                         random.choice(["vertical", "horizontal"]))
            if check_ship(*rand_ship) and \
                    check_available(all_p, create_ship(*rand_ship)):
                all_p = list(set(all_p)-set(create_borders(*rand_ship)))
                ships.append(rand_ship)
                x = False
    return (ships)


def represent(coord):
    return(coord[1]-1, ord(coord[0])-65)


def create_board(data):

    board = [[0 for x in range(10)] for y in range(10)]
    coords = []
    for i in data:
        for j in create_ship(*i):
            coords.append(represent(j))
    for i in coords:
        board[i[0]][i[1]] = 1

    return board

board = create_board(generate_field())
print(board)