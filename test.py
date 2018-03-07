from itertools import chain
import random
import os


def has_ship(data, coord):
    """
    (list, tuple) -> bool

    Function checks if there is sheep on following coordinates
    """
    return data[coord[1] - 1][ord(coord[0]) - 65] == 1


def get_area(data, coord):
    """
    (list, tuple) -> dict

    Function returnes neighbours of cell
    """
    res = {}
    names = ["central", "left", "right", "up", "down"]
    c = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(5):
        if shift(coord, c[i]) != -1:
            if has_ship(data, shift(coord, c[i])):
                res[names[i]] = shift(coord, c[i])

    for i in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        if shift(coord, i) != -1:
            if has_ship(data, shift(coord, i)):
                res["d"] = shift(coord, i)
    return res


def ship_size(data, coord):
    """
    (list, tuple) -> tuple

    Function returnes info about ship (bow coordinates, length, orientation)
    """
    # define vector of shop
    it = get_area(data, coord)
    if not has_ship(data, coord):
        return -1
    if len(it) > 3:
        return -1
    if (("up" in it and "down" in it) or ("up" in it) or ("down" in it))\
            and "central" in it:
        v = "vertical"
    elif (("left" in it and "right" in it) or ("left" in it)
          or ("right" in it)) and "central" in it:
        v = "horizontal"
    elif len(it) == 1 and "central" in it:
        v = "central"
        res_c = coord
        res = 1
    elif "d" in it:
        return -1

    if v == "horizontal":
        # move to most left corner
        for i in range(10):
            st = get_area(data, coord)
            if "left" in st:
                coord = shift(coord, (-1, 0))
            else:
                break
        res_c = coord
        res = 0

        # measure and check ship correctness
        for i in range(10):
            st = get_area(data, coord)
            if (("up" not in st) and ("down" not in st) and ("d" not in st)):
                if "right" in st:
                    coord = shift(coord, (1, 0))
                    res += 1
                else:
                    break
            else:
                return -1

    elif v == "vertical":
        # move to upper corner
        for i in range(10):
            st = get_area(data, coord)
            if "up" in st:
                coord = shift(coord, (0, -1))
            else:
                break
        res_c = coord
        res = 0
        for i in range(10):
            # measure and check ship correctness
            st = get_area(data, coord)
            if (("right" not in st) and ("left" not in st) and
                    ("d" not in st)):
                if "down" in st:
                    coord = shift(coord, (0, 1))
                    res += 1
                else:
                    break
            else:
                return -1
    else:
        return (res_c, 1, v)

    return (res_c, res + 1, v)


def is_valid(data):
    """
    (list) -> int

    Check validity of battleship board
    """
    res = []
    ship_1 = 0
    ship_2 = 0
    ship_3 = 0
    ship_4 = 0

    for i in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
        for j in range(1, 11):
            if has_ship(data, (i, j)):
                res.append(ship_size(data, (i, j)))

    if -1 in list(set(res)):
        return False
    for i in list(set(res)):
        if i[1] < 5:
            if i[1] == 1:
                ship_1 += 1
            elif i[1] == 2:
                ship_2 += 1
            elif i[1] == 3:
                ship_3 += 1
            elif i[1] == 4:
                ship_4 += 1
        else:
            return False
    if ship_1 != 4 or ship_2 != 3 or ship_3 != 2 or ship_4 != 1:
        return False

    return res


def shift(coord, offset):
    """
    (tuple, tuple) -> tuple

    Function shifts coord on defined offset and check correctness of
    shifted coordinates
    """
    res = (chr(ord(coord[0]) + offset[0]), coord[1] + offset[1])
    if "@" not in res and "K" not in res and 1 not in res and 11 not in res:
        return res
    else:
        return -1
