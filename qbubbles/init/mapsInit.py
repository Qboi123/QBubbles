from qbubbles.maps import DimensionalMap, ClassicMap

GAMEMAPS = []


def init_gamemaps():
    GAMEMAPS.append(ClassicMap())
    GAMEMAPS.append(DimensionalMap())
    return GAMEMAPS
