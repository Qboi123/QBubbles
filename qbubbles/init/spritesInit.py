SPRITES = []


def init_sprites():
    from qbubbles.bubbles import BubbleObject
    from qbubbles.sprites import Player

    SPRITES.append(BubbleObject())
    SPRITES.append(Player())
    return SPRITES
