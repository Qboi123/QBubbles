import string
import typing as _t
from tkinter import Canvas
from typing import Optional, List, NoReturn

import qbubbles.effects
from qbubbles import effects
from qbubbles.events import UpdateEvent, CleanUpEvent, CollisionEvent, PauseEvent
from qbubbles.gameIO import Logging

from qbubbles.sprites import Sprite, SpriteData
from qbubbles.exceptions import UnlocalizedNameError
from qbubbles.registry import Registry
from qbubbles.sprites import Player


class Bubble(object):
    def __init__(self):
        self.priority = 0

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 5
        self.maxSpeed: int = 10
        self.hardness: int = 1
        self.damage: int = 1

        # Multipliers
        self.scoreMultiplier: int = 0
        self.attackMultiplier: int = 0
        self.defenseMultiplier: int = 1

        self._uName: Optional[str] = None

    def set_uname(self, name) -> NoReturn:
        for symbol in name:
            if symbol not in string.ascii_letters + string.digits + "_" + ":":
                raise UnlocalizedNameError(f"Invalid character '{symbol}' for unlocalized name '{name}'")
        if name[0] not in string.ascii_letters:
            raise UnlocalizedNameError(f"Invalid start character '{name[0]}' for unlocalized name '{name}'")
        if name[-1] not in string.ascii_letters + string.digits:
            raise UnlocalizedNameError(f"Invalid start character '{name[-1]}' for unlocalized name '{name}'")

        self._uName = name

    def get_uname(self) -> str:
        return self._uName

    def get_uname_registry(self) -> List[str]:
        return Registry.get_id_bubble(self)

    def __repr__(self) -> str:
        return f"Bubble(<{self.get_uname()}>)"

    def on_collision(self, bubbleobject: 'BubbleObject', other: 'Sprite'):
        pass


class BubbleObject(Sprite):
    def __init__(self, baseobject: Bubble = None, maxhealth=5, basehealth=None, radius=5, speed=5, health=5,
                 scoremp=None, attackmp=None, defensemp=None):
        """
        Bubble object, used to create bubble on the game canvas / window.

        Attributes:
          appliedEffects:
            Description: Dictionary of applied-effects, key is the instance, value is the class. \n
            Type: ``Dict[AppliedEffect, Type[AppliedEffect]]``
          baseSpeed:
            Description: Base speed of the bubble, must not be changed after creation. \n
            Type: ``int``
          baseObject:
            Description: Base object of the bubble, must not be changed after creation. \n
            Type: ``Bubble`` (Or a subclass of it)
          baseRadius:
            Description: Base radius of the bubble, must not be changed after creation. \n
            Type: ``int``
          baseHealth:
            Description: The starting health of the bubble, must not be changed after creation. \n
            Type: ``float`` or ``int``.

        :param baseobject:
        :param maxhealth:
        :param basehealth:
        """

        super(BubbleObject, self).__init__()

        # Static attributes
        self._pause = False
        self._spriteName = "qbubbles:bubble"
        self._spriteData = {"objects": [], "speed_multiplier": 0.5, "id": self.get_sname()}
# Base attributes
        self.baseSpeed: Optional[int] = None
        self.baseObject: Bubble = baseobject
        self.baseRadius: Optional[int] = None
        self.baseHealth = maxhealth if basehealth is None else basehealth

        # Switches
        self.allowCollision = True
        self.isInvulnerable = False

        # Dynamic attributes
        self.appliedEffects = {}
        self.maxHealth = maxhealth
        self.radius: Optional[int] = None
        self.speed: Optional[int] = None

        # Modifier attributes
        self.scoreMultiplier: float = self.baseObject.scoreMultiplier if self.baseObject is not None else None

        # Bubble displaying attributes
        self.imageList = {}
        self.id: Optional[int] = None
        if baseobject is not None:
            # Add modifiers.
            self.scoreMultiplier = scoremp if scoremp is not None else self.baseObject.scoreMultiplier
            self.attackMultiplier = attackmp if attackmp is not None else self.baseObject.attackMultiplier
            self.defenceMultiplier = defensemp if defensemp is not None else self.baseObject.defenseMultiplier

            # self._objectData = {"Position": (None, None),
            #                     "Effects": [],
            #                     "Abilities": [],
            #                     "Attributes": {
            #                         "radius": None,
            #                         "health": None,
            #                         "speed": None
            #                     },
            #                     "Bases": {
            #                         "speed": None,
            #                         "radius": None,
            #                         "health": None
            #                     },
            #                     "Modifiers": {
            #                         "regenMultiplier": 0,
            #                         "scoreMultiplier": 0,
            #                         "attackMultiplier": 0,
            #                         "defenseMultiplier": 0
            #                     },
            #                     "Switches": {
            #                         "allowCollision": True,
            #                         "isInvulnerable": False
            #                     },
            #                     "ID": baseobject.get_uname()}

        # Base attributes.
        self.baseSpeed = speed
        self.baseRadius = int(radius / 2)
        self.baseRadiusF = radius / 2

        # Dynamic attributes.
        self.health = health
        self.speed = speed
        self.radius = int(radius / 2)
        self.radiusF = radius / 2

        # # Todo: Remove when object-data is fully using the get_objectdata me
        #  thod.
        # self._objectData["radius"] = radius
        # self._objectData["speed"] = speed
        # self._objectData["health"] = health
        # self._objectData["Position"] = (x, y)

    def reload(self, odata: dict):
        raise Exception("Test exception, reload is called!")

        if self.id is not None:
            raise OverflowError(f"BubbleObject is already created")
        
        for effectdata in odata["Effects"]:
            effect: effects.BaseEffect = Registry.get_effect(effectdata["id"])

            # Start the effect using saved effect data. Using the object-data (odata) given from the arguments.
            if effectdata["duration"] > 0.0:
                self.start_effect(
                    effect, Registry.get_scene("Game"), effectdata["duration"], effectdata["strength"],
                    **dict(effectdata["extradata"]))

        attributes = odata["Attributes"]
        self.speed = attributes["speed"]
        self.radius = attributes["radius"]
        self.radiusF = attributes["radiusF"]
        self.health = attributes["health"]
        self.maxHealth = attributes["maxHealth"]

        bases = odata["Bases"]
        self.baseSpeed = bases["speed"]
        self.baseHealth = bases["health"]
        self.baseRadius = bases["radius"]
        self.baseRadiusF = bases["radiusF"]

        modifiers = odata["Modifiers"]
        self.scoreMultiplier = modifiers["scoreMultiplier"]
        self.regenMultiplier = modifiers["regenMultiplier"]
        self.attackMultiplier = modifiers["attackMultiplier"]
        self.defenseMultiplier = modifiers["defenseMultiplier"]

        switches = odata["Switches"]
        self.allowCollision = switches["allowCollision"]
        self.isInvulnerable = switches["isInvulnerable"]

        # Create bubble image.
        self.id = Registry.get_scene("Game").canvas.create_image(
            *odata["Position"], image=Registry.get_texture(
                "qbubbles:bubble", self.baseObject.get_uname(), radius=self.radius))

        self.teleport(*odata["Position"])

        # Activate Events.
        UpdateEvent.bind(self.on_update)
        CleanUpEvent.bind(self.on_cleanup)
        CollisionEvent.bind(self.on_collision)
        PauseEvent.bind(self.on_pause)

    def add_effect(self, appliedeffect: effects.AppliedEffect):
        """
        Adds an effect, must be an AppliedEffect()-instance. For starting a new effect, use start_effect() instead.

        :param appliedeffect:
        :return:
        """

        self.appliedEffects[appliedeffect] = appliedeffect.baseObject
        # self.appliedEffectTypes.append(type(appliedeffect))

    def remove_effect(self, appliedeffect: effects.AppliedEffect):
        """
        Removes an applied-effect from the player's effect list.

        :param appliedeffect: The applied-effect to remove.
        :return:
        """

        # index = self.appliedEffects.index(appliedeffect)
        del self.appliedEffects[appliedeffect]

    def start_effect(self, effect_class: effects.BaseEffect, scene, duration: float, strength: _t.Union[float, int],
                     **extradata) -> effects.AppliedEffect:
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

        appliedeffect = effects.AppliedEffect(effect_class, scene, duration, strength, self, **extradata)
        self.appliedEffects[appliedeffect] = appliedeffect.baseObject

        return appliedeffect

    # noinspection PyDictCreation
    def get_objectdata(self):
        odata = {}

        # Position, Effects and Abilities
        odata["Position"] = self.get_coords()
        odata["Effects"] = [appliedeffect.get_data() for appliedeffect in self.appliedEffects]
        odata["Abilities"] = [ability.get_data() for ability in self.abilities]

        # Bases
        bases = {}
        bases["speed"] = self.baseSpeed
        bases["radius"] = self.baseRadius
        bases["radiusF"] = self.baseRadiusF
        bases["health"] = self.baseHealth
        odata["Bases"] = bases

        # Attributes
        attributes = {}
        attributes["maxHealth"] = self.maxHealth
        attributes["health"] = self.health
        attributes["radius"] = self.radius
        attributes["radiusF"] = self.radiusF
        attributes["speed"] = self.speed
        odata["Attributes"] = attributes

        switches = {}
        switches["allowCollision"] = self.allowCollision
        odata["Switches"] = switches

        # Modifiers
        modifiers = {}
        modifiers["regenMultiplier"] = self.regenMultiplier
        modifiers["scoreMultiplier"] = self.scoreMultiplier
        modifiers["attackMultiplier"] = self.attackMultiplier
        modifiers["defenseMultiplier"] = self.defenceMultiplier
        odata["Modifiers"] = modifiers

        # ID
        odata["ID"] = self.baseObject.get_uname()

        return odata

    # noinspection PyDictCreation
    def get_spritedata(self):
        sdata = {}
        sdata["objects"] = []
        sdata["speedMultiplier"] = 0.5
        sdata["id"] = self.get_sname()

        return sdata

    def on_collision(self, evt: CollisionEvent):
        if self.allowCollision:
            if evt.eventObject == self and evt.collidedObj != self:
                self.baseObject.on_collision(self, evt.collidedObj)

    def on_pause(self, evt: PauseEvent):
        self._pause = evt.pause

    def create(self, x, y):
        if self.baseObject is None:
            raise UnlocalizedNameError(f"BubbleObject is initialized as use for Sprite information, "
                                       f"use the baseobject argument with "
                                       f"a Bubble-instance instead of NoneType to fix this problem")
        if self.id is not None:
            raise OverflowError(f"BubbleObject is already created")
        canvas: Canvas = Registry.get_scene("Game").canvas

        # Logging.debug("BubbleObject", f"Creation RadiusF: {self.radiusF}")
        # Logging.debug("BubbleObject", f"Creation Radius: {self.radius}")

        # Create bubble image.
        self.id = canvas.create_image(
            x, y, image=Registry.get_texture("qbubbles:bubble", self.baseObject.get_uname(), radius=self.radiusF * 2))

        # Activate Events.
        UpdateEvent.bind(self.on_update)
        CleanUpEvent.bind(self.on_cleanup)
        CollisionEvent.bind(self.on_collision)
        PauseEvent.bind(self.on_pause)

        # print(f"Created Bubble\n Bubble Object Representation: {repr(self)}")

    def on_update(self, evt: UpdateEvent):
        # game_map = Registry.get_scene("Game").gameMap
        if not self._pause:
            spd_mpy = evt.scene.gameMap.player.score / 10000
            spd_mpy /= 2
            if spd_mpy < 0.5:
                spd_mpy = 0.5
            self.move(-self.baseSpeed * evt.dt * spd_mpy, 0)

    def save(self):
        return dict(self._spriteData)

    def on_cleanup(self, evt: CleanUpEvent):
        if self.dead:
            UpdateEvent.unbind(self.on_update)
            CleanUpEvent.unbind(self.on_cleanup)
            CollisionEvent.unbind(self.on_collision)
            PauseEvent.unbind(self.on_pause)
            self.delete()


class NormalBubble(Bubble):
    def __init__(self):
        super(NormalBubble, self).__init__()

        self.priority = 1500000

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 40
        self.maxSpeed: int = 96
        self.scoreMultiplier: float = 1
        self.attackMultiplier: float = 0

        self.set_uname("qbubbles:normal_bubble")


class DoubleBubble(Bubble):
    def __init__(self):
        super(DoubleBubble, self).__init__()

        self.priority = 150000

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 40
        self.maxSpeed: int = 96
        self.scoreMultiplier: float = 2
        self.attackMultiplier: float = 0

        self.set_uname("qbubbles:double_value")


class TripleBubble(Bubble):
    def __init__(self):
        super(TripleBubble, self).__init__()

        self.priority = 100000

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 40
        self.maxSpeed: int = 96
        self.scoreMultiplier: float = 3
        self.attackMultiplier: float = 0

        self.set_uname("qbubbles:triple_value")


class DoubleStateBubble(Bubble):
    def __init__(self):
        super(DoubleStateBubble, self).__init__()

        self.priority = 15000

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 40
        self.maxSpeed: int = 96

        self.scoreMultiplier: float = 2
        self.attackMultiplier: float = 0

        self.set_uname("qbubbles:double_state")

    def on_collision(self, bubbleobject: BubbleObject, other_object: Sprite):
        if other_object.get_sname() == "qbubbles:player":
            other_object: Player
            scene = Registry.get_scene("Game")
            other_object.start_effect(qbubbles.effects.ScoreMultiplierEffect(), scene,
                                      scene.gameMap.randoms["qbubbles:effect.duration"][0].randint(12, 17), 2)


class TripleStateBubble(Bubble):
    def __init__(self):
        super(TripleStateBubble, self).__init__()

        self.priority = 10000

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 40
        self.maxSpeed: int = 96

        self.scoreMultiplier: float = 3
        self.attackMultiplier: float = 0

        self.set_uname("qbubbles:triple_state")

    def on_collision(self, bubbleobject: BubbleObject, other_object: Sprite):
        if other_object.get_sname() == "qbubbles:player":
            other_object: Player
            scene = Registry.get_scene("Game")
            other_object.start_effect(qbubbles.effects.ScoreMultiplierEffect(), scene,
                                      scene.gameMap.randoms["qbubbles:effect.duration"][0].randint(7, 10), 3)


class DamageBubble(Bubble):
    def __init__(self):
        super(DamageBubble, self).__init__()

        self.priority = 1000000

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 40
        self.maxSpeed: int = 96

        self.scoreMultiplier: float = 0.5
        self.attackMultiplier: float = 1

        self.set_uname("qbubbles:damage_bubble")

        # raise RuntimeError("This is shit")


class HealBubble(Bubble):
    def __init__(self):
        super(HealBubble, self).__init__()

        self.priority = 100000

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 40
        self.maxSpeed: int = 96

        self.scoreMultiplier: float = 0.5
        self.attackMultiplier: float = -1

        self.set_uname("qbubbles:healer_bubble")

        # raise RuntimeError("This is shit")


class SpeedupBubble(Bubble):
    def __init__(self):
        super(SpeedupBubble, self).__init__()

        self.priority = 15000

        self.minRadius: int = 5
        self.maxRadius: int = 50
        self.minSpeed: int = 116
        self.maxSpeed: int = 228

        self.scoreMultiplier: float = 3
        self.attackMultiplier: float = 0

        self.set_uname("qbubbles:speedup")

    def on_collision(self, bubbleobject: BubbleObject, other_object: Sprite):
        if other_object.get_sname() == "player":
            other_object: Player
            if other_object.baseSpeed < 20:
                other_object.baseSpeed += int((bubbleobject.baseRadius / 5) + 5)


class TeleportBubble(Bubble):
    def __init__(self):
        super(TeleportBubble, self).__init__()

        self.priority = 10

        self.minRadius: int = 5
        self.maxRadius: int = 30
        self.minSpeed: int = 136
        self.maxSpeed: int = 204

        self.scoreMultiplier: float = 1
        self.attackMultiplier: float = 0

        self.set_uname("qbubbles:teleport_bubble")

    def on_collision(self, bubbleobject: BubbleObject, other_object: Player):
        if other_object.get_sname() == "player":
            other_object.get_ability("qbubbles:teleport")["value"] = \
                bubbleobject.baseSpeed / bubbleobject.baseObject.maxSpeed * 2
