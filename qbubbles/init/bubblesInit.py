from qbubbles.bubbles import *

BUBBLES = []


# noinspection PyListCreation
def init_bubbles() -> List[Bubble]:
    BUBBLES.append(NormalBubble())
    BUBBLES.append(DoubleBubble())
    BUBBLES.append(TripleBubble())
    BUBBLES.append(DoubleStateBubble())
    BUBBLES.append(TripleStateBubble())
    BUBBLES.append(DamageBubble())
    return BUBBLES
