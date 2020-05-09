import math
import typing
import typing as _t
import tkinter

import overload

from deprecated import deprecated

import qbubbles.base as _base
import qbubbles.effects as _effects
import qbubbles.events as _evts
import qbubbles.registry as _reg
import qbubbles.sprite.abilities as _abilities
import qbubbles.gameIO as _gameIO

# noinspection PyShadowingBuiltins
_KT = typing.TypeVar('_KT')
# noinspection PyShadowingBuiltins
_VT = typing.TypeVar('_VT')
# noinspection PyShadowingBuiltins
_T = typing.TypeVar('_T')
# noinspection PyShadowingBuiltins
_S = typing.TypeVar('_S')


# noinspection PyShadowingBuiltins
class SpriteData(object):
    def __init__(self, default):
        if type(default) == dict:
            self._type: typing.Type[dict] = dict
        else:
            raise TypeError(f"The default value is not a dict or list")
        self.default = default.copy()
        self._value = default.copy()

    def __iter__(self):
        if self._type == list:
            return self._value
        else:
            return []

    def __getitem__(self, item):
        return self._value[item]

    def __setitem__(self, item, value):
        self._value[item] = value

    def __delitem__(self, item):
        del self._value[item]

    def __setslice__(self, i, j, sequence: typing.Sequence):
        if type(self._value) == list:
            self._value: list
            self._value[i:j] = sequence

    def __getslice__(self, i, j):
        if type(self._value) == list:
            self._value: list
            return self._value[i:j]

    def __delslice__(self, i, j):
        if type(self._value) == list:
            self._value: list
            del self._value[i:j]

    @overload.overload
    def get(self, k: _KT) -> _VT:
        if self._type == dict:
            self._value: dict
            return self._value.get(k)

    @get.add
    def get(self, k: _KT, default: typing.Union[_VT, _T] = None) -> typing.Union[_VT, _T]:
        if self._type == dict:
            self._value: dict
            return self._value.get(k, default)

    @overload.overload
    def pop(self, k: _KT, default: typing.Union[_VT, _T] = None) -> typing.Union[_VT, _T]:
        if self._type == dict:
            self._value: dict
            return self._value.pop(k, default)

    def keys(self) -> typing.KeysView:
        if self._type == dict:
            self._value: dict
            return self._value.keys()

    def values(self) -> typing.ValuesView:
        if self._type == dict:
            self._value: dict
            return self._value.values()

    def items(self) -> typing.ItemsView:
        if self._type == dict:
            self._value: dict
            return self._value.items()

    @overload.overload
    def update(self, __m: typing.Mapping[_KT, _VT], **kwargs) -> None:
        if self._type == dict:
            self._value: dict
            return self._value.update(__m, **kwargs)

    @update.add
    def update(self, __m: typing.Iterable[typing.Tuple[_KT, _VT]], **kwargs) -> None:
        if self._type == dict:
            self._value: dict
            return self._value.update(__m, **kwargs)

    @update.add
    def update(self, **kwargs) -> None:
        if self._type == dict:
            self._value: dict
            return self._value.update(**kwargs)

    @overload.overload
    def fromkeys(self, seq: typing.Iterable[_T]) -> dict:
        if self._type == dict:
            self._value: dict
            return self._value.fromkeys(seq)

    @fromkeys.add
    def fromkeys(self, seq: typing.Iterable[_T], value: _T) -> dict:
        if self._type == dict:
            self._value: dict
            return self._value.fromkeys(seq, value)

    def popitem(self) -> typing.Tuple[_KT, _VT]:
        if self._type == dict:
            self._value: dict
            return self._value.popitem()

    def setdefault(self, k: _KT, default: _VT) -> int:
        if self._type == dict:
            self._value: dict
            return self._value.setdefault(k, default)

    @pop.add
    def pop(self, k: typing.Union[_KT, int]) -> typing.Union[_VT, _T]:
        if self._type == dict:
            self._value: dict
            return self._value.pop(k)
        if self._type == list:
            self._value: list
            return self._value.pop(k)

    def clear(self) -> None:
        if self._type == dict:
            self._value: dict
            return self._value.clear()
        if self._type == list:
            self._value: list
            return self._value.clear()

    def copy(self) -> typing.Union[list, dict]:
        if self._type == dict:
            self._value: dict
            return self._value.copy()
        if self._type == list:
            self._value: list
            return self._value.copy()

    def remove(self, o: _T) -> None:
        if self._type == list:
            self._value: list
            return self._value.remove(o)

    def extend(self, iterable: typing.Iterable[_T]) -> None:
        if self._type == list:
            self._value: list
            return self._value.extend(iterable)
        self._value: list

    def count(self, object: _T) -> int:
        if self._type == list:
            self._value: list
            return self._value.count(object)

    def index(self, object: _T, start: int = None, stop: int = None) -> int:
        if self._type == list:
            self._value: list
            return self._value.index(object, start, stop)

    def reverse(self) -> None:
        if self._type == list:
            self._value: list
            return self._value.reverse()

    def insert(self, index: int, object: _T) -> None:
        if self._type == list:
            self._value: list
            return self._value.insert(index, object)

    def sort(self, *, key: typing.Callable[[_T], typing.Any] = None, reverse: bool) -> None:
        if self._type == list:
            self._value: list
            return self._value.sort(key=key, reverse=reverse)

    # noinspection PyShadowingBuiltins
    def append(self, object: _T):
        if self._type == list:
            self._value: list
            self._value.append(object)


# noinspection PyUnusedLocal,PyStatementEffect,PyTypeChecker
class Sprite:
    requires = ("sprites", "config", "canvas", "stats", "log", "ship", "bubbles")

    def __init__(self, **kw):
        name = "EmptySprite"

        self._kw = kw

        self.abilities: typing.List[_abilities.Ability] = []

        # Axis
        self.axis = (_base.HORIZONTAL, _base.VERTICAL)

        # Has- variables
        self.hasSkin = True
        self.hasMovetag = True

        # Type
        self.type = _base.TYPE_NEUTRAL
        self.shoots = _base.FALSE
        self.form = _base.FORM_CIRCLE

        # Info
        self.baseRadius = int()
        self.height = int()
        self.width = int()

        # Direction movement
        self.returnBorder = True
        self.direction = _base.LEFT

        # HP System
        self.health = 1
        self.maxHealth = 1
        self.regenValue = 1
        self.attackValue = 0
        self.defenceValue = 1
        self.regenMultiplier = 0
        self.attackMultiplier = 1
        self.defenceMultiplier = 1

        # Switches
        self.allowCollision = True

        # x and y, move and speed variables
        self.xMove = -3
        self.xSpeed = 3
        self.yMove = 0
        self.ySpeed = 0

        # self.collisionWith = (SHIP, ANY_BUBBLE)
        self.collisionWith: typing.Optional[typing.List] = None

        self.lifeCost = 1

        self.id = int()

        self._spriteName: str = None

        self.coordsLen = 2

        self._spriteData = {}
        self._objectData = {"Position": (None, None)}
        self.dead = False

    def reload(self, odata: _t.Union[_t.Dict, SpriteData]):
        pass

    def __repr__(self):
        a = "{"+(", ".join(f"{repr(key)}={repr(value)}" for key, value in dict(self._objectData).items()))+"}"
        return f"Sprite({repr(self.get_sname())}, data="+a+")"

    def delete(self) -> typing.NoReturn:
        canvas: tkinter.Canvas = _reg.Registry.get_scene("Game").canvas
        canvas.delete(self.id)

    def get_spritedata(self) -> dict:
        return self._spriteData

    def create(self, x, y):
        _reg.Registry.get_scene("Game").gameObjects.append(self)

    def get_sname(self):
        return self._spriteName

    @staticmethod
    def _c_create_image(x, y, image, anchor="nw"):
        return _reg.Registry.get_scene("Game").canvas.create_image(x, y, image=image, anchor=anchor)

    def move(self, x, y):
        _reg.Registry.get_scene("Game").canvas.move(self.id, x, y)
        self._objectData["Position"] = self.get_coords()

    def teleport(self, x, y):
        _reg.Registry.get_scene("Game").canvas.coords(self.id, x, y)
        self._objectData["Position"] = self.get_coords()

    def get_coords(self):
        return _reg.Registry.get_scene("Game").canvas.coords(self.id)

    def attack(self, other: object):
        if not issubclass(type(other), Sprite):
            raise TypeError("argument 'other' must be a Sprite-object")
        other: Sprite
        # print(f"{self.__class__.__name__} is attacking {other.__class__.__name__}")
        if other.defenceMultiplier != 0:
            other.damage(self.attackMultiplier / other.defenceMultiplier)
        else:
            other.instant_death()

    def damage(self, value: float, src = None):
        scene = _reg.Registry.get_scene("Game")
        if not _evts.SpriteDamageEvent(scene, self).cancel:
            self.health -= value / self.defenceValue
            if self.health <= 0:
                self.dead = True

    def distance(self, to):
        canvas = _reg.Registry.get_scene("Game").canvas
        try:
            # try:
            x1, y1 = self.get_coords()
            # except ValueError:
            #     self.instant_death()
            # try:
            x2, y2 = to.get_coords()
            # except ValueError:
            #     to.instant_death()
            # print(f"POINT_1: {x1, y1}")
            # print(f"POINT_2: {x2, y2}")
            # noinspection PyUnboundLocalVariable
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        except ValueError:
            return math.inf
        except UnboundLocalError:
            return math.inf

    def instant_death(self):
        self.health = 0
        self.dead = True

    def on_collision(self, evt: _evts.CollisionEvent):
        pass

    def on_keypress(self, evt: _evts.KeyPressEvent):
        pass

    def on_keyrelease(self, evt: _evts.KeyReleaseEvent):
        pass

    def on_xboxcontrol(self, evt: _evts.XInputEvent):
        pass

    def on_mouseenter(self, evt: _evts.MouseEnterEvent):
        pass

    def on_mouseleave(self, evt: _evts.MouseLeaveEvent):
        pass

    def on_update(self, evt: _evts.UpdateEvent):
        pass

    def get_objectdata(self):
        return dict(self._objectData).copy()


class Player(Sprite):
    def __init__(self):
        """
        Player object, one of the most important sprites in the game.
        """
        
        # Super call to the Sprite constructor.
        super(Player, self).__init__()

        # Effects, and applied effects.
        self.appliedEffects: typing.List[_effects.AppliedEffect] = []
        self.appliedEffectTypes: typing.List[typing.Type[_effects.AppliedEffect]] = []

        # Pressed keys.
        self.keysPressed = ""
        
        # Defining sprite-attributes.
        self._spriteName = "qbubbles:player"
        self._spriteData = {
            "objects": [
                {
                    "Abilities": {
                        #  **dict(((key, value) for key, value in _reg.Registry.get_abilities()))
                    },
                    "Attributes": {
                        "highScore": 10,
                        "maxHealth": 10,
                        "health": 10,
                        "speed": 80,
                        "level": 1,
                        "score": 0,
                        "coins": 0
                    },
                    "Modifiers": {
                        "scoreMultiplier": 1,
                        "regenMultiplier": 1,
                        "attackMultiplier": 1,
                        "defenseMultiplier": 1
                    },
                    "Switches": {
                        "allowCollision": True,
                        "isInvulnerable": False
                    },
                    "Effects": [],
                    "Position": [10, 10],
                    "Rotation": 0
                }
            ]
        }
        
        # Defining default object-data.
        self._objectData = dict(
            {
                "Abilities": {
                    # **dict(((key, value) for key, value in _reg.Registry.get_abilities()))
                },
                "Attributes": {
                    "highScore": 10,
                    "maxHealth": 10,
                    "health": 10,
                    "speed": 80,
                    "level": 1,
                    "score": 0,
                    "coins": 0
                },
                "Modifiers": {
                    "scoreMultiplier": 1,
                    "regenMultiplier": 1,
                    "attackMultiplier": 1,
                    "defenseMultiplier": 1
                },
                "Switches": {
                    "allowCollision": True,
                    "isInvulnerable": False
                },
                "Effects": [],
                "Position": [10, 10],
                "Rotation": 0
            }
        )

        # Dynamic attributes.
        self.coins = 0
        self.score = 0
        self.level = 1
        self.speed = 80
        self.health = 10
        self.rotation = 0
        self.highScore = 10
        self.maxHealth = 10
        self._exp = 0

        # Static base attributes.
        self.baseRadius = 12.5
        self.baseSpeed = 0
        self.baseHealth = 10

        # Multiplier attributes
        self.regenValue = 1
        self.attackValue = 1
        self.defenceValue = 1
        self.scoreMultiplier = 1
        self.regenMultiplier = 1
        self.attackMultiplier = 1
        self.defenceMultiplier = 1

        # Switches
        self.allowCollision = True
        self.isInvulnerable = False
        
        # Defining the ‘Events Activated’ switch.
        self.events_activated = False

        # Motion directions.
        self.up = False
        self.down = False
        self.right = False
        self.left = False

        # Pause
        self._pause = False

    def reload(self, odata: _t.Union[_t.Dict, SpriteData]):
        """
        Reloads the player using the given object data.
        
        **Note:** Use only for reloading the game it self, like in a custom gamemap.
        
        :param odata: The object data to use for reloading the player.
        :return: 
        """
        
        self.teleport(*odata["Position"])
        self.rotate(odata["Rotation"])

        for effectdata in odata["Effects"]:
            effect: _effects.BaseEffect = _reg.Registry.get_effect(effectdata["id"])
            
            # Start the effect using saved effect data. Using the object-data (odata) given from the arguments.
            if effectdata["duration"] > 0.0:
                self.start_effect(
                    effect, _reg.Registry.get_scene("Game"), effectdata["duration"], effectdata["strength"],
                    **dict(effectdata["extradata"]))

        attributes = odata["Attributes"]
        self.coins = attributes["coins"]
        self.level = attributes["level"]
        self.speed = attributes["speed"]
        self.score = attributes["score"]
        self.health = attributes["health"]
        self.maxHealth = attributes["maxHealth"]
        self.highScore = attributes["highScore"]

        modifiers = odata["Modifiers"]
        self.scoreMultiplier = modifiers["scoreMultiplier"]
        self.regenMultiplier = modifiers["regenMultiplier"]
        self.attackMultiplier = modifiers["attackMultiplier"]
        self.defenceMultiplier = modifiers["defenseMultiplier"]

        switches = odata["Switches"]
        self.allowCollision = switches["allowCollision"]
        self.isInvulnerable = switches["isInvulnerable"]

        _gameIO.Logging.debug("Player", f"Speed on reload is {self.speed}")

        # effectdata[]
        # self.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation.rotation

    def add_score(self, value):
        self.score += value * self.scoreMultiplier

    def remove_score(self, value):
        result = self.score - value * self.scoreMultiplier
        if result < 0:
            result = 0
        self.score = result

    def set_score(self, value):
        if value < 0:
            raise ValueError("Score value must be greater than or equal to zero")

        self.score = value

    def get_score(self):
        return self.score

    def add_health(self, value):
        self.regen(value)

    def set_health(self, value):
        self.health = value
        self.health_check()

    def get_health(self):
        return self.health

    def health_check(self):
        if self.health < 0:
            self.dead = True

    @overload.overload
    def regen(self, value=None):
        if value is None:
            return self.regen()
        self.health += value * self.regenMultiplier

    @regen.add
    def regen(self):
        self.health += self.regenValue * self.regenMultiplier

    # def damage(self, value: float):

    def add_effect(self, appliedeffect: _effects.AppliedEffect):
        """
        Adds an effect, must be an AppliedEffect()-instance. For starting a new effect, use start_effect() instead.
        
        :param appliedeffect: 
        :return: 
        """
        
        self.appliedEffects.append(appliedeffect)
        self.appliedEffectTypes.append(type(appliedeffect))

    def activate_events(self):
        """
        Activates the player's events.
        
        :return: 
        """
        
        if self.events_activated:
            _gameIO.Logging.info("Player", "Events already activated")
            return
        _gameIO.Logging.info("Player", "Activating events...")
        self.events_activated = True
        _evts.PauseEvent.bind(self.on_pause)
        _evts.KeyPressEvent.bind(self.on_key_press)
        _evts.KeyReleaseEvent.bind(self.on_key_release)
        _evts.UpdateEvent.bind(self.on_update)
        _evts.CollisionEvent.bind(self.on_collision)
        _evts.SavedataReadedEvent.bind(self.on_savedata_readed)

    def deactivate_events(self):
        """
        Deactivates the player's events.

        :return:
        """

        if not self.events_activated:
            _gameIO.Logging.info("Player", "Events already deactivated")
            return
        _gameIO.Logging.info("Player", "Deactivating events...")
        self.events_activated = False
        _evts.PauseEvent.unbind(self.on_pause)
        _evts.KeyPressEvent.unbind(self.on_key_press)
        _evts.KeyReleaseEvent.unbind(self.on_key_release)
        _evts.UpdateEvent.unbind(self.on_update)
        _evts.CollisionEvent.unbind(self.on_collision)
        _evts.SavedataReadedEvent.unbind(self.on_savedata_readed)

    def on_pause(self, evt: _evts.PauseEvent):
        self._pause = evt.pause

    def on_collision(self, evt: _evts.CollisionEvent):
        """
        Collision event handler.

        :param evt:
        :return:
        """

        if evt.collidedObj.get_sname() != "qbubbles:bubble":
            _gameIO.Logging.debug("Player", f"Double Collision Check: {evt.eventObject}")
            evt.collidedObj.attack(evt.eventObject)  # evt.collidedObj.attackMultiplier / self.defenseMultiplier)
            evt.eventObject.attack(evt.collidedObj)
            if isinstance(evt.collidedObj, Player):
                if evt.collidedObj == self:
                    evt.collidedObj.score += int(evt.eventObject.baseRadius * (evt.eventObject.baseSpeed / 8) / 8) * evt.eventObject.scoreMultiplier

        # Todo: Remove when seems to be unnecessary.
        elif evt.eventObject.get_sname() != "qbubbles:bubble":
            _gameIO.Logging.debug("Player", f"Double Collision Check: {evt.collidedObj}")
            evt.collidedObj.attack(evt.eventObject)  # evt.collidedObj.attackMultiplier / self.defenseMultiplier)
            evt.eventObject.attack(evt.collidedObj)
            if evt.eventObject.get_sname() == "qbubbles:player":
                evt.eventObject.score += int(evt.collidedObj.baseRadius * (evt.collidedObj.baseSpeed / 8) / 8) * evt.collidedObj.scoreMultiplier

    def add_experience(self, experience):
        """
        WIP: Work in Progress.
        Used for adding experience to the player.

        :param experience:
        :return:
        """

        _evts.ExperienceEvent(self, experience)

    def on_savedata_readed(self, data):
        """
        Savedata read event handler.

        :param data:
        :return:
        """

        self.score = data["Player"]["score"]

        for effect in data["Player"]["Effects"]:
            effect_class: _effects.BaseEffect = _reg.Registry.get_effect(effect["id"])
            time_length: float = effect["timeRemaining"]
            if time_length > 0.0:
                strength: float = effect["strength"]
                self.start_effect(effect_class, _reg.Registry.get_scene("Game"), time_length, strength)

    def remove_effect(self, appliedeffect: _effects.AppliedEffect):
        """
        Removes an applied-effect from the player's effect list.

        :param appliedeffect: The applied-effect to remove.
        :returns: The index where the applied-effect was removed.
        """

        index = self.appliedEffects.index(appliedeffect)
        del self.appliedEffectTypes[index]
        del self.appliedEffects[index]
        return index

    def start_effect(self, effect_class: _effects.BaseEffect, scene, duration: float, strength: _t.Union[float, int], **extradata) -> _effects.AppliedEffect:
        """
        Starts an effect, it converts the BaseEffect() subclass into an AppliedEffect() instance. And starts the effect.

        :param effect_class: The base-class of the effect.
        :param scene: The game-scene.
        :param duration: The duration of the effect.
        :param strength: The strength of the effect
        :param extradata: The extra data to add to the effect.
        :raises AssertionError: If the effect-class is a type.
        :returns: The applied-effect
        """

        assert not isinstance(effect_class, type)

        appliedeffect = _effects.AppliedEffect(effect_class, scene, duration, strength, self, **extradata)
        self.appliedEffects.append(appliedeffect)

        return appliedeffect

    def get_objectdata(self):
        """
        Method to get the object data of the player, in a dict() format.

        :returns: A dict containing the object data.
        """

        odata = dict(self._objectData.copy())
        odata["Position"] = self.get_coords()
        odata["Rotation"] = self.rotation

        attributes = dict()
        attributes["highScore"] = self.highScore
        attributes["health"] = self.health
        attributes["speed"] = self.speed
        attributes["score"] = self.score
        attributes["level"] = self.level  # TODO: Use levels for Player()-objects
        attributes["coins"] = self.coins
        odata["Attributes"] = attributes

        modifiers = dict()
        modifiers["scoreMultiplier"] = self.scoreMultiplier
        modifiers["regenMultiplier"] = self.regenMultiplier
        modifiers["attackMultiplier"] = self.attackMultiplier
        modifiers["defenseMultiplier"] = self.defenceMultiplier
        odata["Modifiers"] = modifiers

        switches = dict()
        switches["allowCollision"] = self.allowCollision
        switches["isInvulnerable"] = self.isInvulnerable
        odata["Switches"] = switches

        # odata["high_score"] = self.highScore  # TODO: Use high score for Player()-objects
        # self.appliedEffects:
        odata["Effects"] = [effect.get_data() for effect in self.appliedEffects]
        odata["Abilities"] = [ability.get_data() for ability in self.abilities]
        return odata

    def move(self, x: _t.Union[int, float] = 0, y: _t.Union[int, float] = 0):
        """
        Moves the player relative to the current position.

        :param x:
        :param y:
        :return:
        """

        _reg.Registry.get_scene("Game").canvas.move(self.id, x, y)

    @deprecated("Use move() instead")
    def move_joy(self, x=0, y=0):
        """
        Move the player relative to the current position, using joystick.

        :param x:
        :param y:
        :return:
        """

        _reg.Registry.get_scene("Game").canvas.move(self.id, x, y)

    def on_effect_stop(self, appliedeffect: _effects.AppliedEffect):
        self.remove_effect(appliedeffect)

    def on_update(self, evt: _evts.UpdateEvent):
        # if self.up:
        #     y -= self.baseSpeed * evt.dt
        # if self.left:
        #     x -= self.baseSpeed * evt.dt
        # if self.down:
        #     y += self.baseSpeed * evt.dt
        # if self.right:
        #     x += self.baseSpeed * evt.dt

        if not self._pause:
            pixels = 0

            if self.up:
                pixels = self.speed
            if self.down:
                pixels = -self.speed
            if self.left:
                self.rotate(+(evt.dt * 160))
            if self.right:
                self.rotate(-(evt.dt * 160))

            import math

            d = -(evt.dt * pixels)  # distance covered this tick.
            angle_radians = math.radians(self.rotation)
            dx = -math.cos(angle_radians)
            dy = math.sin(angle_radians)

            dx, dy = dx * d, dy * d

            x, y = dx, dy

            # print(self.up, self.left, self.down, self.right)
            # print(x, y)
            self.move(x, y)

    def create(self, x, y):
        image = _reg.Registry.get_texture("sprite", "player", rotation=0)
        self.id = self._c_create_image(x, y, image, anchor="center")
        # self.id = Registry.get_scene("Game").canvas.create_image(x, y, image=Registry.get_texture("sprite", "player",
        #                                                                                           rotation=0))
        self.baseSpeed = 80
        self.speed = 80
        self.speed = self.baseSpeed

    def _update_rot_tex(self):
        """
        Updates the rotation texture

        :return:
        """
        image = _reg.Registry.get_texture(
            "sprite", "player", rotation=int(self.rotation - (self.rotation % 1)))
        c = _reg.Registry.get_scene("Game").canvas
        c.itemconfig(self.id, image=image)

    def rotate(self, r_rot):
        """
        Rotates the player

        :param r_rot: Rotation in degrees
        :return:
        """

        self.rotation += r_rot
        self.rotation = self.rotation % 360
        self._update_rot_tex()

    def on_key_press(self, evt: _evts.KeyPressEvent):
        """
        Key-press event handler

        :param evt:
        :return:
        """

        # print(f"PRESS1: {evt.char} | {evt.keySym}")
        if (evt.char.lower() == "w") and not self.up:
            self.up = True
        elif (evt.keySym.lower() == "up") and not self.up:
            self.up = True
        elif (evt.char.lower() == "a") and not self.left:
            self.left = True
        elif (evt.keySym.lower() == "left") and not self.left:
            self.left = True
        elif (evt.char.lower() == "s") and not self.down:
            self.down = True
        elif (evt.keySym.lower() == "down") and not self.down:
            self.down = True
        elif (evt.char.lower() == "d") and not self.right:
            self.right = True
        elif (evt.keySym.lower() == "right") and not self.right:
            self.right = True
        # TODO: Implement teleport ability for player, using key-events, such as using LShift
        # print(self.up, self.left, self.down, self.right)

    def on_key_release(self, evt: _evts.KeyReleaseEvent):
        """
        Key-release event handler

        :param evt:
        :return:
        """

        list(self.keysPressed)
        # print(f"RELEASE1: {evt.char}")
        if (evt.char.lower() == "w") and self.up:
            self.up = False
        elif (evt.keySym.lower() == "up") and self.up:
            self.up = False
        elif (evt.char.lower() == "a") and self.left:
            self.left = False
        elif (evt.keySym.lower() == "left") and self.left:
            self.left = False
        elif (evt.char.lower() == "s") and self.down:
            self.down = False
        elif (evt.keySym.lower() == "down") and self.down:
            self.down = False
        elif (evt.char.lower() == "d") and self.right:
            self.right = False
        elif (evt.keySym.lower() == "right") and self.right:
            self.right = False
        # TODO: Implement teleport ability for player, using key-events

    def get_ability(self, uname):
        """
        Get ability instance from uname

        :param uname:
        :return:
        """

        if uname in self.get_spritedata()["Abilities"].keys():
            return self.get_spritedata()["Abilities"][uname]
        return None


class TeleportCrosshair(Sprite):
    def __init__(self):
        """
        Deprecated, will use ability and key-events instead.
        TODO: Remove this, and use ability and key-events instead.
        """

        super(TeleportCrosshair, self).__init__()

        self.abilities.append(_abilities.GhostAbility(self))
        self.abilities.append(_abilities.InvulnerableAbility(self))

    def create(self, x, y):
        super(x, y)

    def on_key_release(self, evt: _evts.KeyReleaseEvent):
        if evt.keySym.lower() == "return":
            _reg.Registry.get_mode("teleport").execute(
                "done", x=self.get_coords()[0], y=self.get_coords()[1])


# noinspection PyAttributeOutsideInit
class Ammo(Sprite):
    requires = tuple(list(Sprite.requires) + ["ship", "ammo"])

    def __init__(self, **kw):
        """
        WORK IN PROGRESS
        TODO: Use Ammo(Sprite) class for shooting, and improve performance of the Ammo Sprite.

        :param kw:
        """
        super().__init__(**kw)
        self._kw = kw
        self.form = _base.FORM_LINE
        self.return_border = _base.FALSE
        self.direction = _base.LEFT
        self.axis = [_base.VERTICAL]
        self.x_speed = 60
        self.x_move = 60
        self.y_speed = 0
        self.y_move = 0
        self.height = 1
        self.width = 5

    def on_collide_bubble(self, index):
        """
        FIXME: Rename method to allow compatibility with base sprite

        :param index:
        :return:
        """

        from qbubbles.components import StoppableThread
        from qbubbles.bubble import del_bubble
        from qbubbles.extras import replace_list, distance
        from qbubbles.ammo import del_ammo

        log = self._kw["log"]
        ammo = self._kw["ammo"]
        root = self._kw["root"]
        texts = self._kw["texts"]
        stats = self._kw["stats"]
        canvas = self._kw["canvas"]
        panels = self._kw["panels"]
        bubble = self._kw["bubbles"]
        commands = self._kw["commands"]
        coll_func = self._kw["Coll"].coll_func
        ammo_index = self.id
        backgrounds = self._kw["back"]

        index_bub = index
        try:
            if distance(canvas, log, ammo["ammo-id"][ammo_index], bubble["bub-id"][index_bub][0]) < (
                    1 + bubble["bub-radius"][index_bub]):
                if bubble["bub-hardness"][index_bub] == 1:
                    try:
                        self.thread4 = StoppableThread(
                            None,
                            lambda: coll_func(index_bub, canvas, commands, root, log,
                                              stats,
                                              (bubble["bub-radius"][index_bub] +
                                               bubble["bub-speed"][index_bub]),
                                              bubble["bub-action"][index_bub], bubble,
                                              backgrounds,
                                              texts, panels, False),
                            __name__ + ".CollisionFunction").start()
                    except IndexError:
                        pass
                    del_bubble(index_bub, bubble, canvas)
                    replace_list(ammo["ammo-damage"], ammo_index, ammo["ammo-damage"][ammo_index] + 1)
                    if ammo["ammo-damage"][ammo_index] > 4:
                        del_ammo(canvas, ammo_index, ammo)
                    # # TODO: Replace with something like pygame's mixer'
                    # Thread(None, PlaySound("versions/"+self.launcher_config["versionDir"]+"/assets/bubpop.wav", 1)).start()
                elif bubble["bub-hardness"][index_bub] > 1:
                    replace_list(bubble["bub-hardness"], index_bub, bubble["bub-hardness"][index_bub] - 1)
                    replace_list(ammo["ammo-damage"], ammo_index, ammo["ammo-damage"][ammo_index] + 1)
                    if ammo["ammo-damage"][ammo_index] > 4:
                        del_ammo(canvas, ammo_index, ammo)
                root.update()
        except TypeError:
            pass
        except IndexError:
            pass

    def create(self, x, y):
        id_ = self._kw["ship"]["id"]
        x, y = self._kw["canvas"].coords(id_)

        self.id = self._kw["canvas"].create_line(x + 7, y, x + 12, y, fill="gold")
        self._kw["ammo"]["ammo-id"][self.id] = self.id
        self._kw["ammo"]["ammo-speed"][self.id] = 5
        self._kw["ammo"]["ammo-damage"][self.id] = 0
        super().create(x, y)


# noinspection PyRedundantParentheses
class BaseBarier(Sprite):
    def __init__(self, **kw):
        """
        WORK IN PROGRESS

        :param kw:
        """
        from random import randint, choice
        self._kw = kw
        super().__init__(**kw)
        self.direction = choice([_base.UP, _base.DOWN])
        self.has_skin = True
        self.has_movetag = True
        self.axis = [_base.VERTICAL]
        self.type = _base.TYPE_DANGEROUS
        self.form = _base.FORM_RECT
        self.direction = _base.UP
        self.__speed = randint(80, 104)
        self.x_speed = 0
        self.y_speed = self.__speed
        self.x_move = 0
        self.y_move = self.__speed
        self.height = 100
        self.width = 10
        self.collision_with = [_base.SHIP]

    def create(self, x, y):
        """
        TODO: Use Images instead (Pillow / Tkinter.PhotoImage).

        :param x:
        :param y:
        :return:
        """

        self.id = self._kw["canvas"].create_rectangle(x, y + 72, x + 10, y + 222, fill=_base.RED, outline=_base.RED)
        # print(self.parent.canvas.coords(self.id))
        super().create(x, 72 + y)
