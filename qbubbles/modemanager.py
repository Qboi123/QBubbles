from typing import Optional, Callable

from qbubbles.exceptions import ModeNotFoundError
from qbubbles.registry import Registry


class ModeManager(object):
    def __init__(self):
        self._modes = {}
        self.currentMode: Optional[Mode] = None
        self.currentModeName: Optional[str] = None

    def change_mode(self, name, *args, **kwargs):
        if not Registry.mode_exists(name):
            raise ModeNotFoundError(f"mode '{name}' not existent")

        # Hide old mode first
        if self.currentMode is not None:
            self.currentMode.stop_mode()

        # Get new mode and show it
        new_mode = Registry.get_mode(name)
        self.currentModeName = name
        self.currentMode: Mode = new_mode
        self.currentMode.start_mode(*args, **kwargs)


class Mode(object):
    modemanager = ModeManager()

    def __init__(self, name, start_func: Callable = None, stop_func: Callable = None):
        self._startFunc = start_func
        self._stopFunc = stop_func
        self.name = name

    def stop_mode(self, *args, **kwargs):
        self._stopFunc(*args, **kwargs)

    def start_mode(self, *args, **kwargs):
        self._startFunc(*args, **kwargs)

    def __repr__(self):
        return f"ModeObject<{self.__class__.__name__}>"


class TeleportMode(Mode):
    def __init__(self):
        super(TeleportMode, self).__init__("teleport")

        self.scene = Registry.get_scene("Game")

    def stop_mode(self, *args, **kwargs):
        pass
        # TeleportCrossbar()
