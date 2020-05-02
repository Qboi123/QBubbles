GAMEMAPS = []


def init_gamemaps():
    from qbubbles.maps import ClassicMap

    GAMEMAPS.append(ClassicMap())
    return GAMEMAPS
