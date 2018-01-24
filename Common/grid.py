""" Generate a Grid to be used by the client of the server"""
import math

class Grid():
    """ A grid """
    def __init__(self, game_rules):
        self.__n = game_rules["size_n"]
        self.__m = game_rules["size_m"]
        self.__grid = [
            [{
                "humans": 0,
                "werewolves": 0,
                "vampires": 0
            } for x in range(self.__n)] for y in range(self.__m)
        ]
        self.__number_of_humans = game_rules["number_of_humans"]
        self.__number_of_beasts = game_rules["number_of_beasts"]
        self.__werewolves_start = game_rules["werewolves_start"]
        self.__vampires_start = game_rules["vampires_start"]
        self.__number_of_homes = game_rules["number_of_homes"]
        self.__positions_of_homes = game_rules["positions_of_homes"]
        self.__add_players_spawns()
        self.__add_homes()

    def __repr__(self):
        drawing = [[] for x in range(self.__n)]
        for x in range(self.__n):
            for y in range(self.__m):
                if self.__grid[x][y]["humans"] != 0:
                    drawing[x].append("{}h".format(self.__grid[x][y]["humans"]))
                elif self.__grid[x][y]["vampires"] != 0:
                    drawing[x].append("{}v".format(self.__grid[x][y]["vampires"]))
                elif self.__grid[x][y]["werewolves"] != 0:
                    drawing[x].append("{}w".format(self.__grid[x][y]["werewolves"]))
                else:
                    drawing[x].append("xx")
        return str(drawing)

    def __add_players_spawns(self):
        """ Adds the players to the grid """
        # Werewolves
        self.__grid[self.__werewolves_start[0]][self.__werewolves_start[1]]["werewolves"] \
            = self.__number_of_beasts
        # Vampires
        self.__grid[self.__vampires_start[0]][self.__vampires_start[1]]["vampires"] \
            = self.__number_of_beasts

    def __add_homes(self):
        """ Add the homes to the map """
        for home in self.__positions_of_homes:
            self.__grid[home[0]][home[1]]["humans"] = math.floor(
                self.__number_of_humans / self.__number_of_homes
            )

    def compute_map(self):
        """ Computes the initial MAP message """
        number_of_orders = 0
        orders = []
        for i, line in enumerate(self.__grid):
            for j, column in enumerate(line):
                if self.__grid[i][j]["humans"] != 0:
                    number_of_orders += 1
                    orders.append(i)
                    orders.append(j)
                    orders.append(self.__grid[i][j]["humans"])
                    orders.append(0)
                    orders.append(0)
                if self.__grid[i][j]["vampires"] != 0:
                    number_of_orders += 1
                    orders.append(i)
                    orders.append(j)
                    orders.append(0)
                    orders.append(self.__grid[i][j]["vampires"])
                    orders.append(0)
                if self.__grid[i][j]["werewolves"] != 0:
                    number_of_orders += 1
                    orders.append(i)
                    orders.append(j)
                    orders.append(0)
                    orders.append(0)
                    orders.append(self.__grid[i][j]["werewolves"])
        return number_of_orders, orders

    def compute_upd(self, move):
        """ Computes the UPD message for a move """
