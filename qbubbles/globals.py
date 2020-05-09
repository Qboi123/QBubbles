from tkinter import Canvas as _Canvas
from typing import Dict as _Dict, Any as _Any, Optional as _Optional

NAME2EFFECT: _Dict[str, _Any] = {}
EFFECT2NAME: _Dict[_Any, str] = {}

CANVAS: _Optional[_Canvas] = None

GAME_VERSION = "1.0-alpha3"


def _get_maxbubbles(screensize: int):
    """
    Gets the maximum amount of bubbles.
    Calculate the screensize argument using: ``w*h``

    Example 1:
    ---------
    >>> import qbubbles.registry as _reg
    >>> w = _reg.Registry.gameData["WindowWidth"]
    >>> h = _reg.Registry.gameData["WindowHeight"]
    >>> screensize = w * h
    >>> _get_maxbubbles(screensize)  # Will return 103 if w = 1920 and h = 1080

    Example 2:
    -----------
    >>> w = 1920
    >>> h = 1080
    >>> screen = w * h
    >>> _get_maxbubbles(screensize)  # Will return 103

    :param screensize: Amount of all pixels on the screen. (1920x1080 = 2073600 Pixels = 103 Bubbles)
    :return:
    """

    return int(screensize / 20000)


GET_MAXBUBBLES = _get_maxbubbles
