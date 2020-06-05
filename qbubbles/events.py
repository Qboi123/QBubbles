import tkinter as _tk
import typing as _t

from qbubbles.lib.xbox import XboxController as _XboxController
from qbubbles.scenemanager import Scene as _Scene


class Event(object):
    _handlers = list()

    def __init__(self, scene):
        self.frame = scene.frame
        # self.audio = scene.audio
        self.scene = scene
        self.cancel = False

        for handler in self._handlers:
            if handler(self) == "cancel":
                self.cancel = True

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class ExperienceEvent(Event):
    _handlers = list()

    def __init__(self, scene, experience):
        self.experience = experience

        super(ExperienceEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['ExperienceEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['ExperienceEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class LanguageChangeEvent(Event):
    _handlers = list()

    def __init__(self, scene, langid):
        self.langid = langid

        super(LanguageChangeEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['LanguageChangeEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['LanguageChangeEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


# noinspection PyUnusedLocal
class PreInitializeEvent(Event):
    _handlers = list()

    def __init__(self, scene, canvas, t1, t2):
        # self.experience = experience
        self.canvas = canvas
        self.t2 = t2

        for handler in self._handlers:
            canvas.itemconfig(t1, text=f"Pre initialize mod '{handler.__self__.name}'")
            handler(self)

        super(Event, self).__init__()

    @classmethod
    def bind(cls, func: _t.Callable[['PreInitializeEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['PreInitializeEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


# noinspection PyUnusedLocal
class InitializeEvent(Event):
    _handlers = list()

    def __init__(self, scene, canvas, t1, t2):
        # self.experience = experience
        self.canvas = canvas
        self.t2 = t2

        for handler in self._handlers:
            canvas.itemconfig(t1, text=f"Initialize mod '{handler.__self__.name}'")
            handler(self)

        super(Event, self).__init__()

    @classmethod
    def bind(cls, func: _t.Callable[['InitializeEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['InitializeEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


# noinspection PyUnusedLocal
class PostInitializeEvent(Event):
    _handlers = list()

    def __init__(self, scene, canvas, t1, t2):
        # self.experience = experience
        self.canvas = canvas
        self.t2 = t2

        for handler in self._handlers:
            canvas.itemconfig(t1, text=f"Post initialize mod '{handler.__self__.name}'")
            handler(self)

        super(Event, self).__init__()

    @classmethod
    def bind(cls, func: _t.Callable[['PostInitializeEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['PostInitializeEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class ResizeEvent(Event):
    _handlers = list()

    def __init__(self, scene, width, height):
        self.width = width
        self.height = height

        super(ResizeEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['ResizeEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['ResizeEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class SavedataReadedEvent(Event):
    _handlers = list()

    def __init__(self, data):
        super(Event, self).__init__()

        for handler in self._handlers:
            handler(data)

    @classmethod
    def bind(cls, func: _t.Callable[['_t.Any'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['_t.Any'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class UpdatableEvent(Event):
    _handlers = list()

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


# noinspection PyMethodOverriding,PyShadowingBuiltins
class CanvasIDEvent(Event):
    _handlers = dict()
    event = ""

    def __init__(self, scene):
        super(CanvasIDEvent, self).__init__(scene)

    @classmethod
    def _call(cls, scene, event):
        cls(scene)

    @classmethod
    def bind(cls, func, id: int, canvas: _tk.Canvas, scene):
        cls._handlers[func] = canvas.tag_bind(id, cls.event, lambda event: cls._call(scene, event))
        # print(func)
        return func

    @classmethod
    def unbind(cls, func, id, canvas: _tk.Canvas, scene):
        canvas.tag_unbind(id, cls.event, cls._handlers[func])
        del cls._handlers[func]
        # print(f"Unbind: {func.__name__}")
        return func


# noinspection PyShadowingBuiltins
class MouseEnterEvent(CanvasIDEvent):
    _handlers = dict()
    event = "<Enter>"

    def __init__(self, scene, x, y):
        self.x = x
        self.y = y
        super(MouseEnterEvent, self).__init__(scene)

    @classmethod
    def _call(cls, scene, event):
        cls(scene, event.x, event.y)

    @classmethod
    def bind(cls, func, id: int, canvas: _tk.Canvas, scene):
        cls._handlers[func] = canvas.tag_bind(id, cls.event, lambda event: cls._call(scene, event))
        # print(func)
        return func

    @classmethod
    def unbind(cls, func, id, canvas: _tk.Canvas, scene):
        canvas.tag_unbind(id, cls.event, cls._handlers[func])
        del cls._handlers[func]
        # print(f"Unbind: {func.__name__}")
        return func


# noinspection PyMethodOverriding,PyShadowingBuiltins
class MouseLeaveEvent(CanvasIDEvent):
    _handlers = dict()
    event = "<Leave>"

    def __init__(self, scene, x, y):
        self.x = x
        self.y = y
        super(MouseLeaveEvent, self).__init__(scene)

    @classmethod
    def _call(cls, scene, event):
        cls(scene, event.x, event.y)

    @classmethod
    def bind(cls, func, id: int, canvas: _tk.Canvas, scene):
        cls._handlers[func] = canvas.tag_bind(id, cls.event, lambda event: cls._call(scene, event))
        # print(func)
        return func

    @classmethod
    def unbind(cls, func, id, canvas: _tk.Canvas, scene):
        canvas.tag_unbind(id, cls.event, cls._handlers[func])
        del cls._handlers[func]
        # print(f"Unbind: {func.__name__}")
        return func


class KeyPressEvent(Event):
    _handlers = list()

    def __init__(self, scene, tkevent):
        self.keySym = tkevent.keysym
        self.char = tkevent.char

        super(KeyPressEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['KeyPressEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['KeyPressEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class SpriteDamageEvent(Event):
    _handlers = list()

    def __init__(self, scene, sprite):
        self.sprite = sprite

        super(SpriteDamageEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['SpriteDamageEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['SpriteDamageEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class MapInitializeEvent(Event):
    _handlers = list()

    def __init__(self, scene, t1, t2, save_name):
        if scene.__class__.__name__ != "Game":
            raise RuntimeError("Scene must be specific a Game instance")
        self.canvas = scene.canvas
        self.t1 = t1
        self.t2 = t2
        self.saveName = save_name

        super(MapInitializeEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['MapInitializeEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['MapInitializeEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class FirstLoadEvent(Event):
    _handlers = list()

    def __init__(self, scene, t1, t2, save_name):
        if scene.__class__.__name__ != "Game":
            raise RuntimeError("Scene must be specific a Game instance")
        self.canvas = scene.canvas
        self.t1 = t1
        self.t2 = t2
        self.saveName = save_name

        super(FirstLoadEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['FirstLoadEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['FirstLoadEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class SaveEvent(Event):
    _handlers = list()

    def __init__(self, scene, save_name):
        if scene.__class__.__name__ != "Game":
            raise RuntimeError("Scene must be specific a Game instance")
        self.canvas = scene.canvas
        self.saveName = save_name

        super(SaveEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['SaveEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['SaveEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class LoadCompleteEvent(Event):
    _handlers = list()

    def __init__(self, scene, save_name):
        if scene.__class__.__name__ != "Game":
            raise RuntimeError("Scene must be specific a Game instance")
        self.canvas = scene.canvas
        self.saveName = save_name

        super(LoadCompleteEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['LoadCompleteEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['LoadCompleteEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class GameExitEvent(Event):
    _handlers = list()

    def __init__(self, scene, save_name):
        if scene.__class__.__name__ != "Game":
            raise RuntimeError("Scene must be specific a Game instance")
        self.canvas = scene.canvas
        self.saveName = save_name

        super(GameExitEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['GameExitEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['GameExitEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class CleanUpEvent(Event):
    _handlers = list()

    def __init__(self, scene):
        if scene.__class__.__name__ != "Game":
            raise RuntimeError("Scene must be specific a Game instance")
        self.canvas = scene.canvas
        super(CleanUpEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['CleanUpEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['CleanUpEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class RegionEnterEvent(Event):
    _handlers = list()

    def __init__(self, scene, region: _t.Tuple[int, int]):
        if scene.__class__.__name__ != "Game":
            raise RuntimeError("Scene must be specific a Game instance")
        self.canvas = scene.canvas
        self.region = region
        super(RegionEnterEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['RegionEnterEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['RegionEnterEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class RegionLeaveEvent(Event):
    _handlers = list()

    def __init__(self, scene, region: _t.Tuple[int, int]):
        if scene.__class__.__name__ != "Game":
            raise RuntimeError("Scene must be specific a Game instance")
        self.canvas = scene.canvas
        self.region = region
        super(RegionLeaveEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['RegionLeaveEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['RegionLeaveEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class KeyReleaseEvent(Event):
    _handlers = list()

    def __init__(self, scene, tkevent):
        self.keySym = tkevent.keysym
        self.char = tkevent.char

        super(KeyReleaseEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['KeyReleaseEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['KeyReleaseEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class UpdateEvent(Event):
    _handlers = list()

    def __init__(self, scene: _Scene, dt: float, canvas: _tk.Canvas):
        self.dt: float = dt
        self.canvas: _tk.Canvas = canvas

        # print(len(self._handlers))

        super(UpdateEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['UpdateEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['UpdateEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


# noinspection PyUnusedLocal
class CollisionEvent(Event):
    _handlers = list()

    def __init__(self, scene: _Scene, eventobj, collidedobj, canvas: _tk.Canvas):
        self.eventObject = eventobj
        self.collidedObj = collidedobj
        self.canvas: _tk.Canvas = canvas
        self.scene: _Scene = scene

        super(Event, self).__init__()
        for handler in self._handlers:
            if handler.__self__ is not None:
                if handler.__self__ == eventobj:
                    if handler(self) == "cancel":
                        self.cancel = True
            else:
                if handler(self) == "cancel":
                    self.cancel = True

    @classmethod
    def bind(cls, func: _t.Callable[['CollisionEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['CollisionEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


# noinspection PyUnusedLocal
class PauseEvent(Event):
    """
    For pausing / unpausing the game.
    """
    _handlers = list()

    def __init__(self, scene, canvas, temp, pause: bool):
        """
        For pausing / unpausing the game.

        :param scene:
        :param canvas:
        :param temp:
        :param pause:
        """

        self.canvas: _tk.Canvas = canvas
        self.pause = pause
        self.temp = temp

        super(PauseEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['PauseEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['PauseEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class EffectApplyEvent(Event):
    """
    For pausing / unpausing the game.
    """
    _handlers = list()

    def __init__(self, scene, canvas, appliedeffect):
        """
        For pausing / unpausing the game.

        :param scene:
        :param canvas:
        :param temp:
        :param pause:
        """

        self.canvas: _tk.Canvas = canvas
        self.appliedEffect = appliedeffect
        self.sprite = self.appliedEffect.sprite

        super(EffectApplyEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['EffectApplyEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['EffectApplyEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class XInputEvent(UpdatableEvent):
    _handlers = list()
    xboxController = _XboxController()
    _A = None
    _B = None
    _X = None
    _Y = None
    _LB = None
    _RB = None
    _LTR = None
    _RTR = None
    _LTH = None
    _RTH = None
    _LJOY = None
    _RJOY = None
    _START = None
    _SELEC = None

    # noinspection PyMissingConstructor
    def __init__(self, scene):
        """
        Triggers to update xinput values, and call event handlers on parent class

        :param scene:
        """

        self.eventype = "button"
        if self._A != XInputEvent.xboxController.A:
            self.event = "A"
            self.value = XInputEvent.xboxController.A
            super(UpdatableEvent, self).__init__(scene)
        if self._B != XInputEvent.xboxController.B:
            self.event = "B"
            self.value = XInputEvent.xboxController.B
            super(UpdatableEvent, self).__init__(scene)
        if self._X != XInputEvent.xboxController.X:
            self.event = "X"
            self.value = XInputEvent.xboxController.X
            super(UpdatableEvent, self).__init__(scene)
        if self._Y != XInputEvent.xboxController.Y:
            self.event = "Y"
            self.value = XInputEvent.xboxController.Y
            super(UpdatableEvent, self).__init__(scene)
        if self._LB != XInputEvent.xboxController.LeftBumper:
            self.event = "LBUMPER"
            self.value = XInputEvent.xboxController.LeftBumper
            super(UpdatableEvent, self).__init__(scene)
        if self._RB != XInputEvent.xboxController.RightBumper:
            self.event = "RBUMPER"
            self.value = XInputEvent.xboxController.RightBumper
            super(UpdatableEvent, self).__init__(scene)
        if self._LTH != XInputEvent.xboxController.LeftThumb:
            self.event = "LTHUMB"
            self.value = XInputEvent.xboxController.LeftThumb
            super(UpdatableEvent, self).__init__(scene)
        if self._RTH != XInputEvent.xboxController.RightThumb:
            self.event = "RTHUMB"
            self.value = XInputEvent.xboxController.RightThumb
            super(UpdatableEvent, self).__init__(scene)

        self.eventype = "trigger"
        if self._LTR != XInputEvent.xboxController.LeftTrigger:
            self.event = "LTRIGGER"
            self.value = XInputEvent.xboxController.LeftTrigger
            super(UpdatableEvent, self).__init__(scene)
        if self._RTR != XInputEvent.xboxController.RightTrigger:
            self.event = "RTRIGGER"
            self.value = XInputEvent.xboxController.RightTrigger
            super(UpdatableEvent, self).__init__(scene)

        self.eventype = "joystick"
        x = XInputEvent.xboxController
        if self._LJOY != (x.LeftJoystickX, x.LeftJoystickY):
            self.event = "LJOYSTICK"
            self.value = (x.LeftJoystickX, x.LeftJoystickY)
            super(UpdatableEvent, self).__init__(scene)
        if self._RJOY != (x.RightJoystickX, x.RightJoystickY):
            self.event = "RJOYSTICK"
            self.value = (x.RightJoystickX, x.RightJoystickY)
            super(UpdatableEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: _t.Callable[['XInputEvent'], _t.Any]):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: _t.Callable[['XInputEvent'], _t.Any]):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func
