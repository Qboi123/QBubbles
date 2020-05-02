import string as _str
import time as _time
import typing as _t

# import qbubbles.sprites
import qbubbles.globals as _g
import qbubbles.events as _evts
import qbubbles.exceptions as _exc


class BaseEffect(object):
    def __init__(self):
        """
        Base effect class constructor.
        """

        self.callWhen: _t.Callable[[object, float, _t.Union[float, int]], bool] = lambda game, time, strength: True
        self.incompatibles: _t.List[BaseEffect] = []

    def on_apply(self, effect: 'AppliedEffect', sprite):
        """
        Applief-effect start event handler.

        :param effect:
        :param sprite:
        :return:
        """

        pass

    def on_stop(self, effect: 'AppliedEffect', sprite):
        """
        Applied-effect stop event handler.

        :param effect:
        :param sprite:
        :return:
        """

        pass

    def __call__(self, game, time, strength) -> _t.Optional['AppliedEffect']:
        """
        Used for getting the applied effect for the sprite, featuring event handling and remaining time.

        :param game: The Game Scene
        :param time: The amount of time the effect shold be active
        :param strength: The strength of the effect
        :return: AppliedEffect instance or None if the BaseEffect callWhen call returns False.
        """
        if not self.callWhen(game, time, strength):
            return

        active_effects = [applied_effect.baseObject for applied_effect in game.player.appliedEffects]
        for base_effect in self.incompatibles:
            if base_effect in active_effects:
                return
            if self.__class__ in base_effect.incompatibles:
                return

        return AppliedEffect(self, game, time, strength)

    def set_uname(self, name):
        """
        Sets the unlocalized of the base-effect..

        :param name: The unlocalized name to set.
        :return:
        """

        for symbol in name:
            if symbol not in _str.ascii_letters+_str.digits+ "_":
                raise _exc.UnlocalizedNameError(f"Invalid character '{symbol}' for unlocalized name '{name}'")
        if name[0] not in _str.ascii_letters:
            raise _exc.UnlocalizedNameError(f"Invalid start character '{name[0]}' for unlocalized name '{name}'")
        if name[-1] not in _str.ascii_letters+_str.digits:
            raise _exc.UnlocalizedNameError(f"Invalid start character '{name[-1]}' for unlocalized name '{name}'")

        if self in _g.EFFECT2NAME.keys():
            raise ValueError(f"Effect '{self.__class__.__module__}.{self.__class__.__name__}' has already an unlocalized name")
        if self in _g.NAME2EFFECT.values():
            raise ValueError(f"Effect '{self.__class__.__module__}.{self.__class__.__name__}' has already an unlocalized name")
        if name in _g.EFFECT2NAME.values():
            raise ValueError(f"Name '{name}' already defined for effect '{self.__class__.__module__}.{self.__class__.__name__}'")
        if name in _g.NAME2EFFECT.keys():
            raise ValueError(f"Name '{name}' already defined for effect '{self.__class__.__module__}.{self.__class__.__name__}'")

        return self.get_uname()

    def __repr__(self):
        return f"Effect(<{self.get_uname()}>)"

    def get_uname(self):
        """
        Gets the unlocalized name of the base-effect.

        :returns: The unlocalized name of the base-effect.
        """

        if self not in _g.EFFECT2NAME.keys():
            raise ValueError(f"Effect '{self.__class__.__module__}.{self.__class__.__name__}' has no unlocalized name")

        return _g.EFFECT2NAME[self]


class AppliedEffect(object):
    def __init__(self, baseclass: BaseEffect, game, duration: float, strength: _t.Union[float, int],
                 sprite, **extradata):
        """
        Applied effect, is an effect that is applied to an sprite / entity like a player or a bubble.

        :param baseclass: The BaseEffect()-instance. Used for ID and events.
        :param game: The Game-Scene instance
        :param duration: The effect duration.
        :param strength: The effect strength.
        :param extradata: The extra data to add to the effect.
        """

        self.baseObject: BaseEffect = baseclass
        self.baseUname: str = baseclass.get_uname()
        self.strength = strength
        self.extraData = extradata
        self._game = game

        self.boundSprite = sprite

        self._pause = False
        self.dead = False
        self.pause_duration: _t.Optional[float] = None

        if duration < 0:
            self.dead = True

        self._endTime = _time.time() + duration

    def __repr__(self):
        return f"AppliefEffect(<{self.baseObject.get_uname()}>, {self.get_remaining_time()}, {self.strength})"

    def get_end_time(self):
        """
        Gets the end time of the effect, can be changed using set_remaining_time().

        :returns: The end time of the effect
        """

        return self._endTime

    def on_pause(self, evt: _evts.PauseEvent):
        self._pause = evt.pause

        if evt.pause is True:
            self.pause_duration = self.get_remaining_time()

    def get_data(self):
        return {"id": self.baseUname, "duration": self.get_remaining_time(), "strength": self.strength}

    def on_stop(self, sprite):
        self.baseObject.on_stop(self, sprite)

    def on_apply(self, sprite):
        self.baseObject.on_apply(self, sprite)

    def on_update(self, evt: _evts.UpdateEvent):
        if self.get_remaining_time() < 0:
            self.dead = True
            return
        elif self._pause:
            self.set_remaining_time(self.pause_duration)
        else:
            self.baseObject.on_update(self)

        self.on_stop()

    def get_uname(self):
        """
        Gets the unlocalized name of the base-effect.

        :return:
        """

        return self.baseObject.get_uname()

    def get_remaining_time(self) -> float:
        """
        Gets the remaining time of the effect.

        :return:
        """

        return self._endTime - _time.time()

    def set_remaining_time(self, time_length: float):
        """
        Sets the remaining time of the effect.

        :param time_length:
        :return:
        """

        self._endTime = _time.time() + time_length


class SpeedBoostEffect(BaseEffect):
    def __init__(self):
        super(SpeedBoostEffect, self).__init__()

    def on_apply(self, effect: 'AppliedEffect', sprite):
        sprite.speed += (effect.strength * sprite.baseSpeed) / 4

    def on_stop(self, effect: 'AppliedEffect', sprite):
        sprite.speed -= (effect.strength * sprite.baseSpeed)


class DefenceBoostEffect(BaseEffect):
    def __init__(self):
        super(DefenceBoostEffect, self).__init__()

    def on_apply(self, effect: 'AppliedEffect', sprite):
        sprite.defence += effect.strength * 2

    def on_stop(self, effect: 'AppliedEffect', sprite):
        sprite.defence -= effect.strength * 2
