from generator import generate_field, shift, field_to_str, create_borders
import os


class Ship():
    """
    Class represents ship with (bow, is_horizontal, length) parameters
    """

    def __init__(self, bow, horizontal, length):
        """
        (tuple, bool, int) -> None

        Initialise Ship class
        """
        self.bow = bow
        self.horizontal = horizontal
        self.__length = length
        self.__hit = []

    def shoot_at(self, coord):
        """
        (tuple) -> None

        Function adds hit to ship
        """
        self.__hit.append(coord)

    def ship_coords(self):
        """
        Function returns coordinates of all parts of ship

        (None) -> list
        """
        if self.horizontal:
            res = [shift(self.bow, (i, 0)) for i in range(self.__length)]
        else:
            res = [shift(self.bow, (0, i)) for i in range(self.__length)]
        return res

    def is_hitted(self, coord):
        """
        (tuple) -> bool

        Function returnes True if ship hitted in certain coordinates
        """
        return coord in self.__hit

    def is_killed(self):
        """
        (None) -> bool

        Function returnes True if ship is killed
        """
        return len(self.__hit) == self.__length

    def get_length(self):
        """
        (None) -> int

        Function returns length of ship
        """
        return self.__length

    def get_borders(self):
        """
        (None) -> list

        Function returnes coordinates of borders of ship
        """
        borders = map(lambda x: (x[1]-1, ord(x[0])-65),
                      create_borders(self.bow, self.__length, "horizontal" if
                                     self.horizontal else "vertical"))
        return set(borders)-set(map(lambda x: (x[1]-1, ord(x[0])-65),
                                    self.ship_coords()))


class Field():
    """
    Function represents game field with automaticly generated board every time
    """

    def __init__(self):
        """
        (None) -> None

        Initialise Field class
        """
        lst = [Ship(i[0], True if i[2] == "horizontal" else False, i[1])
               for i in generate_field()]
        board = [[0 for x in range(10)] for y in range(10)]
        for i in lst:
            crd = list(map(lambda x: (x[1]-1, ord(x[0])-65), i.ship_coords()))
            for j in crd:
                board[j[0]][j[1]] = i
        self.board = board

    def shoot_at(self, coord):
        """
        (tuple) -> Ship or False

        Function tries to shoot on certain coordinates and returns
        Ship object if hit and False if not
        """
        if isinstance(self.board[coord[1]-1][ord(coord[0])-65], Ship):
            self.board[coord[1]-1][ord(coord[0])-65].shoot_at(coord)
            return self.board[coord[1]-1][ord(coord[0])-65]
        else:
            self.board[coord[1]-1][ord(coord[0])-65] = 3
            return False

    def field_without_ships(self):
        """
        (None) -> str

        Function returns formatted field without ships on it, but with hits
        """
        res = []
        coord = ("A", 1)
        for i in self.board:
            line = []
            for j in i:
                if isinstance(j, Ship):
                    if j.is_hitted(coord):
                        line.append(2)
                    else:
                        line.append(0)
                elif j == 3:
                    line.append(3)
                else:
                    line.append(0)

                coord = shift(coord, (1, 0))
            coord = shift(("A", coord[1]), (0, 1))
            res.append(line)
        return field_to_str(res)

    def field_with_ships(self):
        """
        (None) -> str

        Function returns formatted field
        """
        res = []
        coord = ("A", 1)
        for i in self.board:
            line = []
            for j in i:
                if isinstance(j, Ship):
                    if j.is_hitted(coord):
                        line.append(2)
                    else:
                        line.append(1)
                elif j == 3:
                    line.append(3)
                else:
                    line.append(0)

                coord = shift(coord, (1, 0))
            coord = shift(("A", coord[1]), (0, 1))
            res.append(line)
        return field_to_str(res)


class Player():
    """
    Class represents player with (name) parameter
    """

    def __init__(self, name):
        """
        (str) -> None

        Initialise Player class
        """
        self.__name = name
        self.kills = 0

    def read_position(self):
        """
        (None) -> tuple

        Function gets position of player's hit from keyboard
        """
        x = input(
            "Enter shoot coords:\ne.x: A, 2\n[{}] > ".format(self.__name))
        if "," in x and x.count(",") and x.split(",")[0] in "ABCDEFGHIJ" and\
                int(x.split(",")[1]) in range(1, 11):
            return (x.split(",")[0], int(x.split(",")[1]))
        else:
            print("Enter correct value!")
            return self.read_position()

    def request_field(self, field):
        """
        (Field) -> int

        Function generates field for player as many times as he want
        """
        os.system('cls')
        print("Here is your field [{}]:".format(self.__name))
        print(field.field_with_ships())
        x = input(
            "(1) - Regenerate\n(2) - Proceed\n [{}] > ".format(self.__name))
        if x in ["1", "2"]:
            return x
        else:
            return self.request_field(field)

    def get_name(self):
        """
        (None) ->str

        Function returnes players name
        """
        return self.__name

    def add_kill(self):
        """
        (None) -> None

        Function adds kills to player counter
        """
        self.kills += 1


class Game():
    """
    Class represents game with (field, players, current_player) parameters
    """

    def __init__(self, field, players, current_player):
        """
        (dict, list, Player) -> None

        Initialise Game class
        """
        self.__field = field
        self.__players = players
        self.__current_player = current_player

    def read_position(self):
        """
        (None) -> tuple

        Function gets position of current player's hit from keyboard
        """
        return self.__current_player.read_position()

    def field_without_ships(self, index):
        """
        (None) -> str

        Function returns formatted field without ships on it, but with hits
        """
        return self.__field[index].field_without_ships()

    def field_with_ships(self, index):
        """
        (None) -> str

        Function returns formatted field
        """
        return self.__field[index].field_with_ships()

    def run(self):
        """
        (None) -> None

        Main function of game: gives control to every player, up to the win
        """
        while True:
            # define players fields
            my_field = self.__field[self.__current_player.get_name()]
            enemy_field = self.__field[other_p(
                self.__current_player, self.__players).get_name()]

            # start player session
            print("[{}] is playing with {} kills".format(
                self.__current_player.get_name(),
                str(self.__current_player.kills)))
            print(concat_fields(enemy_field.field_without_ships(),
                                my_field.field_with_ships(), "        "))
            pos = self.read_position()
            to_pass = enemy_field.shoot_at(pos)
            os.system("cls")
            print(concat_fields(enemy_field.field_without_ships(),
                                my_field.field_with_ships(), "        "))
            if to_pass:
                # on hit
                os.system("cls")
                if to_pass.is_killed():
                    print("You killed {} HP ship".format(
                        str(to_pass.get_length())))
                    self.__current_player.add_kill()
                    for i in to_pass.get_borders():
                        enemy_field.board[i[0]][i[1]] = 3
                    enemy_field.board
                    if self.__current_player.kills == 10:
                        WINNER(self.__current_player.get_name())
                        break

                else:
                    print("Hoorey, you hitted")

            else:
                # give control to other player
                print("You missed")
                input(
                    "Control to player [{}] step 1/2\n[ENTER]".format(
                        self.__current_player.get_name()))
                os.system("cls")
                input(
                    "Control to player [{}] step 2/2\n[ENTER]".format(
                        self.__current_player.get_name()))
                os.system("cls")
                self.__current_player = other_p(
                    self.__current_player, self.__players)


def concat_fields(one, two, sep):
    """
    (str, str, str) -> str

    Function concat two multiline strings
    """
    line = ""
    s_one, s_two = one.split("\n"), two.split("\n")
    for i in range(len(s_one)):
        line += (s_one[i]+sep+s_two[i]+"\n")
    return line


def other_p(msg, lst):
    """
    (Player, list) -> Player

    Function returnes other player from list of 2
    """
    if msg == lst[0]:
        return lst[1]
    return lst[0]


def WINNER(name):
    """
    (str) -> None

    Function prints winner message
    """
    os.system("cls")
    print("Player [{}] WIN!".format(name))
