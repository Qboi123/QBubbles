import sys
from time import time

from main import Game, launcher_config
from qbubbles.utils import tkinter_excepthook

if __name__ == '__main__':
    sys.excepthook = tkinter_excepthook
    Game(launcher_config, time(), False)