import os
from random import Random
from tkinter import Canvas
from typing import Dict, Tuple, Optional, List

from qbubbles.advUtils.time import TimeLength
from qbubbles.bubbleSystem import BubbleSystem
from qbubbles.bubbles import Bubble, BubbleObject
from qbubbles.config import Reader
from qbubbles.effects import AppliedEffect
from qbubbles.events import UpdateEvent, CollisionEvent, KeyPressEvent, KeyReleaseEvent, XInputEvent, \
    MapInitializeEvent, FirstLoadEvent, SaveEvent, LoadCompleteEvent, GameExitEvent, PauseEvent, EffectApplyEvent
from qbubbles.gameIO import printerr
from qbubbles.gui import CPanel, CEffectBarArea
from qbubbles.nzt import NZTFile
from qbubbles.registry import Registry
from qbubbles.sprites import Sprite, Player
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
        bubbleObject, radius, speed = self.get_random_bubble()
        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]

        if x is None:
            x = self.randoms["qbubbles:bubble.x"][0].randint(0 - radius, w + radius)
        if y is None:
            y = self.randoms["qbubbles:bubble.y"][0].randint(0 - radius, h + radius)
        self.create_bubble(x, y, bubbleObject, radius, speed, bubbleObject.maxHealth)

    def get_random_bubble(self) -> Tuple[BubbleObject, float, float]:
        bubble: Bubble = BubbleSystem.random(self.randoms["qbubbles:bubblesystem"][0])
        radius = self.randoms["qbubbles:bubble.radius"][0].randint(bubble.minRadius, bubble.maxRadius)
        speed = self.randoms["qbubbles:bubble.speed"][0].randint(bubble.minSpeed, bubble.maxSpeed)

        max_health = 1
        if hasattr(bubble, "maxHealth"):
            max_health = bubble.maxHealth

        return BubbleObject(bubble, max_health), radius, speed

    def create_bubble(self, x: int, y: int, bubble_object: BubbleObject, radius: float, speed: float, health: float):
        assert type(bubble_object) != type

        bubble_object.create(x=x, y=y, radius=radius, speed=speed, health=health)
        self._bubbles.append(bubble_object)
        self._gameobjects.append(bubble_object)

    def delete_bubble(self, bubble_object: BubbleObject):
        self._bubbles.remove(bubble_object)
        bubble_object.delete()

    def on_update(self, evt: UpdateEvent):
        pass

    # def on_playermotion(self, evt: PlayerMotionEvent):
    #     pass

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
        _gameIO.Logging.info("Gamemap", "Create bubbles because the save is loaded for first time")

        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]
        for i in range(self.maxBubbles):
            self.create_random_bubble()
        Registry.saveData["Game"]["GameMap"]["initialized"] = True
        self.player.teleport(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"])

    def on_mapinit(self, evt: MapInitializeEvent):
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
            bub = Registry.get_bubble(bubble["id"])
            pos = bubble["Position"]
            x = pos[0]
            y = pos[1]
            rad = bubble["radius"]
            spd = bubble["speed"]
            hlt = bubble["health"]
            bub_obj = BubbleObject(bub, bub.hardness)
            self.create_bubble(x, y, bub_obj, rad, spd, hlt)

        self.player = Player()
        if Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Position"]:
            self.player.create(*Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Position"])
            self.player.reload(Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0])
        else:
            self.player.create(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"])
        self._gameobjects.append(self.player)

    def on_pause(self, evt: PauseEvent):
        self._pause = evt.pause

    def on_update(self, evt: UpdateEvent):
        if self._pause:
            return

        if len(self._bubbles) < self.maxBubbles:
            bubbleObject, radius, speed = self.get_random_bubble()
            w = Registry.gameData["WindowWidth"]
            h = Registry.gameData["WindowHeight"]

            x = w + radius
            y = self.randoms["qbubbles:bubble.y"][0].randint(71 + radius, h - radius)
            self.create_bubble(x, y, bubbleObject, radius, speed, bubbleObject.maxHealth)
        self.canvas.itemconfig(self.texts["score"], text=f"{self.player.score}")
        self.canvas.itemconfig(self.texts["level"], text=f"{self.player.get_objectdata()['level']}")
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
        bubbleObject, radius, speed = self.get_random_bubble()
        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]

        if x is None:
            x = self.randoms["qbubbles:bubble.x"][0].randint(0 - radius, w + radius)
        if y is None:
            y = self.randoms["qbubbles:bubble.y"][0].randint(71 + radius, h - radius)
        self.create_bubble(x, y, bubbleObject, radius, speed, bubbleObject.maxHealth)

    def on_loadcomplete(self, evt: LoadCompleteEvent):
        UpdateEvent.bind(self.on_update)
        PauseEvent.bind(self.on_pause)
        # CleanUpEvent.bind(self.on_cleanup)
        GameExitEvent.bind(self.on_gameexit)
        LoadCompleteEvent.unbind(self.on_loadcomplete)
        SaveEvent.bind(self.on_save)
        _gameIO.Logging.info("Gamemap", "Load Complete")

        self.player.activate_events()

    def on_gameexit(self, evt: GameExitEvent):
        _gameIO.Logging.info("Gamemap", "Exiting Game - Game Map")
        UpdateEvent.unbind(self.on_update)
        PauseEvent.unbind(self.on_pause)
        # CleanUpEvent.unbind(self.on_cleanup)
        GameExitEvent.unbind(self.on_gameexit)
        SaveEvent.unbind(self.on_save)

        self._bubbles = []
        self.player.deactivate_events()

    def on_save(self, evt: SaveEvent):
        save_path = f"{Registry.gameData['launcherConfig']['gameDir']}saves/{evt.saveName}"
        return self.save_savedata(save_path)

        # game_data = Registry.saveData["Game"].copy()
        # game_data["GameMap"]["Randoms"] = self.randoms
        # sprites_data = Registry.saveData["Sprites"].copy()
        # sprite_info_data = Registry.saveData["SpriteInfo"].copy()
        #
        # save_path = f"{Registry.gameData['launcherConfig']['gameDir']}saves/{evt.saveName}"
        #
        # game_data_file = NZTFile(f"{save_path}/game.nzt", "w")
        # game_data_file.data = game_data
        # game_data_file.save()
        # game_data_file.close()
        #
        # sprite_info_file = NZTFile(f"{save_path}/spriteinfo.nzt", "w")
        # sprite_info_file.data = sprite_info_data
        # sprite_info_file.save()
        # sprite_info_file.close()
        #
        # os.makedirs(f"{save_path}/sprites/")
        #
        # for sprite in sprites_data.keys():
        #     path = '/'.join(sprite.split(":")[:-1])
        #     os.makedirs(f"{save_path}/sprites/{path}")
        #     sprite_data_file = NZTFile(f"{save_path}/sprites/{sprite.replace(':', '/')}.nzt", "w")
        #     sprite_data_file.data = sprites_data[sprite]
        #     sprite_data_file.save()
        #     sprite_data_file.close()

    def load_savedata(self, path):
        Registry.saveData["SpriteInfo"] = Reader(f"{path}/spriteinfo.nzt").get_decoded()
        Registry.saveData["Sprites"] = {}
        self.maxBubbles = Registry.saveData["SpriteInfo"]["qbubbles:bubble"]["maxAmount"]

        # Get Sprite data
        for sprite_id in Registry.saveData["SpriteInfo"]["Sprites"]:
            sprite_path = sprite_id.replace(":", "/")
            data = Reader(f"{path}/sprites/{sprite_path}.nzt").get_decoded()
            Registry.saveData["Sprites"][sprite_id] = data

    def save_savedata(self, path):
        save_data = Registry.saveData.copy()

        # sprite_data2 = []

        for sprite in Registry.get_sprites():
            save_data["Sprites"][sprite.get_sname()]["objects"] = []
            _gameIO.Logging.debug("GameMapSaving", f"SpriteData: {save_data['Sprites'][sprite.get_sname()]}")
        for sprite in self.get_gameobjects():
            save_data["Sprites"][sprite.get_sname()]["objects"].append(sprite.get_objectdata())
        for sprite in Registry.get_sprites():
            _gameIO.Logging.debug("GameMapSaving", f"SpriteData: {save_data['Sprites'][sprite.get_sname()]}")
        #  = sprite_data2

        game_data = save_data["Game"]
        sprite_info_data = save_data["SpriteInfo"]
        sprite_data = save_data["Sprites"]

        game_data_file = NZTFile(f"{path}/game.nzt", "w")
        game_data_file.data = game_data
        game_data_file.save()
        game_data_file.close()

        sprite_info_file = NZTFile(f"{path}/spriteinfo.nzt", "w")
        sprite_info_file.data = sprite_info_data
        sprite_info_file.save()
        sprite_info_file.close()

        if not os.path.exists(f"{path}/sprites/"):
            os.makedirs(f"{path}/sprites/")

        for sprite in sprite_data.keys():
            sprite_path = '/'.join(sprite.split(":")[:-1])
            if not os.path.exists(f"{path}/sprites/{sprite_path}"):
                os.makedirs(f"{path}/sprites/{sprite_path}", exist_ok=True)
            sprite_data_file = NZTFile(
                f"{path}/sprites/"
                f"{sprite.replace(':', '/')}.nzt",
                "w")
            sprite_data_file.data = sprite_data[sprite]
            sprite_data_file.save()
            sprite_data_file.close()

    def create_savedata(self, path, seed):
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
            "SpriteData": dict(((s.get_sname(), dict_exclude_key("objects", dict(s.get_spritedata()))) for s in Registry.get_sprites()))
        }

        spriteData = dict()
        for sprite in Registry.get_sprites():
            spriteData[sprite.get_sname()] = sprite.get_spritedata().default

        Registry.saveData = {"GameData": game_data, "SpriteInfo": spriteinfo_data, "SpriteData": spriteData}

        bubble_data = {"bub-id": [], "bub-special": [], "bub-action": [], "bub-radius": [], "bub-speed": [],
                       "bub-position": [], "bub-index": [], "key-active": False}

        game_data_file = NZTFile(f"{path}/game.nzt", "w")
        game_data_file.data = game_data
        game_data_file.save()
        game_data_file.close()

        sprite_info_file = NZTFile(f"{path}/spriteinfo.nzt", "w")
        sprite_info_file.data = spriteinfo_data
        sprite_info_file.save()
        sprite_info_file.close()

        os.makedirs(f"{path}/sprites/", exist_ok=True)

        for sprite in spriteData.keys():
            sprite_path = '/'.join(sprite.split(":")[:-1])
            if not os.path.exists(f"{path}/sprites/{sprite_path}"):
                os.makedirs(f"{path}/sprites/{sprite_path}", exist_ok=True)
            sprite_data_file = NZTFile(
                f"{path}/sprites/"
                f"{sprite.replace(':', '/')}.nzt",
                "w")
            sprite_data_file.data = spriteData[sprite]
            sprite_data_file.save()
            sprite_data_file.close()

        game_data_file = NZTFile(f"{path}/bubble.nzt", "w")
        game_data_file.data = bubble_data
        game_data_file.save()
        game_data_file.close()


class DimensionalMap(GameMap):
    def __init__(self):
        super(DimensionalMap, self).__init__()

        self.set_uname("qbubbles:dimensional_map")
        self.maxBubbles = 100
        self.texts = {}
        self.panelTop: Optional[CPanel] = None
        self.tSpecialColor = "#ffffff"
        self.tNormalColor = "#3fffff"

    def init_defaults(self):
        self.add_random("qbubbles:bubblesystem", 4)
        self.add_random("qbubbles:bubblesystem.start_x", 8)
        self.add_random("qbubbles:bubblesystem.start_y", 12)
        self.add_random("qbubbles:bubble.radius", 32)
        self.add_random("qbubbles:bubble.speed", 64)
        self.add_random("qbubbles:bubble.x", 128)
        self.add_random("qbubbles:bubble.y", 256)

    def on_firstload(self, evt: FirstLoadEvent):
        print("Create bubbles because the save is loaded for first time")

        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]
        for i in range(self.maxBubbles):
            self.create_random_bubble()

        Registry.saveData["Game"]["GameMap"]["initialized"] = True
        self.player.teleport(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"])


    def on_mapinit(self, evt: MapInitializeEvent):
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

        self.texts["shiptp"] = canvas.create_text(w - 20, 10, fill="cyan")
        canvas.itemconfig(t2, text="Teleports")
        self.texts["diamond"] = canvas.create_text(w - 20, 30, fill="cyan")
        canvas.itemconfig(t2, text="Diamonds")
        self.texts["coin"] = canvas.create_text(w - 20, 50, fill="cyan")
        canvas.itemconfig(t2, text="Coins")
        self.texts["level-view"] = canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"],
                                                      fill='Orange',
                                                      font=Font("Helvetica", 46).get_tuple())
        canvas.itemconfig(t2, text="Level View")

        self.background = CPanel(canvas, 0, 71, "extend", "expand", fill="#00a7a7", outline="#00a7a7")

        LoadCompleteEvent.bind(self.on_loadcomplete)

        bubbles = Registry.saveData["Sprites"]["qbubbles:bubble"]["objects"].copy()
        Registry.saveData["Sprites"]["qbubbles:bubble"]["objects"] = []
        for bubble in bubbles:
            bub = Registry.get_bubble(bubble["id"])
            pos = bubble["pos"]
            x = pos[0]
            y = pos[1]
            rad = bubble["radius"]
            spd = bubble["speed"]
            hlt = bubble["health"]
            bub_obj = BubbleObject(bub, bub.maxHealth)
            self.create_bubble(x, y, bub_obj, rad, spd, hlt)

        self.player = Player()
        if Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Position"]:
            self.player.create(*Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Position"])
        else:
            self.player.create(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"])
        self._gameobjects.append(self.player)
        self.canvas = canvas

    def on_update(self, evt: UpdateEvent):
        if len(self._bubbles) < self.maxBubbles:
            bubbleObject, radius, speed = self.get_random_bubble()
            w = Registry.gameData["WindowWidth"]
            h = Registry.gameData["WindowHeight"]

            x = w + radius
            y = self.randoms["qbubbles:bubble.y"][0].randint(71 + radius, h - radius)
            self.create_bubble(x, y, bubbleObject, radius, speed, bubbleObject.maxHealth)
        self.canvas.itemconfig(self.texts["score"], text=f"{self.player.score}")
        self.canvas.itemconfig(self.texts["level"], text=f"{self.player.get_objectdata()['level']}")
        self.canvas.itemconfig(self.texts["lives"], text=f"{round(self.player.health, 1)}")
        self.canvas.itemconfig(self.texts["score"], text=f"{self.player.score}")
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
        bubbleObject, radius, speed = self.get_random_bubble()
        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]

        if x is None:
            x = self.randoms["qbubbles:bubble.x"][0].randint(0 - radius, w + radius)
        if y is None:
            y = self.randoms["qbubbles:bubble.y"][0].randint(71 + radius, h - radius)
        self.create_bubble(x, y, bubbleObject, radius, speed, bubbleObject.maxHealth)

    def on_loadcomplete(self, evt: LoadCompleteEvent):
        UpdateEvent.bind(self.on_update)
        # CleanUpEvent.bind(self.on_cleanup)
        GameExitEvent.bind(self.on_gameexit)
        LoadCompleteEvent.unbind(self.on_loadcomplete)
        print("Load Complete")

        self.player.activate_events()

    def on_gameexit(self, evt: GameExitEvent):
        print("Exiting Game - Game Map")
        UpdateEvent.unbind(self.on_update)
        # CleanUpEvent.unbind(self.on_cleanup)
        GameExitEvent.unbind(self.on_gameexit)

        self._bubbles = []
        self.player.deactivate_events()

    def on_save(self, evt: SaveEvent):
        print(f"Saving savedata to {evt.saveName}")

        game_data = Registry.saveData["Game"].copy()
        game_data["GameMap"]["Randoms"] = self.randoms
        sprites_data = Registry.saveData["Sprites"].copy()
        sprite_info_data = Registry.saveData["SpriteInfo"].copy()

        save_path = f"{Registry.gameData['launcherConfig']['gameDir']}saves/{evt.saveName}"

        game_data_file = NZTFile(f"{save_path}/game.nzt", "w")
        game_data_file.data = game_data
        game_data_file.save()
        game_data_file.close()

        sprite_info_file = NZTFile(f"{save_path}/spriteinfo.nzt", "w")
        sprite_info_file.data = sprite_info_data
        sprite_info_file.save()
        sprite_info_file.close()

        os.makedirs(f"{save_path}/sprites/")

        for sprite in sprites_data.keys():
            path = '/'.join(sprite.split(":")[:-1])
            os.makedirs(f"{save_path}/sprites/{path}")
            sprite_data_file = NZTFile(f"{save_path}/sprites/{sprite.replace(':', '/')}.nzt", "w")
            sprite_data_file.data = sprites_data[sprite]
            sprite_data_file.save()
            sprite_data_file.close()

    def load_savedata(self, path):
        Registry.saveData["SpriteInfo"] = Reader(f"{path}/spriteinfo.nzt").get_decoded()
        Registry.saveData["Sprites"] = {}
        self.maxBubbles = Registry.saveData["SpriteInfo"]["qbubbles:bubble"]["maxAmount"]

        # Get Sprite data
        for sprite_id in Registry.saveData["SpriteInfo"]["Sprites"]:
            sprite_path = sprite_id.replace(":", "/")
            data = Reader(f"{path}/sprites/{sprite_path}.nzt").get_decoded()
            Registry.saveData["Sprites"][sprite_id] = data

    def save_savedata(self, path):
        print(f"Saving savedata to {path}")
        
        # saveData = {}
        saveData = Registry.saveData.copy()
        
        for sprite in self.get_gameobjects():
            saveData["Sprites"][sprite.get_sname()]["objects"] = sprite.get_objectdata()

        game_data = saveData["Game"]
        sprite_info_data = saveData["SpriteInfo"]
        sprite_data = saveData["Sprites"]

        game_data_file = NZTFile(f"{path}/game.nzt", "w")
        game_data_file.data = game_data
        game_data_file.save()
        game_data_file.close()

        sprite_info_file = NZTFile(f"{path}/spriteinfo.nzt", "w")
        sprite_info_file.data = sprite_info_data
        sprite_info_file.save()
        sprite_info_file.close()

        if not os.path.exists(f"{path}/sprites/"):
            os.makedirs(f"{path}/sprites/", exist_ok=True)

        for sprite in sprite_data.keys():
            sprite_path = '/'.join(sprite.split(":")[:-1])
            if not os.path.exists(f"{path}/sprites/{sprite_path}"):
                os.makedirs(f"{path}/sprites/{sprite_path}", exist_ok=True)
            sprite_data_file = NZTFile(
                f"{path}/sprites/"
                f"{sprite.replace(':', '/')}.nzt",
                "w")
            sprite_data_file.data = sprite_data[sprite]
            sprite_data_file.save()
            sprite_data_file.close()

    def create_savedata(self, path, seed):
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
            "SpriteData": dict(((s.get_sname(), dict_exclude_key("objects", dict(s.get_spritedata()))) for s in
                                Registry.get_sprites()))
        }

        spriteData = dict()
        for sprite in Registry.get_sprites():
            spriteData[sprite.get_sname()] = sprite.get_spritedata().default

        Registry.saveData = {"GameData": game_data, "SpriteInfo": spriteinfo_data, "SpriteData": spriteData}

        bubble_data = {"bub-id": [], "bub-special": [], "bub-action": [], "bub-radius": [], "bub-speed": [],
                       "bub-position": [], "bub-index": [], "key-active": False}

        game_data_file = NZTFile(f"{path}/game.nzt", "w")
        game_data_file.data = game_data
        game_data_file.save()
        game_data_file.close()

        sprite_info_file = NZTFile(f"{path}/spriteinfo.nzt", "w")
        sprite_info_file.data = spriteinfo_data
        sprite_info_file.save()
        sprite_info_file.close()

        os.makedirs(f"{path}/sprites/", exist_ok=True)

        for sprite in spriteData.keys():
            sprite_path = '/'.join(sprite.split(":")[:-1])
            if not os.path.exists(f"{path}/sprites/{sprite_path}"):
                os.makedirs(f"{path}/sprites/{sprite_path}", exist_ok=True)
            sprite_data_file = NZTFile(
                f"{path}/sprites/"
                f"{sprite.replace(':', '/')}.nzt",
                "w")
            sprite_data_file.data = spriteData[sprite]
            sprite_data_file.save()
            sprite_data_file.close()

        game_data_file = NZTFile(f"{path}/bubble.nzt", "w")
        game_data_file.data = bubble_data
        game_data_file.save()
        game_data_file.close()
