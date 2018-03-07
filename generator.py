import os
import random
from itertools import chain


def field_to_str(data):
    """
    (list) -> str

    Function represents two dimensional list as battleship field
    """
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
    return x.format(*["_" if i == 0 else "O" if i == 1 else "X" if i == 2
                      else "·" for i in chain(*data)])


def shift(coord, offset):
    """
    (tuple, tuple) -> tuple

    Function shifts coord on defined offset
    """
    return (chr(ord(coord[0]) + offset[0]), coord[1] + offset[1])


def create_borders(coord, length, v):
    """
    (tuple, int, str) -> list

    Function generate borders around the ship in battleship game
    (if borders are outside field - removes that coordinates)
    """
    coord = shift(coord, (-1, -1))
    if v == "horizontal":
        res = [shift(coord, (j, i)) for i in range(3) for j in range(length+2)]

    elif v == "vertical":
        res = [shift(coord, (i, j)) for i in range(3) for j in range(length+2)]

    res_u = list(filter(lambda x: x[0] not in [
                 "@", "K"] and x[1] not in [0, 11], res))
    return res_u


def check_ship(coord, length, v):
    """
    (tuple, int, str) -> bool

    Function checks if certain ship can be placed on blank field
    """
    if v == "horizontal":
        if ord(coord[0])+length > 74:
            return False
    else:
        if coord[1]+length > 10:
            return False
    return True


def check_available(all_p, other):
    """
    (list, list) -> bool

    Function checks if coordinates are available for ship placement
    """
    return len(set(all_p).intersection(set(other))) == len(other)


def create_ship(coord, length, v):
    """
    (tuple, int, str) -> list

    Function generates ship coordinates
    """
    if v == "horizontal":
        res = [shift(coord, (i, 0)) for i in range(length)]
    else:
        res = [shift(coord, (0, i)) for i in range(length)]
    return res


def generate_field():
    """
    (None) -> list

    Function generates random field for battleship (always correct,
    so there is no need to check it XD)
    """
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
    return ships
