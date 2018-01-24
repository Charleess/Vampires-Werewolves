""" Contains the Server class """
from threading import Thread
import socket
from .game import Game


class Server(Thread):
    """ Main server for the game """
    def __init__(self, port, parameters):
        Thread.__init__(self)
        if not isinstance(port, int):
            raise TypeError("[SERVER] Le port doit etre un entier")
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind(('localhost', port))
        self.__running = True
        self.__waiting_for_connexions = True
        self.__parameters = parameters

    def run(self):
        self.__sock.listen(2)  # On autorise deux connexions en attente à la fois
        print("[SERVER] En attente d'une connexion sur le serveur")
        connexions = []
        clients = []
        while self.__running:
            while self.__waiting_for_connexions:
                try:
                    connexion, client = self.__sock.accept()
                    connexions.append(connexion)
                    clients.append(client)
                    print("[SERVER] Connected to {}".format(client[1]))
                    try:
                        self.__waiting_for_connexions = \
                            not isinstance(connexions[0], socket.socket) & \
                            isinstance(connexions[1], socket.socket)
                    except IndexError:
                        self.__waiting_for_connexions = True
                except OSError as err:
                    # se produit quand on coupe la socket
                    print(err)

            print("[SERVER] Starting Game")
            current_game = Game(connexions, clients, self.__parameters)
            current_game.start()
            self.__running = (input("[SERVER] Press any key to quit...\n") is None)

        print("[SERVER] Arret du serveur")
        current_game.stop()
        current_game.join()
        self.__sock.close()
