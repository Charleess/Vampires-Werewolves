""" Contains the GameRules class """
import math
from random import randint

class GameRules():
    """ A set of rules for the Vampires vs Humans vs Werewolves game """
    def __init__(self, parameters):
        self.__size_n = parameters["size_n"]
        self.__size_m = parameters["size_m"]
        self.__humans = parameters["humans"]
        self.__beasts = parameters["beasts"]
        self.rules = {}

    def creategame(self):
        """ Generates a new game """
        used_spots = set()
        # Homes
        number_of_homes = math.ceil((self.__size_m + self.__size_m) / 12)
        # Position of the homes
        positions_of_homes = set()
        while len(positions_of_homes) < number_of_homes:
            coord_1 = randint(0, self.__size_n - 1)
            coord_2 = randint(0, self.__size_m - 1)
            positions_of_homes.add((coord_1, coord_2))
            used_spots.add((coord_1, coord_2))

        # Player spawn
        tmp = len(used_spots)
        while len(used_spots) == tmp:
            player1_start = (randint(0, self.__size_n - 1), randint(0, self.__size_m - 1))
            used_spots.add(player1_start)

        tmp = len(used_spots)
        while len(used_spots) == tmp:
            player2_start = (randint(0, self.__size_n - 1), randint(0, self.__size_m - 1))
            used_spots.add(player2_start)

        self.rules = {
            "size_n": self.__size_n,
            "size_m": self.__size_m,
            "number_of_humans": self.__humans,
            "number_of_beasts": self.__beasts,
            "number_of_homes": number_of_homes,
            "positions_of_homes": positions_of_homes,
            "vampires_start": player2_start,
            "werewolves_start": player1_start
        }

        print("[GAMERULES] Initialized Rules")

        return self.rules

    def loadgame(self, map_commands):
        """ Generates a GameRule object from a config """
        number_of_homes = 0
        positions_of_homes = []

        for command in map_commands:
            if command[2] != 0:
                number_of_homes += 1
                positions_of_homes.append((command[0], command[1]))
            if command[3] != 0:
                vampires_start = (command[0], command[1])
            if command[4] != 0:
                werewolves_start = (command[0], command[1])

        self.rules = {
            "size_n": self.__size_n,
            "size_m": self.__size_m,
            "number_of_humans": self.__humans,
            "number_of_beasts": self.__beasts,
            "number_of_homes": number_of_homes,
            "positions_of_homes": positions_of_homes,
            "vampires_start": vampires_start,
            "werewolves_start": werewolves_start
        }
