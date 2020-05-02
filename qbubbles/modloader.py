import os
import string
from inspect import isclass, getfile
from typing import Optional
from zipimport import zipimporter
from functools import wraps

from qbubbles.globals import GAME_VERSION
from qbubbles.registry import Registry

MODS = []


def Addon(*, modid, name, version, qbversion=GAME_VERSION):
    if modid[0] not in string.ascii_letters:
        raise ValueError(f"Invalid character of modid {repr(modid)}: '{modid[0]}' must be a ASCII letter")
    for character in modid[1:]:
        if character not in string.ascii_letters+string.digits:
            raise ValueError(f"Invalid character of modid {repr(modid)}: '{character}' must be a ASCII letter")
    # print(modid, name, version, qbversion)

    def decorator(func):
        if not isclass(func):
            raise TypeError(f"Object '{func.__name___}' is not a class")
        if qbversion == GAME_VERSION:
            # MODS.append(dict(modid=modid, name=name, version=version, func=func))
            Registry.register_modobject(modid=modid, name=name, version=version, func=func)
            func.modID = modid
            func.name = name
            func.fpath = getfile(func)
            func.modPath = os.path.split(func.fpath)[0]
            func.version = version
            func.zipimport = None
    return decorator


class AddonSkeleton(object):
    modID: str
    name: str
    version: str
    fpath: str
    modPath: str
    zipimport: Optional[zipimporter]

    def __repr__(self):
        return f"Addon(<{self.modID}>)"
