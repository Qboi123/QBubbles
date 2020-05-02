import traceback
from random import randint, Random
from tkinter import Canvas
from typing import Dict, Any, List, Tuple

from deprecated import deprecated

from qbubbles.bubble import create_bubble, Registry
from qbubbles.bubbles import Bubble
from qbubbles.components import SpecialMode
from qbubbles.config import Reader


class BubbleSystem(object):
    _bubblePriorities: List[Tuple] = []
    _maxPriority: int = 0

    @classmethod
    def init(cls, bubbles: List[Bubble] = None):
        if bubbles is None:
            bubbles: Tuple[Bubble] = Registry.get_bubbles()
        BubbleSystem._bubblePriorities = []
        BubbleSystem._maxPriority = 0

        for bubble in bubbles:
            BubbleSystem._bubblePriorities.append(
                (bubble, BubbleSystem._maxPriority, BubbleSystem._maxPriority + bubble.priority))
            BubbleSystem._maxPriority += bubble.priority

    @classmethod
    def random(cls, rand: Random):
        integer = rand.randint(0, cls._maxPriority)
        for priority in cls._bubblePriorities:
            # print(priority, integer)
            if priority[1] <= integer <= priority[2]:
                return priority[0]


# noinspection PyUnresolvedReferences
@deprecated("Implemented in gamemaps")
def start(bubble: Dict[str, Any], save_name: str, stats: Dict[str, Any], config: Dict[str, Any], bub,
          modes: Dict[str, bool], canvas: Canvas):
    try:
        if len(Registry.saveData["Sprites"]["qbubbles:bubble"]["objects"]) == 0:
            r_start(bubble, stats, config, bub, canvas)
            return
        print(bubs)
        for i in range(len(bubs["bub-id"])):
            bubble["active2"].append(False)
            # print(i)
        for i in range(len(bubs["bub-id"]) - 1):
            if bubs["bub-special"]:
                create_bubble(stats, config, bub, canvas, bubble, bubs["bub-index"][i],
                              bubs["bub-position"][i][0],
                              bubs["bub-position"][i][1], bubs["bub-radius"][i], bubs["bub-speed"][i])
            elif not bubs["bub-special"]:
                SpecialMode.create_bubble(canvas, config, bubble, stats, bub, bubs["bub-index"][i],
                                          bubs["bub-position"][i][0],
                                          bubs["bub-position"][i][1], bubs["bub-radius"][i], bubs["bub-speed"][i])
    except Exception as e:
        from inspect import currentframe
        import sys
        print(f"Error at line {currentframe().f_lineno} in {__file__}: {e.__class__.__name__}: {e.__str__()}", file=sys.stderr)


@deprecated("Implemented in gamemaps")
def r_start(bubble: Dict[str, Any], stats: Dict[str, Any], config: Dict[str, Any], bub, canvas: Canvas):
    try:
        for i in range(int((config["width"] - 72) / 10)):
            bubble["active2"].append(False)
            # print(i)

        # print(int((config["width"] - 72) / 10))
        for i in range(int((config["width"] - 73) / 10)):
            # print(i)
            r = randint(int(config["Bubble"]["min-radius"]),
                        int(config["Bubble"]["max-radius"]))
            x = randint(-r, config["width"] + r)
            y = randint(72 + r, (config["height"] - r))
            # spd = stats["bubspeed"]
            # i = randint(0, 1600)
            create_bubble(stats, config, bub, canvas, bubble, x=x, y=y, r=r)
    except Exception as e:
        from inspect import currentframe
        import sys
        print(f"Error at line {currentframe().f_lineno} in {__file__}: {e.__class__.__name__}: {e.__str__()}", file=sys.stderr)
