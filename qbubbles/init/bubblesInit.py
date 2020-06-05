from qbubbles.bubbles import *

BUBBLES = []


# noinspection PyListCreation
def init_bubbles() -> List[Bubble]:
    BUBBLES.append(NormalBubble())

    # Double.
    BUBBLES.append(DoubleBubble())
    BUBBLES.append(DoubleStateBubble())

    # Triple.
    BUBBLES.append(TripleBubble())
    BUBBLES.append(TripleStateBubble())

    # Decuple.
    BUBBLES.append(DecupleBubble())
    BUBBLES.append(DecupleStateBubble())

    # Health changers.
    BUBBLES.append(DamageBubble())
    BUBBLES.append(HealBubble())

    # Effect holders.
    BUBBLES.append(SpeedBoostBubble())

    # Return Bubble list.
    return BUBBLES
