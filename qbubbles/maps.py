import os
from inspect import ismethod, isfunction
from random import Random
from tkinter import Canvas, TclError
from typing import Dict, Tuple, Optional, List, Callable, Any

import dill

from qbubbles.advUtils.time import TimeLength
from qbubbles.bubbleSystem import BubbleSystem
from qbubbles.bubbles import Bubble, BubbleObject
from qbubbles.config import Reader
from qbubbles.events import UpdateEvent, CollisionEvent, KeyPressEvent, KeyReleaseEvent, XInputEvent, \
    MapInitializeEvent, FirstLoadEvent, SaveEvent, LoadCompleteEvent, GameExitEvent, PauseEvent, EffectApplyEvent, \
    RegionEnterEvent, RegionLeaveEvent
from qbubbles.gameIO import printerr
from qbubbles.gui import CPanel, CEffectBarArea
# from qbubbles.nzt import NZTFile
from qbubbles.registry import Registry
from qbubbles.sprites import Sprite, Player, DimensionalPlayer
from qbubbles.utils import Font
import qbubbles.gameIO as _gameIO


class GameMap(object):
    def __init__(self):
        self._bubbles = []
        self._gameobjects = []
        self.player: Optional[Player] = None
        self.seedRandom = None
        self.randoms: Dict[str, Tuple[Random, int]] = {}
        self._uname = None

    def load(self):
        MapInitializeEvent.bind(self.on_mapinit)
        FirstLoadEvent.bind(self.on_firstload)
        LoadCompleteEvent.bind(self.on_loadcomplete)

    def on_gamexit(self):
        MapInitializeEvent.unbind(self.on_mapinit)
        FirstLoadEvent.unbind(self.on_firstload)
        LoadCompleteEvent.unbind(self.on_loadcomplete)

    def on_loadcomplete(self, evt: LoadCompleteEvent):
        pass

    def get_gameobjects(self) -> List[Sprite]:
        return self._gameobjects

    @staticmethod
    def get_bubbles():
        return Registry.saveData["Sprites"]["qbubbles:bubble"]["objects"]

    def create(self, seed, randoms=None):
        self.seedRandom = seed
        self.randoms: Dict[str, Tuple[Random, int]] = {}
        if randoms is not None:
            for random in randoms:
                randomState = random["State"]
                offset = random["offset"]
                id_ = random["id"]

                # noinspection PyNoneFunctionAssignment,PyTypeChecker
                r: Random = Random(self.seedRandom << offset).setstate(randomState)
                self.randoms[id_] = (r, offset)
        else:
            self.init_defaults()
        self._uname = None

    def add_random(self, id_, offset):
        if id_.count(":") != 1:
            printerr(f"Randomizer id must contain a single COLON, id: {id_}")
        self.randoms[id_] = self.format_random(offset)

    def init_defaults(self):
        self.add_random("qbubbles:effect.duration", 24)
        self.add_random("qbubbles:effect.strength", 16)
        self.add_random("qbubbles:bubblesystem", 4096)
        self.add_random("qbubbles:bubble.radius", 32)
        self.add_random("qbubbles:bubble.speed", 64)
        self.add_random("qbubbles:bubble.x", 128)
        self.add_random("qbubbles:bubble.y", 256)

    def on_mapinit(self, evt: MapInitializeEvent):
        pass

    def on_firstload(self, evt: FirstLoadEvent):
        pass

    def format_random(self, offset):
        if offset % 4 == 0:
            return Random(self.seedRandom << offset), offset
        else:
            raise ValueError("Offset must be multiple of 4")

    def __setattr__(self, key, value):
        if key == "format_random":
            if value != self.format_random:
                raise PermissionError("Cannot set format_random")
        self.__dict__[key] = value

    def set_uname(self, uname):
        self._uname = uname

    def get_uname(self):
        return self._uname

    def get_save_data(self):
        randoms = []
        for id, data in self.randoms.items():
            sdata = {}
            random: Random = data[0]
            sdata["State"] = random.getstate()
            sdata["offset"] = data[1]
            sdata["id"] = id
            randoms.append(sdata)

    def create_random_bubble(self, *, x=None, y=None):
        # Get random bubble.
        bubbleobject = self.get_random_bubble()

        # Get width and height of window
        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]

        # Get random x or/and y coordinates for the bubble.
        if x is None:
            x = self.randoms["qbubbles:bubble.x"][0].randint(0 - bubbleobject.radiusF, w + bubbleobject.radiusF)
        if y is None:
            y = self.randoms["qbubbles:bubble.y"][0].randint(0 - bubbleobject.radiusF, h + bubbleobject.radiusF)
        self.create_bubble(x, y, bubbleobject)

    def get_random_bubble(self) -> BubbleObject:
        bubble: Bubble = BubbleSystem.random(self.randoms["qbubbles:bubblesystem"][0])
        radius = self.randoms["qbubbles:bubble.radius"][0].randint(bubble.minRadius, bubble.maxRadius)
        speed = self.randoms["qbubbles:bubble.speed"][0].randint(bubble.minSpeed, bubble.maxSpeed)

        max_health = 1
        if hasattr(bubble, "maxHealth"):
            max_health = bubble.maxHealth

        return BubbleObject(
            bubble, max_health, max_health, radius=radius, speed=speed, health=bubble.hardness,
            scoremp=bubble.scoreMultiplier, attackmp=bubble.attackMultiplier, defensemp=bubble.defenseMultiplier)

    def create_bubble(self, x: int, y: int, bubble_object: BubbleObject):
        """
        Creates a bubble puts it into the gameobjects and bubbles list.

        :param x: The x-coordinate of the bubble to create.
        :param y: The y-coordinate of the bubble to create.
        :param bubble_object: The bubble object, to use for creating the bubble.
        :returns: The bubble object that was created.
        :raises AssertionError: if the bubble object is a type.
        """

        assert type(bubble_object) != type

        bubble_object.create(x=x, y=y)
        self._bubbles.append(bubble_object)
        self._gameobjects.append(bubble_object)
        return bubble_object

    def delete_bubble(self, bubble_object: BubbleObject):
        """
        Deletes a bubble from the game.

        :param bubble_object: The bubble object to delete.
        :returns: The bubble object that was deleted.
        """

        self._bubbles.remove(bubble_object)
        self._gameobjects.remove(bubble_object) if bubble_object in self._gameobjects else None
        bubble_object.delete()
        return bubble_object

    def on_update(self, evt: UpdateEvent):
        pass

    def on_collision(self, evt: CollisionEvent):
        pass

    def on_keypress(self, evt: KeyPressEvent):
        pass

    def on_keyrelease(self, evt: KeyReleaseEvent):
        pass

    def on_xinput(self, evt: XInputEvent):
        pass

    def __repr__(self):
        return f"GameMap<{self.get_uname()}>"

    def load_savedata(self, path):
        raise RuntimeError("Default Game Map does not support loading savedata")

    def save_savedata(self, path):
        raise RuntimeError("Default Game Map does not support saving savedata")

    def create_savedata(self, path, seed):
        raise RuntimeError("Default Game Map does not support creating savedata")


class ClassicMap(GameMap):
    def __init__(self):
        """
        Classic outdated game map.
        """

        super(ClassicMap, self).__init__()

        self._pause = False
        self.set_uname("qbubbles:classic_map")
        self.maxBubbles = 100
        self.texts = {}
        self.panelTop: Optional[CPanel] = None
        self.tSpecialColor = "#ffffff"
        self.tNormalColor = "#3fffff"
        self.effectImages = {}
        self.effectX = 100

    def init_defaults(self):
        """
        Initialize the default randomizers.

        :return:
        """

        self.add_random("qbubbles:effect.duration", 24)
        self.add_random("qbubbles:effect.strength", 16)
        self.add_random("qbubbles:bubblesystem", 4096)
        self.add_random("qbubbles:bubblesystem.start_x", 8)
        self.add_random("qbubbles:bubblesystem.start_y", 12)
        self.add_random("qbubbles:bubble.radius", 32)
        self.add_random("qbubbles:bubble.speed", 64)
        self.add_random("qbubbles:bubble.x", 128)
        self.add_random("qbubbles:bubble.y", 256)

    def on_effect_apply(self, evt: EffectApplyEvent):
        """
        On effect apply event handler, used for displaying the current effects.

        :param evt: The event object.
        :return:
        """

        if evt.sprite == self.player:
            self.effectX += 256
            lname = Registry.get_lname("effect", evt.appliedEffect.get_uname().replace(":", "."), "name")
            name = Registry.gameData["language"][lname] if lname in Registry.gameData["language"].keys() else lname
            self.effectImages[evt.appliedEffect] = {
                # Textures
                "effectBar": self.canvas.create_image(
                    self.effectX, 5,
                    image=Registry.get_texture(
                        "gui", "qbubbles:effect_bar", gamemap=self.get_uname()), anchor="nw"
                ),
                "icon": self.canvas.create_image(
                    self.effectX+1, 6,
                    image=Registry.get_texture(
                        "effect", evt.appliedEffect.get_uname(), gamemap=self.get_uname()), anchor="nw"
                ),

                # Texts
                "text": self.canvas.create_text(
                    self.effectX + 36, 18,
                    text=name % {
                        "strength": int(evt.appliedEffect.strength)
                    }, anchor="w"
                ),
                "time": self.canvas.create_text(
                    self.effectX + 200, 18, text=str(TimeLength(evt.appliedEffect.get_remaining_time())), anchor="w"
                )
            }
        
    def on_firstload(self, evt: FirstLoadEvent):
        """
        Event handler for initialize the save when loaded for the first time.

        :param evt:
        :return:
        """

        FirstLoadEvent.unbind(self.on_firstload)

        _gameIO.Logging.info("Gamemap", "Create bubbles because the save is loaded for first time")

        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]
        for i in range(self.maxBubbles):
            self.create_random_bubble()
        Registry.saveData["Game"]["GameMap"]["initialized"] = True
        self.player.teleport(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"])

    def on_mapinit(self, evt: MapInitializeEvent):
        """
        Gamemap initialization event handler. (GIEH)

        :param evt:
        :return:
        """

        MapInitializeEvent.unbind(self.on_mapinit)

        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]

        self.seedRandom = Registry.saveData["Game"]["GameMap"]["seed"]
        self.init_defaults()

        canvas: Canvas = evt.canvas

        t1 = evt.t1
        t2 = evt.t2

        # noinspection PyUnusedLocal
        self.panelTop = CPanel(canvas, 0, 0, width="extend", height=69, fill="darkcyan", outline="darkcyan")
        # print(f"Panel Top created: {self.panelTop}")
        panelTopFont = Font("Helvetica", 12)

        # # Initializing the panels for the game.
        # self.panels["game/top"] = canvas.create_rectangle(
        #     -1, -1, Registry.gameData["WindowWidth"], 69, fill="darkcyan"
        # )

        # Create seperating lines.
        canvas.create_line(0, 70, Registry.gameData["WindowWidth"], 70, fill="lightblue")
        canvas.create_line(0, 69, Registry.gameData["WindowWidth"], 69, fill="lightblue")

        canvas.create_text(
            55, 30, text=Registry.get_lname("info", "score"),
            fill=self.tSpecialColor, font=panelTopFont.get_tuple())
        canvas.itemconfig(t2, text="Score")
        canvas.create_text(
            110, 30, text=Registry.get_lname("info", "level"),
            fill=self.tSpecialColor, font=panelTopFont.get_tuple())
        canvas.itemconfig(t2, text="Level")
        canvas.create_text(
            165, 30, text=Registry.get_lname("info", "speed"),
            fill=self.tSpecialColor, font=panelTopFont.get_tuple())
        canvas.itemconfig(t2, text="Speed")
        canvas.create_text(
            220, 30, text=Registry.get_lname("info", "lives"),
            fill=self.tSpecialColor, font=panelTopFont.get_tuple())
        canvas.itemconfig(t2, text="Lives")

        CEffectBarArea(canvas, gamemap=self)

        canvas.create_text(1120, 30, text=Registry.gameData["language"]["info.tps"],
                           fill=self.tNormalColor, font=panelTopFont.get_tuple())
        canvas.itemconfig(t2, text="Teleports")

        # Coin / Diamond icons
        canvas.create_image(1185, 30, image=Registry.get_icon("StoreDiamond"))
        canvas.itemconfig(t2, text="Diamonds")
        canvas.create_image(1185, 50, image=Registry.get_icon("StoreCoin"))
        canvas.itemconfig(t2, text="Coins")

        canvas.itemconfig(t1, text="Creating Stats Data")
        canvas.itemconfig(t2, text="")

        # Game information values.
        self.texts["score"] = canvas.create_text(55, 50, fill="cyan")
        canvas.itemconfig(t2, text="Score")
        self.texts["level"] = canvas.create_text(110, 50, fill="cyan")
        canvas.itemconfig(t2, text="Level")
        self.texts["speed"] = canvas.create_text(165, 50, fill="cyan")
        canvas.itemconfig(t2, text="Speed")
        self.texts["lives"] = canvas.create_text(220, 50, fill="cyan")
        canvas.itemconfig(t2, text="Lives")

        self.texts["shiptp"] = canvas.create_text(w-20, 10, fill="cyan")
        canvas.itemconfig(t2, text="Teleports")
        self.texts["diamond"] = canvas.create_text(w-20, 30, fill="cyan")
        canvas.itemconfig(t2, text="Diamonds")
        self.texts["coin"] = canvas.create_text(w-20, 50, fill="cyan")
        canvas.itemconfig(t2, text="Coins")
        self.texts["level-view"] = canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"],
                                                      fill='Orange',
                                                      font=Font("Helvetica", 46).get_tuple())
        canvas.itemconfig(t2, text="Level View")

        self.background = CPanel(canvas, 0, 71, "extend", "expand", fill="#00a7a7", outline="#00a7a7")

        self.canvas = canvas

        LoadCompleteEvent.bind(self.on_loadcomplete)
        EffectApplyEvent.bind(self.on_effect_apply)

        bubbles = Registry.saveData["Sprites"]["qbubbles:bubble"]["objects"].copy()
        Registry.saveData["Sprites"]["qbubbles:bubble"]["objects"] = []
        for bubble in bubbles:
            bub = Registry.get_bubble(bubble["ID"])
            pos = bubble["Position"]
            x = pos[0]
            y = pos[1]
            rad = bubble["Attributes"]["radius"]
            spd = bubble["Attributes"]["speed"]
            hlt = bubble["Attributes"]["health"]
            bub_obj = BubbleObject(bub, bub.hardness)
            bub_obj.reload(bubble)
            self._gameobjects.append(bub_obj)
            self._bubbles.append(bub_obj)

        # Create the player, if the player has already been initialized, reload it.
        self.player = Player()
        if Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Position"]:
            self.player.create(*Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Position"])
            self.player.reload(Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0])
        else:
            self.player.create(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"])
        self._gameobjects.append(self.player)

    def on_pause(self, evt: PauseEvent):
        """
        Pause event handler.

        :param evt:
        :return:
        """

        self._pause = evt.pause

    def on_update(self, evt: UpdateEvent):
        """
        Update event handler.

        :param evt:
        :return:
        """

        if self._pause:
            return

        if len(self._bubbles) < self.maxBubbles:
            bubbleObject = self.get_random_bubble()
            w = Registry.gameData["WindowWidth"]
            h = Registry.gameData["WindowHeight"]

            x = w + bubbleObject.radius
            y = self.randoms["qbubbles:bubble.y"][0].randint(71 + bubbleObject.radius, h - bubbleObject.radius)
            self.create_bubble(x, y, bubbleObject)
        self.canvas.itemconfig(self.texts["score"], text=f"{self.player.score}")
        self.canvas.itemconfig(self.texts["level"], text=f"{self.player.get_objectdata()['Attributes']['level']}")
        self.canvas.itemconfig(self.texts["lives"], text=f"{round(self.player.health, 1)}")
        self.canvas.itemconfig(self.texts["score"], text=f"{self.player.score}")

        move_left = 0
        for appliedeffect, dict_ in self.effectImages.copy().items():

            self.canvas.itemconfig(dict_["time"],
                                   text=str(TimeLength(appliedeffect.get_remaining_time())))

            self.canvas.move(dict_["icon"], -move_left, 0)
            self.canvas.move(dict_["time"], -move_left, 0)
            self.canvas.move(dict_["text"], -move_left, 0)
            self.canvas.move(dict_["effectBar"], -move_left, 0)

            if appliedeffect.get_remaining_time() < 0:
                appliedeffect.dead = True

            if appliedeffect.dead:
                self.canvas.delete(dict_["icon"])
                self.canvas.delete(dict_["time"])
                self.canvas.delete(dict_["text"])
                self.canvas.delete(dict_["effectBar"])

                del self.effectImages[appliedeffect]
                move_left += 256
                self.effectX -= 256

        # self.texts["score"] = self.player.score
        for bubble in self._bubbles.copy():
            bubble: BubbleObject
            if not bubble.dead:
                # print((-bubble.radius))
                if bubble.get_coords()[0] < -bubble.baseRadius:
                    bubble.instant_death()
            else:
                self._gameobjects.remove(bubble)
                self._bubbles.remove(bubble)

    def create_random_bubble(self, *, x=None, y=None):
        """
        Create a random bubble at x, and y. If x is None, choose a random x coordinate, same for y.

        :param x: The x-coordinate of the bubble to create, If None, choose a random x coordinate.
        :param y: The y-coordinate of the bubble to create, If None, choose a random y coordinate.
        :returns: The random created bubble.
        """

        bubble_object = self.get_random_bubble()
        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]

        if x is None:
            x = self.randoms["qbubbles:bubble.x"][0].randint(0 - bubble_object.radius, w + bubble_object.radius)
        if y is None:
            y = self.randoms["qbubbles:bubble.y"][0].randint(71 + bubble_object.radius, h - bubble_object.radius)
        return self.create_bubble(x, y, bubble_object)

    def on_loadcomplete(self, evt: LoadCompleteEvent):
        """
        Event handler for when game loading is complete.

        :param evt: Event object.
        :return:
        """

        # Unbinds
        LoadCompleteEvent.unbind(self.on_loadcomplete)

        # Binds
        UpdateEvent.bind(self.on_update)
        PauseEvent.bind(self.on_pause)
        GameExitEvent.bind(self.on_gameexit)
        SaveEvent.bind(self.on_save)

        _gameIO.Logging.info("Gamemap", "Load Complete")

        self.player.activate_events()

    # noinspection PyStatementEffect,PyCallingNonCallable,PyUnusedLocal
    def on_gameexit(self, evt: GameExitEvent):
        """
        Event handler for when the game exists.
        It will unbind all events, and remove the player and  all gameobjects, bubbles.

        :param evt: Event object.
        :return:
        """

        # Log
        _gameIO.Logging.info("Gamemap", "Exiting Game: Game Map -  Stage 1 (Unbining events)")

        # Unbinds
        UpdateEvent.unbind(self.on_update)
        PauseEvent.unbind(self.on_pause)
        GameExitEvent.unbind(self.on_gameexit)
        SaveEvent.unbind(self.on_save)

        # Log
        _gameIO.Logging.info("Gamemap", "Exiting Game: Game Map -  Stage 2 (Removing Gameobjects)")

        # Removing GameMaps
        for gameobject in self._gameobjects.copy():
            gameobject: Sprite
            try:
                if hasattr(gameobject, "delete"):
                    if ismethod(gameobject.delete):
                        gameobject.delete()
                    elif isfunction(gameobject.delete):
                        gameobject.delete()
                elif hasattr(gameobject, "destroy"):
                    if ismethod(gameobject.destroy):
                        gameobject.destroy()
                    elif isfunction(gameobject.destroy):
                        gameobject.destroy()
            except TclError:
                pass
            try:
                self._gameobjects.remove(gameobject)
            except KeyError:
                pass

        # Log
        _gameIO.Logging.info("Gamemap", "Exiting Game: Game Map -  Stage 3 (Removing Bubbles)")

        for bubble in self._bubbles.copy():
            bubble: BubbleObject

            try:
                bubble.delete()
            except TclError:
                pass
            try:
                self._bubbles.remove(bubble)
            except KeyError:
                pass

        try:
            self.player.delete()
        except TclError:
            pass

        # Log
        _gameIO.Logging.info(
            "Gamemap",
            "Exiting Game: Game Map -  Stage 4 (Empty Bubble and Gameobject lists, deactivate and delete player)")

        self._bubbles = []
        self._gameobjects = []
        self.player.deactivate_events()
        self.player.delete()
        del self.player

    def on_save(self, evt: SaveEvent):
        """
        Event handler, called when the game would be saved.

        :param evt:
        :return:
        """

        save_path = f"{Registry.gameData['launcherConfig']['gameDir']}saves/{evt.saveName}"
        return self.save_savedata(save_path)

    def load_savedata(self, path):
        """
        Loads the savedata.

        :param path:
        :return:
        """

        # Get registry values of Sprite Info, and Sprites
        Registry.saveData["SpriteInfo"] = Reader(f"{path}/spriteinfo.dill").get_decoded()
        Registry.saveData["Sprites"] = {}

        # Retrieve maximum number of bubbles active at once.
        self.maxBubbles = Registry.saveData["SpriteInfo"]["qbubbles:bubble"]["maxAmount"]

        # Get Sprite data
        for sprite_id in Registry.saveData["SpriteInfo"]["Sprites"]:
            sprite_path = sprite_id.replace(":", "/")
            data = Reader(f"{path}/sprites/{sprite_path}.dill").get_decoded()
            Registry.saveData["Sprites"][sprite_id] = data

    def save_savedata(self, path):
        """
        Saves the savedata.

        :param path:
        :return:
        """

        save_data = Registry.saveData.copy()

        # Transform Object data into List / Dict data.
        for sprite in Registry.get_sprites():
            save_data["Sprites"][sprite.get_sname()]["objects"] = []
            _gameIO.Logging.debug("GameMapSaving", f"SpriteData: {save_data['Sprites'][sprite.get_sname()]}")
        for sprite in self.get_gameobjects():
            save_data["Sprites"][sprite.get_sname()]["objects"].append(sprite.get_objectdata())
        for sprite in Registry.get_sprites():
            _gameIO.Logging.debug("GameMapSaving", f"SpriteData: {save_data['Sprites'][sprite.get_sname()]}")
        #  = sprite_data2

        game_data = save_data["Game"].copy()
        sprite_info_data = save_data["SpriteInfo"].copy()
        sprite_data = save_data["Sprites"].copy()

        with open(f"{path}/game.dill", "wb+") as file:
            dill.dump(game_data, file)
            file.close()
        with open(f"{path}/spriteinfo.dill", "wb+") as file:
            dill.dump(sprite_info_data, file)
            file.close()

        if not os.path.exists(f"{path}/sprites/"):
            os.makedirs(f"{path}/sprites/")

        for sprite in sprite_data.keys():
            sprite_path = '/'.join(sprite.split(":")[:-1])
            if not os.path.exists(f"{path}/sprites/{sprite_path}"):
                os.makedirs(f"{path}/sprites/{sprite_path}", exist_ok=True)

            with open(f"{path}/sprites/{sprite.replace(':', '/')}.dill", "wb+") as file:
                dill.dump(sprite_data[sprite], file)
                file.close()

    def create_savedata(self, path, seed):
        """
        Creates / resets the savedata.

        :param path:
        :param seed:
        :return:
        """

        game_data = {
            "GameInfo": {
                "seed": seed
            },
            "GameMap": {
                "id": self.get_uname(),
                "seed": seed,
                "initialized": False,
                "Randoms": []
            }
        }

        def dict_exclude_key(key, d: dict):
            d2 = d.copy()
            del d2[key]
            return d2

        spriteinfo_data = {
            "qbubbles:bubble": {
                "speedMultiplier": 5,
                "maxAmount": 100
            },
            "Sprites": [
                sprite.get_sname() for sprite in Registry.get_sprites()
            ],
            "SpriteData": dict([
                (
                    s.get_sname(), dict_exclude_key(
                        "objects", dict(s.get_spritedata())
                    )
                )
                for s in Registry.get_sprites()
            ])
        }

        sprite_data = dict()
        for sprite in Registry.get_sprites():
            sprite_data[sprite.get_sname()] = sprite.get_spritedata()

        Registry.saveData = {"GameData": game_data, "SpriteInfo": spriteinfo_data, "SpriteData": sprite_data}

        bubble_data = {"bub-id": [], "bub-special": [], "bub-action": [], "bub-radius": [], "bub-speed": [],
                       "bub-position": [], "bub-index": [], "key-active": False}

        with open(f"{path}/game.dill", "wb+") as file:
            dill.dump(game_data, file)
            file.close()

        with open(f"{path}/spriteinfo.dill", "wb+") as file:
            dill.dump(spriteinfo_data, file)
            file.close()

        os.makedirs(f"{path}/sprites/", exist_ok=True)

        for sprite in sprite_data.keys():
            if not os.path.exists(f"{path}/sprites/{sprite.replace(':', '/')}"):
                os.makedirs(f"{path}/sprites/{sprite.replace(':', '/')}", exist_ok=True)

            with open(f"{path}/sprites/{sprite.replace(':', '/')}.dill", "wb+") as file:
                dill.dump(sprite_data[sprite], file)
                file.close()

        # Todo: Remove, it's unused.
        with open(f"{path}/bubble.dill", "wb+") as file:
            dill.dump(bubble_data, file)


class DimensionalMap(ClassicMap):
    def __init__(self):
        super(DimensionalMap, self).__init__()

        self.set_uname("qbubbles:dimensional_map")

    def init_defaults(self):
        self.add_random("qbubbles:effect.duration", 24)
        self.add_random("qbubbles:effect.strength", 16)
        self.add_random("qbubbles:bubblesystem", 4096)
        self.add_random("qbubbles:bubble.radius", 32)
        self.add_random("qbubbles:bubble.speed", 64)
        self.add_random("qbubbles:bubble.x", 128)
        self.add_random("qbubbles:bubble.y", 256)

    @staticmethod
    def on_region_enter(evt: RegionEnterEvent):
        rx, ry = evt.region

    @staticmethod
    def on_region_leave(evt: RegionLeaveEvent):
        rx, ry = evt.region

    def on_mapinit(self, evt: MapInitializeEvent):
        """
        Gamemap initialization event handler. (GIEH)

        :param evt:
        :return:
        """

        MapInitializeEvent.unbind(self.on_mapinit)

        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]

        self.seedRandom = Registry.saveData["Game"]["GameMap"]["seed"]
        self.init_defaults()

        canvas: Canvas = evt.canvas

        t1 = evt.t1
        t2 = evt.t2

        # noinspection PyUnusedLocal
        self.panelTop = CPanel(canvas, 0, 0, width="extend", height=69, fill="darkcyan", outline="darkcyan")
        # print(f"Panel Top created: {self.panelTop}")
        panel_top_font = Font("Helvetica", 12)

        # # Initializing the panels for the game.
        # self.panels["game/top"] = canvas.create_rectangle(
        #     -1, -1, Registry.gameData["WindowWidth"], 69, fill="darkcyan"
        # )

        # Create seperating lines.
        canvas.create_line(0, 70, Registry.gameData["WindowWidth"], 70, fill="lightblue")
        canvas.create_line(0, 69, Registry.gameData["WindowWidth"], 69, fill="lightblue")

        canvas.create_text(
            55, 30, text=Registry.get_lname("info", "score"),
            fill=self.tSpecialColor, font=panel_top_font.get_tuple())
        canvas.itemconfig(t2, text="Score")
        canvas.create_text(
            110, 30, text=Registry.get_lname("info", "level"),
            fill=self.tSpecialColor, font=panel_top_font.get_tuple())
        canvas.itemconfig(t2, text="Level")
        canvas.create_text(
            165, 30, text=Registry.get_lname("info", "speed"),
            fill=self.tSpecialColor, font=panel_top_font.get_tuple())
        canvas.itemconfig(t2, text="Speed")
        canvas.create_text(
            220, 30, text=Registry.get_lname("info", "lives"),
            fill=self.tSpecialColor, font=panel_top_font.get_tuple())
        canvas.itemconfig(t2, text="Lives")

        CEffectBarArea(canvas, gamemap=self)

        canvas.create_text(1120, 30, text=Registry.gameData["language"]["info.tps"],
                           fill=self.tNormalColor, font=panel_top_font.get_tuple())
        canvas.itemconfig(t2, text="Teleports")

        # Coin / Diamond icons
        canvas.create_image(1185, 30, image=Registry.get_icon("StoreDiamond"))
        canvas.itemconfig(t2, text="Diamonds")
        canvas.create_image(1185, 50, image=Registry.get_icon("StoreCoin"))
        canvas.itemconfig(t2, text="Coins")

        canvas.itemconfig(t1, text="Creating Stats Data")
        canvas.itemconfig(t2, text="")

        # Game information values.
        self.texts["score"] = canvas.create_text(55, 50, fill="cyan")
        canvas.itemconfig(t2, text="Score")
        self.texts["level"] = canvas.create_text(110, 50, fill="cyan")
        canvas.itemconfig(t2, text="Level")
        self.texts["speed"] = canvas.create_text(165, 50, fill="cyan")
        canvas.itemconfig(t2, text="Speed")
        self.texts["lives"] = canvas.create_text(220, 50, fill="cyan")
        canvas.itemconfig(t2, text="Lives")

        self.texts["shiptp"] = canvas.create_text(w-20, 10, fill="cyan")
        canvas.itemconfig(t2, text="Teleports")
        self.texts["diamond"] = canvas.create_text(w-20, 30, fill="cyan")
        canvas.itemconfig(t2, text="Diamonds")
        self.texts["coin"] = canvas.create_text(w-20, 50, fill="cyan")
        canvas.itemconfig(t2, text="Coins")
        self.texts["level-view"] = canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"],
                                                      fill='Orange',
                                                      font=Font("Helvetica", 46).get_tuple())
        canvas.itemconfig(t2, text="Level View")

        self.background = CPanel(canvas, 0, 71, "extend", "expand", fill="#00a7a7", outline="#00a7a7")

        self.canvas = canvas

        LoadCompleteEvent.bind(self.on_loadcomplete)
        EffectApplyEvent.bind(self.on_effect_apply)

        bubbles = Registry.saveData["Sprites"]["qbubbles:bubble"]["objects"].copy()
        Registry.saveData["Sprites"]["qbubbles:bubble"]["objects"] = []
        for bubble in bubbles:
            bub = Registry.get_bubble(bubble["ID"])
            pos = bubble["Position"]
            x = pos[0]
            y = pos[1]
            rad = bubble["Attributes"]["radius"]
            spd = bubble["Attributes"]["speed"]
            hlt = bubble["Attributes"]["health"]
            bub_obj = BubbleObject(bub, bub.hardness)
            bub_obj.reload(bubble)
            self._gameobjects.append(bub_obj)
            self._bubbles.append(bub_obj)

        # Create the player, if the player has already been initialized, reload it.
        self.player = DimensionalPlayer()
        if Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Position"]:
            self.player.create(*Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Position"])
            self.player.reload(Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0])
        else:
            self.player.create(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"])
        self._gameobjects.append(self.player)

        print("DimensionalPlayer added")
