from battleship import *
import logo


def main():
    os.system("cls")
    logo.logo()
    os.system("cls")

    # Initialise first player
    first = Player(input("Enter your name, captain:\n[o] > "))
    field_one = Field()
    while first.request_field(field_one) != "2":
        field_one = Field()
    input("Hit [Enter] to give control to other player:")

    # Initialise second player
    os.system('cls')
    second_in = input("Enter your name, captain:\n[o] >")
    while second_in == first.get_name():
        print("Enter other name:")
        second_in = input("Enter your name, captain:\n[o] >")
    second = Player(second_in)

    field_two = Field()
    while second.request_field(field_two) != "2":
        field_two = Field()

    input("Hit [Enter] to give control to other player step [1/2]:")
    os.system("cls")
    input("Hit [Enter] to give control to other player step [2/2]:")
    os.system("cls")

    # Start game
    x = Game({first.get_name(): field_one, second.get_name(): field_two},
             [first, second], first)
    x.run()
    if input("Play again?").uppercase() == "YES":
        main()


main()
