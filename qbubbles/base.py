from tkinter import Canvas
from typing import Optional, Union, Callable, List, Tuple

from qbubbles.events import UpdateEvent, CollisionEvent, KeyPressEvent, KeyReleaseEvent, XInputEvent, MouseEnterEvent, \
    MouseLeaveEvent, ResizeEvent
from qbubbles.registry import Registry
from qbubbles.sprite.abilities import Ability

HORIZONTAL = "horizontal"
VERTICAL = "vertical"

TYPE_DANGEROUS = "dangerous"
TYPE_NEUTRAL = "neutral"

FORM_CIRCLE = "circle"
FORM_RECT = "rectangle/line"
FORM_LINE = "rectangle/line"

BUB_NOSTATE = "nostate"
BUB_WITHSTATE = "withstate"

LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"

TRUE = True
FALSE = False

COLOR_RED = "red"

RED = COLOR_RED

ANY_BUBBLE = "any.bubble"
SHIP = "ship"

OBJ_SHIP = SHIP
OBJ_ANY_BUBBLE = ANY_BUBBLE
OBJ_BARIER = "barier"


# noinspection PyMissingConstructor
class StoreItem:
    def __init__(self, parent):
        self.parent = parent
        self.coins = 0
        self.diamonds = 0

    def __repr__(self):
        return f"StoreItem<{self.__class__.__name__}>"

    def on_buy(self, parent):
        pass

    def on_select(self, parent):
        pass


class Event:
    def __init__(self):
        pass

    def on_update(self, parent):
        pass

    def on_t_update(self, parent):
        pass


DirectionWaring = Warning


ActionIsNoneWarning = Warning
