from qbubbles.effects import ScoreMultiplierEffect, SpeedBoostEffect

EFFECTS = []


def init_effects():
    EFFECTS.append(ScoreMultiplierEffect())
    EFFECTS.append(SpeedBoostEffect())

    return EFFECTS
