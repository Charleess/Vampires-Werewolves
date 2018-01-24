""" Main EntryPoint for the game """
from TestServer.server import Server
from Player.V0.player import Player

PORT = 555
PARAMETERS = {
    "size_n": 10,
    "size_m": 10,
    "humans": 15,
    "beasts": 15
}

if __name__ == '__main__':
    # Lancement du serveur (comme un thread)
    SERVER = Server(PORT, PARAMETERS)
    SERVER.start()
    PLAYER_1 = Player(PORT, PARAMETERS, "vampires")
    PLAYER_2 = Player(PORT, PARAMETERS, "werewolves")
    PLAYER_1.start()
    PLAYER_2.start()
