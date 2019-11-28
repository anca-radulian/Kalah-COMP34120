import sys

"""
The main application class. It also provides methods for communication
with the game engine.
"""


class Main:

    # Sends a message to the game engine.
    def sendMsg(msg):
        print(msg, flush=True)

    # Receives a message from the game engine.
    def recvMsg(self):
        msg = sys.stdin.readline()
        return msg

    # The main method, invoked when the program is started.
    def main(self):
        return 0
