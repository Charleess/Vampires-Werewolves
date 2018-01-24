""" Contains the Player class """
from threading import Thread
import socket
import struct
from Common.grid import Grid
from Common.gamerules import GameRules

class Player(Thread):
    """ A player """
    def __init__(self, port, parameters, player_name):
        Thread.__init__(self)
        self.__parameters = parameters
        self.__player_name = player_name
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect(('localhost', port))
        self.__gamerules = None
        self.__grid = None

    def __receive_data(self, size, fmt):
        data = bytes()
        while len(data) < size:
            data += self.__sock.recv(size - len(data))
        return struct.unpack(fmt, data)

    @staticmethod
    def __grouper(_n, iterable):
        args = [iter(iterable)] * _n
        return zip(*args)

    def run(self):
        print("[PLAYER - {}] Démarrage".format(self.__player_name.capitalize()))
        self.__sock.send("NME".encode("ascii"))
        # Initialization
        # SET
        header = self.__sock.recv(3).decode("ascii")
        if header.strip() != "SET":
            print("[PLAYER - {}] Protocol Error at SET".format(self.__player_name.capitalize()))
        else:
            size_n, size_m = self.__receive_data(16, "1q1q")

        # HUM
        header = self.__sock.recv(3).decode("ascii")
        if header.strip() != "HUM":
            print("[PLAYER - {}] Protocol Error at HUM".format(self.__player_name.capitalize()))
        else:
            number_of_homes = self.__receive_data(8, "1q")[0]
            homes_raw = self.__receive_data(
                number_of_homes * 2 * 8, "{}q".format(number_of_homes * 2)
            )
            homes = list(self.__grouper(2, homes_raw))

        # HME
        header = self.__sock.recv(3).decode("ascii")
        if header.strip() != "HME":
            print("[PLAYER - {}] Protocol Error at HME".format(self.__player_name.capitalize()))
        else:
            start_position = self.__receive_data(16, "1q1q")

        # MAP
        header = self.__sock.recv(3).decode("ascii")
        if header.strip() != "MAP":
            print("[PLAYER - {}] Protocol Error at HME".format(self.__player_name.capitalize()))
        else:
            number_map_commands = self.__receive_data(8, "1q")[0]
            map_commands_raw = self.__receive_data(
                number_map_commands * 8 * 5, "{}q".format(number_map_commands * 5)
            )
            map_commands = list(self.__grouper(5, map_commands_raw))

        # A ce stade, toutes les infos nécessaires sont disponibles
        print(
            "[PLAYER - {}] Received all the data. Initializing map".format(
                self.__player_name.capitalize()
            )
        )

        self.__gamerules = GameRules(self.__parameters)
        self.__gamerules.loadgame(map_commands)
        self.__grid = Grid(self.__gamerules.rules)

        print(
            "[PLAYER - {}] Map done: {}".format(
                self.__player_name.capitalize(),
                self.__grid
            )
        )