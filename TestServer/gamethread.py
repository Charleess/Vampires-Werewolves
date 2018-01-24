""" Contains the GameThread class """
from threading import Thread
import socket
import struct
from Common.grid import Grid

class GameThread(Thread):
    """ A thread to communicate with a client """
    def __init__(self, sock, client, rules, name, data_queue):
        Thread.__init__(self)
        if not isinstance(sock, socket.socket) or sock is None:
            raise TypeError("Necessite une vraie socket")
        self.__socket = sock
        self.__client = client
        self.__rules = rules
        self.__name = name
        self.__data_queue = data_queue
        self.__grid = Grid(self.__rules)

    def __getcommand(self):
        data = bytes()
        while len(data) < 3:
            data += self.__socket.recv(3 - len(data))
        return data.decode("ascii")

    def __createcommand(self, ordre):
        if ordre == "SET":
            code = "SET".encode("ascii")
            command = struct.pack(
                "1q1q", self.__rules["size_n"], self.__rules["size_m"]
            )
            commands = [code, command]

        elif ordre == "HUM":
            code = "HUM".encode("ascii")
            positions_of_homes = []
            for home in self.__rules["positions_of_homes"]:
                positions_of_homes.append(home[0])
                positions_of_homes.append(home[1])

            command_1 = struct.pack(
                "1q", self.__rules["number_of_homes"]
            )
            command_2 = struct.pack(
                "{}q".format(self.__rules["number_of_homes"] * 2), *positions_of_homes
            )
            commands = [code, command_1, command_2]

        elif ordre == "HME":
            code = "HME".encode("ascii")
            command = struct.pack(
                "1q1q", \
                self.__rules["{}_start".format(self.__name)][0], \
                self.__rules["{}_start".format(self.__name)][1]
            )
            commands = [code, command]

        elif ordre == "MAP":
            # Send the command...
            number_of_orders, orders = self.__grid.compute_map()
            code = "MAP".encode("ascii")
            command_1 = struct.pack(
                "1q", number_of_orders
            )
            command_2 = struct.pack(
                "{}q".format(number_of_orders * 5), \
                *orders
            )
            commands = [code, command_1, command_2]

        elif ordre == "END":
            commands = [struct.pack("3s", "END".encode("ascii"))]

        elif ordre == "BYE":
            commands = [struct.pack("3s", "BYE".encode("ascii"))]

        else:
            commands = None

        return commands

    def __sendcommands(self, commands):
        if commands:
            for command in commands:
                self.__socket.send(command)
        else:
            print(
                "[GAMETHREAD - {}] La commande n'est pas reconnue".format(
                    self.__name.capitalize()
                )
            )

    def __printerror(self, message):
        print(message)
        try:
            self.__socket.close()
        except Exception:
            print(
                "[GAMETHREAD - {}] Erreur lors de la fermeture de la socket".format(
                    self.__name.capitalize()
                )
            )

    def run(self):
        print("[GAMETHREAD - {}] Just connected".format(self.__name.capitalize()))

        # Implementation du protocole
        # L'idée est d'attendre en permanence une instruction du master
        commande = self.__getcommand()
        if commande != "NME":
            self.__printerror(
                "[GAMETHREAD - {}] Erreur de protocole: attendu NME".format(
                    self.__name.capitalize()
                )
            )
            return
        else:
            print(
                "[GAMETHREAD - {}] Reçu NME".format(self.__name.capitalize())
            )
            print(
                "[GAMETHREAD - {}] Starting Initialization".format(self.__name.capitalize())
            )
            self.__data_queue.put("Hello from {}".format(self.name))
            # On peut envoyer les différentes informations de jeu
            self.__sendcommands(self.__createcommand("SET"))
            self.__sendcommands(self.__createcommand("HUM"))
            self.__sendcommands(self.__createcommand("HME"))
            self.__sendcommands(self.__createcommand("MAP"))

        self.__socket.close()

    def stop(self):
        """ Close the socket correctly """
        print("[GAMETHREAD - {}] Closing Socket".format(self.__name.capitalize()))
        self.__socket.close()
