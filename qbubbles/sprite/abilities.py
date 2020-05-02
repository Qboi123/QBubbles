from typing import Optional

from qbubbles.advUtils.time import Time, TimeSpan
from qbubbles.events import KeyPressEvent, KeyReleaseEvent, CollisionEvent, SpriteDamageEvent


class Ability(object):
    def __init__(self, sprite):
        self.energy = 0
        self._sprite = sprite
        KeyPressEvent.bind(self.on_keypress)
        KeyReleaseEvent.bind(self.on_keyrelease)

        self._uname = None

    def set_uname(self, uname):
        self._uname = uname

    def get_uname(self):
        return self._uname

    def on_keypress(self, event: KeyPressEvent):
        pass

    def on_keyrelease(self, event: KeyReleaseEvent):
        pass

    def on_sprite_move(self, event):
        pass

    def on_sprite_death(self, event):
        pass

    def get_data(self):
        return {"id": self.get_uname(), "energy": self.energy}


class GhostAbility(Ability):
    def __init__(self, sprite):
        super(GhostAbility, self).__init__(sprite)

        CollisionEvent.bind(self.on_collision)

        self.set_uname("qbubbles:ghost_ability")

    def on_collision(self, event: CollisionEvent):
        if event.eventObject == self._sprite:
            event.collidedObj.skip_collision(self._sprite)
        elif event.collidedObj == self._sprite:
            event.eventObject.skip_collision(self._sprite)


class TeleportAbility(Ability):
    def __init__(self, sprite):
        super(TeleportAbility, self).__init__(sprite)

        self.loadedTime: Optional[Time] = None

        self.set_uname("qbubbles:teleport_ability")

    def on_keypress(self, evt: KeyPressEvent):
        if evt.keySym.lower() != "shift_l":
            print(f"[Test] TeleportAbility<KeyPressEvent.keySym.lower()>: {evt.keySym.lower()}")
            return
        self.loadedTime = Time.system_time()

    def on_keyrelease(self, evt: KeyReleaseEvent):
        if self.loadedTime is None:
            return
        if evt.keySym.lower() != "shift_l":
            print(f"[Test] TeleportAbility<KeyReleaseEvent.keySym.lower()>: {evt.keySym.lower()}")
            return
        timeSpan = TimeSpan(self.loadedTime, Time.system_time())
        timeLength = timeSpan.get_timelength()
        if 0 < timeLength.get_seconds() <= 0.25:
            pixels = 1
        elif 0.25 < timeLength.get_seconds() <= 0.5:
            pixels = 2
        elif 0.5 < timeLength.get_seconds() <= 1:
            pixels = 4
        elif 1 < timeLength.get_seconds() <= 3:
            pixels = 8
        elif 3 < timeLength.get_seconds() <= 5:
            pixels = 16
        elif 5 < timeLength.get_seconds() <= 7.5:
            pixels = 32
        elif 7.5 < timeLength.get_seconds() <= 10:
            pixels = 64
        elif 10 < timeLength.get_seconds() <= 60:
            pixels = 128
        elif 60 < timeLength.get_seconds():
            pixels = 256


class InvulnerableAbility(Ability):
    def __init__(self, sprite):
        super(InvulnerableAbility, self).__init__(sprite)

        SpriteDamageEvent.bind(self.on_sprite_damage)

        self.set_uname("qbubbles:invulnerable_ability")

    def on_sprite_damage(self, event):
        if event.sprite != self._sprite:
            return
        return "cancel"
