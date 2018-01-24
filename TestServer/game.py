""" Contains the Game class """
from threading import Thread
import socket
from queue import Queue
from Common.gamerules import GameRules
from Common.grid import Grid
from TestServer.gamethread import GameThread

class Game(Thread):
    """ A game between two clients """
    def __init__(self, socks, clients, parameters):
        Thread.__init__(self)
        if not isinstance(socks[0], socket.socket) or \
            not isinstance(socks[0], socket.socket) or \
            socks[0] is None or \
            socks[1] is None:
            raise TypeError("Necessite une vraie socket")
        self.__sockets = socks
        self.__clients = clients
        self.__vampires_thread = None
        self.__werewolves_thread = None
        self.__data_queue = Queue()
        self.__rules = GameRules(parameters).creategame()
        self.__grid = Grid(self.__rules)
        print("[GAME] Map initialized")
        print("[GAME] Rules: {}".format(self.__rules))

    def run(self):
        """ Start the game """
        print("[GAME] Starting Vampires")
        self.__vampires_thread = GameThread(
            self.__sockets[0], self.__clients[0], self.__rules, "vampires", self.__data_queue
        )
        self.__vampires_thread.start()

        print("[GAME] Starting Werewolves")
        self.__werewolves_thread = GameThread(
            self.__sockets[1], self.__clients[1], self.__rules, "werewolves", self.__data_queue
        )
        self.__werewolves_thread.start()

        # L'idée est d'utiliser une Queue pour traiter les demandes

    def stop(self):
        """ Stops the game and closes the sockets """
        self.__vampires_thread.stop()
        self.__werewolves_thread.stop()
        self.__vampires_thread.join()
        self.__werewolves_thread.join()
