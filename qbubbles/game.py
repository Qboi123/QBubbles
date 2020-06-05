import os
import os
import shutil
from time import sleep

from PIL import ImageGrab, ImageTk, ImageFilter, Image

from qbubbles.ammo import *
from qbubbles.bubble import place_bubble
import qbubbles.bubbles
from qbubbles.components import *
from qbubbles.effects import BaseEffect, AppliedEffect
from qbubbles.events import KeyReleaseEvent, UpdateEvent, KeyPressEvent, XInputEvent, CollisionEvent, \
    MapInitializeEvent, FirstLoadEvent, CleanUpEvent, LoadCompleteEvent, GameExitEvent, PauseEvent, SaveEvent
from qbubbles.gameIO import Logging
from qbubbles.gui import CTransparentButton
from qbubbles.maps import GameMap
from qbubbles.modemanager import ModeManager
from qbubbles.scenemanager import CanvasScene
from qbubbles.special import ScrolledWindow
from qbubbles.sprites import Sprite, Player
from qbubbles.teleport import *
from qbubbles.utils import Maintance, Font

default_launchercfg = {"version": "v1.5.0-pre1",
                       "versionDir": "v1_5_0_pre1",
                       "debug": False}

FatalError = Exception

ModRequirementInvalid = FatalError
ClassRequirementInvalid = ModRequirementInvalid

log = Logging

# log.info("<Root>", "Imports loading success")
# log.info("<Root>", "Starting Game")


def control(modes, config, root, canvas, stats, bubbles, back, texts, commands, temp, panels, fore, ship, tp, lang,
            return_main, icons, bub, font, event, c_ammo, laucher_cfg):
    """
    Ship-motion event
    :param laucher_cfg:
    :param c_ammo:
    :param font:
    :param bub:
    :param icons:
    :param ship:
    :param tp:
    :param lang:
    :param return_main:
    :param commands:
    :param fore:
    :param panels:
    :param temp:
    :param modes:
    :param config:
    :param root:
    :param canvas:
    :param stats:
    :param bubbles:
    :param back:
    :param texts:
    :param event:
    """

    if modes["store"] and commands["store"] is not None:
        if event.keysym == "Up":
            commands["store"].set_selected(canvas, -1)
        if event.keysym == "Down":
            commands["store"].set_selected(canvas, 1)
        if event.keysym == "Left":
            commands["store"].set_selected(canvas, int(-((config["height"] - 215) / 140 + 1)))
        if event.keysym == "Right":
            commands["store"].set_selected(canvas, int((config["height"] - 215) / 140 + 1))
        if event.keysym == "space":
            commands["store"].buy_selected(config, modes, log, root, canvas, stats, bubbles, back,
                                           texts,
                                           commands, temp, panels)
        if event.keysym == "BackSpace":
            commands["store"].exit(canvas, log, modes, stats, temp, commands)
            commands["store"] = None
        if event.keysym == "Escape":
            sleep(1)
            commands["store"].exit(canvas, log, modes, stats, temp, commands)
            commands["store"] = None
    if modes["present"]:
        if event.keysym == "space":
            # noinspection PyDeepBugsBinOperator
            if False != commands["present"] != True:
                commands["present"].exit(canvas)
                modes["pause"] = False
                modes["present"] = False
                stats["scorestate_time"] = temp["scorestate-save"] + time()
                stats["secure_time"] = temp["secure-save"] + time()
                stats["timebreak_time"] = temp["timebreak-save"] + time()
                stats["confusion_time"] = temp["confusion-save"] + time()
                stats["slowmotion_time"] = temp["slowmotion-save"] + time()
                stats["paralyse_time"] = temp["paralyse-save"] + time()
                stats["shotspeed_time"] = temp["shotspeed-save"] + time()
                stats["notouch_time"] = temp["notouch-save"] + time()
    if modes["teleport"]:
        x, y = get_coords(canvas, tp["id1"])
        if event.keysym == 'Up':
            if y > 72 + 5:
                canvas.move(tp["id1"], 0, -5)
                canvas.move(tp["id2"], 0, -5)
                canvas.move(tp["id3"], 0, -5)
                canvas.move(tp["id4"], 0, -5)
        if event.keysym == "Down":
            if y < config["height"] - 105 - 5:
                canvas.move(tp["id1"], 0, 5)
                canvas.move(tp["id2"], 0, 5)
                canvas.move(tp["id3"], 0, 5)
                canvas.move(tp["id4"], 0, 5)
        if event.keysym == "Left":
            if x > 0 + 5:
                canvas.move(tp["id1"], -5, 0)
                canvas.move(tp["id2"], -5, 0)
                canvas.move(tp["id3"], -5, 0)
                canvas.move(tp["id4"], -5, 0)
        if event.keysym == "Right":
            if x < config["width"] - 5:
                canvas.move(tp["id1"], 5, 0)
                canvas.move(tp["id2"], 5, 0)
                canvas.move(tp["id3"], 5, 0)
                canvas.move(tp["id4"], 5, 0)
        if event.keysym == "BackSpace":
            modes["pause"] = False

            stats["scorestate_time"] = temp["scorestate-save"] + time()
            stats["secure_time"] = temp["secure-save"] + time()
            stats["timebreak_time"] = temp["timebreak-save"] + time()
            stats["confusion_time"] = temp["confusion-save"] + time()
            stats["slowmotion_time"] = temp["slowmotion-save"] + time()
            stats["paralyse_time"] = temp["paralyse-save"] + time()
            stats["shotspeed_time"] = temp["shotspeed-save"] + time()
            stats["notouch_time"] = temp["notouch-save"] + time()
        if event.keysym == "Escape":
            modes["pause"] = False

            stats["scorestate_time"] = temp["scorestate-save"] + time()
            stats["secure_time"] = temp["secure-save"] + time()
            stats["timebreak_time"] = temp["timebreak-save"] + time()
            stats["confusion_time"] = temp["confusion-save"] + time()
            stats["slowmotion_time"] = temp["slowmotion-save"] + time()
            stats["paralyse_time"] = temp["paralyse-save"] + time()
            stats["shotspeed_time"] = temp["shotspeed-save"] + time()
            stats["notouch_time"] = temp["notouch-save"] + time()
            sleep(1)
        if event.keysym == "Return":
            modes["pause"] = False

            stats["scorestate_time"] = temp["scorestate-save"] + time()
            stats["secure_time"] = temp["secure-save"] + time()
            stats["timebreak_time"] = temp["timebreak-save"] + time()
            stats["confusion_time"] = temp["confusion-save"] + time()
            stats["slowmotion_time"] = temp["slowmotion-save"] + time()
            stats["paralyse_time"] = temp["paralyse-save"] + time()
            stats["shotspeed_time"] = temp["shotspeed-save"] + time()
            stats["notouch_time"] = temp["notouch-save"] + time()

            stats["teleports"] -= 1
            teleport(canvas, root, stats, modes, ship, tp, tp["id1"])
        if event.keysym.lower() == "space":
            modes["pause"] = False

            stats["scorestate_time"] = temp["scorestate-save"] + time()
            stats["secure_time"] = temp["secure-save"] + time()
            stats["timebreak_time"] = temp["timebreak-save"] + time()
            stats["confusion_time"] = temp["confusion-save"] + time()
            stats["slowmotion_time"] = temp["slowmotion-save"] + time()
            stats["paralyse_time"] = temp["paralyse-save"] + time()
            stats["shotspeed_time"] = temp["shotspeed-save"] + time()
            stats["notouch_time"] = temp["notouch-save"] + time()

            stats["teleports"] -= 1
            teleport(canvas, root, stats, modes, ship, tp, tp["id1"])
    elif event.keysym.lower() == "space":
        a = c_ammo()
        a.create(None, None)
    if event.keysym == "Escape" and (not modes["pause"]) and (not modes["store"]) and (not modes["teleport"]) and \
            (not modes["window"]) and (not modes["present"]) and (not modes["cheater"]):
        modes["pause"] = True

        canvas.delete(icons["pause"])
        if stats["special-level"]:
            temp['pause/bg'] = canvas.create_rectangle(0, 69,
                                                       config["width"],
                                                       config[
                                                           "height"],
                                                       fill="#3f3f3f",
                                                       outline="#3f3f3f")
            temp['pause/toline'] = canvas.create_line(0, 69, config["width"], 69,
                                                      fill="#afafaf")
            # temp['pause/bottom.line'] = canvas.create_line(0, config["height"] - 102, config["width"],
            #                                                config["height"] - 102,
            #                                                fill="#afafaf")

            temp['pause/menu_frame'] = Frame(root, bg="#3f3f3f")
            temp['pause/menu'] = canvas.create_window(config["middle-x"], config["middle-y"] / 2 + 130,
                                                      window=temp['pause/menu_frame'], anchor='n',
                                                      height=20, width=300)

            temp["pause/back-to-menu"] = Button(temp["qbubbles:pause.menu_frame"], text=lang["pause.back-to-home"],
                                                command=lambda: return_main(),
                                                relief="flat", bg="#1f1f1f", fg="#afafaf", font=font)
            back = "#1f1f1f"
            fore = "yellow"
        else:
            temp['pause/bg'] = canvas.create_rectangle(0, 69,
                                                       config["width"],
                                                       config[
                                                           "height"],
                                                       fill="darkcyan",
                                                       outline="darkcyan")
            temp['pause/toline'] = canvas.create_line(0, 69, config["width"], 69,
                                                      fill="#7fffff")
            # temp['pause/bottom.line'] = canvas.create_line(0, config["height"] - 102, config["width"],
            #                                                config["height"] - 102,
            #                                                fill="#7fffff")

            temp['pause/menu_frame'] = Frame(root, bg="darkcyan")
            temp['pause/menu'] = canvas.create_window(config["middle-x"], config["middle-y"] / 2 + 130,
                                                      window=temp['pause/menu_frame'], anchor='n',
                                                      height=500, width=300)

            temp["pause/back-to-menu"] = Button(temp["qbubbles:pause.menu_frame"], text=lang["pause.back-to-home"],
                                                command=lambda: return_main(),
                                                relief="flat", bg="#005f5f", fg="#7fffff", font=[font])

            back = "#005f5f"
            fore = "#7fffff"

        temp["qbubbles:pause.s_frame"] = Frame(root, bg=back)
        temp["qbubbles:pause.s_frame"].place(x=config["middle-x"], y=config["middle-y"] / 2 + 250, anchor='n',
                                             width=1000)

        temp["qbubbles:pause.sw"] = ScrolledWindow(temp["qbubbles:pause.s_frame"], 1020, 321, height=321, width=1000)

        temp["qbubbles:pause.canv"] = temp["qbubbles:pause.sw"].canv
        temp["qbubbles:pause.canv"].config(bg=back)
        temp["qbubbles:pause.sw"].scrollwindow.config(bg=back)

        temp["qbubbles:pause.frame"] = temp["qbubbles:pause.sw"].scrollwindow

        a = ("Normal", "Double", "Kill", "Triple", "SpeedUp", "SpeedDown", "Up", "Ultimate", "DoubleState",
             "Protect", "SlowMotion", "TimeBreak", "Confusion", "HyperMode", "energy_bubble",
             "Coin", "NoTouch", "Paralyse", "Diamond", "StoneBub", "Present", "SpecialKey", "LevelKey")

        canvas = (
            "bubble.normal", "bubble.double", "bubble.kill", "bubble.triple", "bubble.speedup", "bubble.speeddown",
            "bubble.up", "bubble.state.ultimate", "bubble.state.double", "bubble.state.protect",
            "bubble.state.slowmotion",
            "bubble.state.timebreak", "bubble.state.confusion", "bubble.state.hypermode", "bubble.energy_bubble",
            "bubble.coin", "bubble.state.notouch", "bubble.state.paralyse", "bubble.diamond", "bubble.stonebubble",
            "bubble.present", "bubble.state.specialkey", "bubble.levelkey")

        canvass = Canvas(temp["qbubbles:pause.frame"], bg=back, highlightthickness=0)
        x = 50
        y = 50
        temp["pause/bubble.iconss"] = []
        for i in range(len(a)):
            # print(a[i], b[i])
            place_bubble(canvass, bub, x, y, 25, a[i])
            canvass.create_text(x, y + 40, text=lang[canvas[i]], fill=fore, font=[font, 10])
            if x > 900:
                x = 50
                y += 100
            else:
                x += 100

        canvass.config(height=y + 70, width=1000)
        canvass.pack(fill="y")

        temp["pause/back-to-menu"].pack(fill="x")

        icons["pause"] = canvas.create_image(config["middle-x"], config["middle-y"] / 2,
                                             image=icons["pause-id"])

        canvas.itemconfig(texts["pause"], text="")
        root.update()

        temp["scorestate-save"] = stats["scorestate_time"] - time()
        temp["secure-save"] = stats["secure_time"] - time()
        temp["timebreak-save"] = stats["timebreak_time"] - time()
        temp["confusion-save"] = stats["confusion_time"] - time()
        temp["slowmotion-save"] = stats["slowmotion_time"] - time()
        temp["paralyse-save"] = stats["paralyse_time"] - time()
        temp["shotspeed-save"] = stats["shotspeed_time"] - time()
        temp["notouch-save"] = stats["notouch_time"] - time()
        temp["special-level-save"] = stats["special-level_time"] - time()
    elif event.keysym == "Escape" and modes["pause"] and (not modes["store"]) and (not modes["teleport"]) and \
            (not modes["window"]) and (not modes["present"]) and (not modes["cheater"]):
        modes["pause"] = False

        canvas.itemconfig(icons["pause"], state="hidden")
        canvas.itemconfig(texts["pause"], text="")

        temp["pause/back-to-menu"].destroy()
        temp['pause/menu_frame'].destroy()
        temp["qbubbles:pause.s_frame"].destroy()

        canvas.delete(temp['pause/toline'])
        # canvas.delete(temp['pause/bottom.line'])
        canvas.delete(temp['pause/menu'])
        canvas.delete(temp['pause/bg'])

        root.update()

        stats["scorestate_time"] = temp["scorestate-save"] + time()
        stats["secure_time"] = temp["secure-save"] + time()
        stats["timebreak_time"] = temp["timebreak-save"] + time()
        stats["confusion_time"] = temp["confusion-save"] + time()
        stats["slowmotion_time"] = temp["slowmotion-save"] + time()
        stats["paralyse_time"] = temp["paralyse-save"] + time()
        stats["shotspeed_time"] = temp["shotspeed-save"] + time()
        stats["notouch_time"] = temp["notouch-save"] + time()
    if event.keysym == "t" and stats["teleports"] > 0 and (not modes["teleport"]):
        modes["pause"] = True

        temp["scorestate-save"] = stats["scorestate_time"] - time()
        temp["secure-save"] = stats["secure_time"] - time()
        temp["timebreak-save"] = stats["timebreak_time"] - time()
        temp["confusion-save"] = stats["confusion_time"] - time()
        temp["slowmotion-save"] = stats["slowmotion_time"] - time()
        temp["paralyse-save"] = stats["paralyse_time"] - time()
        temp["shotspeed-save"] = stats["shotspeed_time"] - time()
        temp["notouch-save"] = stats["notouch_time"] - time()
        temp["special-level-save"] = stats["special-level_time"] - time()

        modes["teleport"] = True

        tp_mode(canvas, config, stats, modes, tp)
    if event.keysym.lower() == "e" and (not modes["store"]):
        modes["pause"] = True
        temp["scorestate-save"] = stats["scorestate_time"] - time()
        temp["secure-save"] = stats["secure_time"] - time()
        temp["timebreak-save"] = stats["timebreak_time"] - time()
        temp["confusion-save"] = stats["confusion_time"] - time()
        temp["slowmotion-save"] = stats["slowmotion_time"] - time()
        temp["paralyse-save"] = stats["paralyse_time"] - time()
        temp["shotspeed-save"] = stats["shotspeed_time"] - time()
        temp["notouch-save"] = stats["notouch_time"] - time()
        temp["special-level-save"] = stats["special-level_time"] - time()
        modes["store"] = True
        log.debug("bub_move", "Creating Store() to variable \"store\"")
        log.debug("bub_move", "storemode=" + str(modes["store"]))
        # # TODO: Change to Store-scene instead of creating a Store instance
        # commands["store"] = Store(canvas, log, config, modes, stats, icons, fore, font, laucher_cfg)
    # if event.char == "/":
    #     CheatEngine().event_handler(canvas, modes, stats, config, temp, log, backgrounds, bubble, event, bub)
    # if modes["cheater"]:
    #     CheatEngine().input_event_handler(canvas, log, stats, backgrounds, bubble, event, config, bub, temp,
    #                                       modes)

    if event.keysym == "Escape":
        s.save()
    root.update()


# noinspection PyUnusedLocal,PyArgumentList,PyCallByClass,PyAttributeOutsideInit
class Game(CanvasScene):
    def __init__(self):
        super().__init__(Registry.get_window("default"))

        # Start variables for the game
        self.texts = {}
        self.pauseIcon: Optional[PhotoImage] = None
        self.modeManager = ModeManager()
        # self.log = log
        self.returnmain = False

        # Startup
        self.root: Tk = Registry.get_window("default")
        self.time1: float = Registry.gameData["startTime"]
        self.maintance: Maintance = Maintance()
        self.saveName: Optional[str] = None

        # Stats
        Registry.saveData = dict()
        self.xControl = dict()

        # Standard Temporaray variables
        self.temp: Dict[str, Any] = dict()
        self.temp["scorestate-save"] = 0
        self.temp["secure-save"] = 0
        self.temp["timebreak-save"] = 0
        self.temp["confusion-save"] = 0
        self.temp["slowmotion-save"] = 0
        self.temp["paralyse-save"] = 0
        self.temp["shotspeed-save"] = 0
        self.temp["notouch-save"] = 0
        self.temp["special-level-save"] = 0
        self.temp["found-bubble"] = False

        # XInput pressed dpad buttons
        self.pressed = {"Up": False,
                        "Down": False,
                        "Left": False,
                        "Right": False,
                        }

        self._pauseMode = False

        # self.gameMap.player: Optional[Player] = None

    # noinspection PyAttributeOutsideInit
    def show_scene(self, save_name):  # , save_data: Dict[str, Union[List, Dict[Any, Any], str, int, bool, float]]):
        super(Game, self).show_scene()

        Logging.info("GameScene", f"Started Game()-scene on saved game with name {repr(save_name)}")

        # Initialize save-data
        self.saveName = save_name

        # noinspection PyDictCreation
        self.commands = {"store": False, "present": False, "special-mode": False}
        self.commands["store"]: Union[bool, Store] = False
        self.commands["present"]: Union[bool, Present] = False
        self.commands["special-mode"]: Union[bool, SpecialMode] = False

        # self.gameMap.player = Player()

        # self.tp = TPSprite()  # TODO: Make support for TPSprite(...) object in './sprites.py'. When done, uncomment.

        # # TODO: Replace Ammo id-dict with classes loaded in ./load.py using ./ammoTypes.py, ./ammo.py, ./sprites.py
        # # Ammo id-dictionary
        # self.ammo = {"ammo-id": list(), "ammo-radius": 5, "ammo-speed": list(), "ammo-position": list(),
        #              "ammo-damage": list(), "retime": Registry.gameData["startTime"]}

        self.run(save_name)

        # # Saved game data event, and regiser save-data
        # Registry.saveData = save_data
        # SavedataReadedEvent(Registry.saveData)

    def options(self):
        pass

    def run(self, save_name):
        # Getting save-name and copy this in the self.
        self.saveName = save_name

        gamedir = Registry.gameData['launcherConfig']['gameDir']

        # Reload stats with the reader.
        Registry.saveData["Game"] = Reader(f"{gamedir}saves/{self.saveName}/game.dill").get_decoded()

        # Game Maps
        gamemap = Registry.get_gamemap(Registry.saveData["Game"]["GameMap"]["id"])
        gamemap.load_savedata(f"{gamedir}saves/{self.saveName}")

        # Log
        Logging.info("GameScene", f"Saved data is loaded, game map uname is '{Registry.saveData['Game']['GameMap']['id']}'")

        # Run the main method (function).
        self.main()

    @staticmethod
    def on_resize(event):
        if "--travis" in sys.argv:
            return
        return

    def return_main(self):
        """
        Return to title screen
        :return:
        """

        # Returning to title menu.
        self.canvas.destroy()
        self.canvas = Canvas(self.frame, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Summon game exit event.
        GameExitEvent(self, self.saveName)

        # Wipe savedata from memory
        Registry.saveData = []

        # Change Scene
        self.scenemanager.change_scene("qbubbles:title")

    def on_keyrelease(self, evt: KeyReleaseEvent):
        """
        TODO: Rename method to on_keyrelease
        Key-release event, called when user stops pressing a key on the keyboard
        :param evt:
        :return:
        """
        if evt.char.lower() == "e":
            pass  # TODO: Change here to the inventory scene (when created)
        if evt.char.lower() == "r":
            # self._pauseMode = True
            # PauseEvent(self, self.canvas, self.temp, True)
            # self.scenemanager.change_scene("qbubbles:store")
            pass  # TODO: Implement to change to Store()-scene, when possible.
        if evt.keySym.lower() == "esc" or evt.keySym.lower() == "escape":
            if self._pauseMode is False:
                self.pause()  # FIXME: Create pause-menu
            elif self._pauseMode is True:
                self.unpause()  # FIXME: Destroy pause-menu
            else:
                raise ValueError("Pause mode must be True or False")
        # Logging.debug("KeyReleaseEvent", f"Key Released: {evt.keySym}")

    def pause(self):
        from PIL import ImageGrab, ImageTk, ImageFilter, Image

        # TODO: Create pause menu here, set game to pause and call PauseEvent(...)
        self._pauseMode = True

        root = Registry.get_window("default")

        font = Font("Helvetica", 10)

        blurim = ImageGrab.grab((0, 70, Registry.gameData["WindowWidth"], Registry.gameData["WindowHeight"]), True)
        blurim2 = blurim.filter(ImageFilter.GaussianBlur(20))
        blurimtk = ImageTk.PhotoImage(blurim2)
        bubviewback = Image.new("RGBA", (Registry.gameData["WindowWidth"], 650), "#0000003f")
        bubviewbacktk = ImageTk.PhotoImage(bubviewback)

        self.root.update()
        # im.show()
        # im = im.crop((0, 70, Registry.gameData["WindowWidth"], Registry.gameData["WindowHeight"]))

        if self.pauseIcon is not None:
            self.canvas.delete(self.pauseIcon)  # Registry.get_icon("pause"))
        if self.modeManager.currentModeName == "specialLevel":
            # self.temp["qbubbles:pause.bg"] = self.canvas.create_rectangle(
            #     0, 69, Registry.gameData["WindowWidth"], Registry.gameData["WindowHeight"],
            #     fill="#3f3f3f", outline="#3f3f3f")
            self.temp["qbubbles:pause.bg"] = self.canvas.create_image(0, 70, image=blurimtk, anchor="nw")
            self.temp["qbubbles:pause.to_line"] = self.canvas.create_line(
                0, 69, Registry.gameData["WindowWidth"], 69, fill="#afafaf")
            # self.temp["qbubbles:pause.menu_frame"] = Frame(
            #     root, bg="#000001")
            # self.temp["qbubbles:pause.menu_canvas"] = Canvas(
            #     root, bg="#000001")
            # self.temp['qbubbles:pause.menu'] = self.canvas.create_window(
            #     Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] / 2 + 130,
            #     window=self.temp['qbubbles:pause.menu_frame'], anchor='n', height=20, width=300)
            self.temp["qbubbles:pause.back_to_menu"] = CTransparentButton(
                self.canvas, Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] / 2 + 150, 32, 300,
                text=Registry.gameData["language"]["pause.back-to-home"],
                command=lambda: self.return_main(), font=font.get_tuple())
            back = "tran"
            fore = "yellow"
        else:
            # self.temp["qbubbles:pause.bg"] = self.canvas.create_rectangle(
            #     0, 69, Registry.gameData["WindowWidth"], Registry.gameData["WindowHeight"],
            #     fill="#000001", outline="#000001")
            self.temp["qbubbles:pause.bg"] = self.canvas.create_image(0, 70, image=blurimtk, anchor="nw")
            self.temp["qbubbles:pause.to_line"] = self.canvas.create_line(
                0, 69, Registry.gameData["WindowWidth"], 69, fill="#7fffff")
            # self.temp['pause/bottom.line'] = self.canvas.create_line(0, config["height"] - 102, config["width"],
            #                                                config["height"] - 102,
            #                                                fill="#7fffff")

            # self.temp["qbubbles:pause.menu_frame"] = Frame(root, bg="#000001")
            # self.temp["qbubbles:pause.menu"] = self.canvas.create_window(
            #     Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] / 2 + 130,
            #     window=self.temp['qbubbles:pause.menu_frame'], anchor='n', height=500, width=300)

            self.temp["qbubbles:pause.back_to_menu"] = CTransparentButton(
                self.canvas, Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] / 2 + 150, 32, 300,
                text=Registry.gameData["language"]["pause.back-to-home"],
                command=lambda: self.return_main(), relief="flat", bg="#005f5f", fg="#7fffff", font=font.get_tuple())

            back = "#00a7a7"
            fore = "#7fffff"

        s_frame = self.temp["qbubbles:pause.s_frame"] = Frame(root, bg=back)

        # self.temp["qbubbles:pause.s_frame"].place(
        #     x=Registry.gameData["MiddleX"], y=Registry.gameData["MiddleY"] / 2 + 250, anchor='n', width=1000)
        # self.temp["qbubbles:pause.sw"] = ScrolledWindow(
        #     self.temp["qbubbles:pause.s_frame"], 1020, 321, height=321, width=1000)
        #
        # self.temp["qbubbles:pause.canv"] = self.temp["qbubbles:pause.sw"].canv
        # self.temp["qbubbles:pause.canv"].config(bg=back)
        # canv = self.temp["qbubbles:pause.canv"]
        # # canv: Canvas
        # # self.temp["qbubbles:pause.canvblurim"] = canv.create_image(
        # #     0 - canv.winfo_x(), 70 - canv.winfo_y(), image=blurimtk, anchor='nw')
        # self.temp["qbubbles:pause.sw"].scrollwindow.config(bg=back)
        #
        # self.temp["qbubbles:pause.frame"] = self.temp["qbubbles:pause.sw"].scrollwindow
        #
        # a = ("Normal", "Double", "Kill", "Triple", "SpeedUp", "SpeedDown", "Up", "Ultimate", "DoubleState",
        #      "Protect", "SlowMotion", "TimeBreak", "Confusion", "HyperMode", "energy_bubble",
        #      "Coin", "NoTouch", "Paralyse", "Diamond", "StoneBub", "Present", "SpecialKey", "LevelKey")
        #
        # c = ("bubble.normal", "bubble.double", "bubble.kill", "bubble.triple", "bubble.speedup", "bubble.speeddown",
        #      "bubble.up", "bubble.state.ultimate", "bubble.state.double", "bubble.state.protect",
        #      "bubble.state.slowmotion",
        #      "bubble.state.timebreak", "bubble.state.confusion", "bubble.state.hypermode", "bubble.energy_bubble",
        #      "bubble.coin", "bubble.state.notouch", "bubble.state.paralyse", "bubble.diamond", "bubble.stonebubble",
        #      "bubble.present", "bubble.state.specialkey", "bubble.levelkey")
        #
        # canvass = Canvas(self.temp["qbubbles:pause.frame"], bg=back, highlightthickness=0)
        x = 50
        y = Registry.gameData["MiddleY"] / 2 + 350
        self.bubviewbacktk = bubviewbacktk
        self.temp["qbubbles:pause.bubbleviewback"] = self.canvas.create_image(
            0, Registry.gameData["MiddleY"] / 2 + 300, image=bubviewbacktk, anchor="nw")

        # x17 = Registry.gameData["MiddleX"]
        # y17 = Registry.gameData["MiddleY"] / 2 + 250
        # print(x17, y17)
        # # print(s_frame.winfo_y())
        # # x18 = -(x17 / 2)
        # # y18 = -(y17) + 70  #  (-y17 + 70)+y17/2
        # # x18 = -(x17)
        # # y18 = -(y17)
        # # print(x18, y18)
        # # self.temp["qbubbles:pause.canvblurim"] = canv.create_image(x18, y18, image=blurimtk, anchor='nw')
        self.temp["qbubbles:pause.bubble.icons"] = []
        self.temp["qbubbles:pause.bubble.texts"] = []
        bubbles: List[qbubbles.bubbles.Bubble] = Registry.get_bubbles()
        for i in range(len(bubbles)):
            # print(a[i], b[i])
            uname = bubbles[i].get_uname()
            bubble_icon = Registry.get_texture("qbubbles:bubble", uname, radius=50)
            # bubble_icon = Registry.get_texture("sprites", uname, "images")[50]
            self.temp["qbubbles:pause.bubble.icons"].append(
                self.canvas.create_image(
                    x, y, image=bubble_icon, tags=("BubbleView",)
                )
            )
            print(x, y + 40, Registry.get_lname("bubble", uname.replace(":", "."), "name"), fore, font)

            lname = Registry.get_lname("bubble", uname.replace(":", "."), "name")
            # name = Registry.gameData["language"][lname] if lname in Registry.gameData["language"].keys() else lname
            name = lname

            self.temp["qbubbles:pause.bubble.texts"].append(
                self.canvas.create_text(
                    x, y + 40, text=name, fill=fore, font=font.get_tuple(), tags=("BubbleView",)
                )
            )
            # place_bubble(canvass, bub, x, y, 25, a[i])

            if x > (Registry.gameData["WindowWidth"] - 150):
                x = 50
                y += 100
            else:
                x += 100

        canvg_h = y + 70

        if canvg_h < 321:
            canvg_h = 321

        # canvass.config(height=canvg_h, width=1000)
        # canvass.pack(fill="y")

        self.temp["qbubbles:pause.canvass"] = None
        # self.temp["qbubbles:pause.back_to_menu"].pack(fill="x")

        self.temp["qbubbles:pause.icon_id"] = self.canvas.create_image(
            Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] / 2, image=Registry.get_icon("Pause"))

        self.canvas.itemconfig(self.texts["pause"], text="")  # TODO: Remove the use of pause-text
        root.update()

        PauseEvent(self, self.canvas, self.temp, pause=True)
        SaveEvent(self, self.saveName)

        # self.temp["qbubbles:pause.bg"] = self.canvas.create_image(0, 70, image=blurimtk, anchor="nw")
        self.blurimage = blurimtk

        self.blurimageupdate = True
        UpdateEvent.bind(self.on_updateblurimage)

    def on_updateblurimage(self, evt: UpdateEvent):
        if self.blurimageupdate:
            pass
            # self.temp["qbubbles:pause.bg"] = self.canvas.create_image(0, 70, image=self.blurimage, anchor="nw")
            # canv = self.temp["qbubbles:pause.canvass"]
            # self.temp["qbubbles:pause.canvblurim"] = canv.create_image(
            #     0 - canv.winfo_x(), 70 - canv.winfo_y(), image=self.blurimage, anchor='nw')

    def unpause(self):
        """
        Unpauses the game.
        TODO: Remove Bubble view and Bubble view background, when unpausing.

        :return:
        """

        self._pauseMode = False

        # self.canvas.itemconfig(icons["pause"], state="hidden")
        # canvas.itemconfig(texts["pause"], text="")

        self.temp["qbubbles:pause.back_to_menu"].delete()
        # self.temp['qbubbles:pause.menu_frame'].destroy()
        # self.temp["qbubbles:pause.s_frame"].destroy()

        self.blurimageupdate = False
        UpdateEvent.unbind(self.on_updateblurimage)

        self.canvas.delete(self.temp["qbubbles:pause.bubbleviewback"])
        self.canvas.delete(self.temp["qbubbles:pause.icon_id"])
        self.canvas.delete(self.temp['qbubbles:pause.to_line'])
        # canvas.delete(temp['pause/bottom.line'])
        # self.canvas.delete(self.temp['qbubbles:pause.menu'])
        self.canvas.delete(self.temp['qbubbles:pause.bg'])

        self.canvas.delete("BubbleView")

        self.root.update()

        PauseEvent(self, self.canvas, self.temp, pause=False)

        # # Remove stats restore, it's unused.
        # stats["scorestate_time"] = temp["scorestate-save"] + time()
        # stats["secure_time"] = temp["secure-save"] + time()
        # stats["timebreak_time"] = temp["timebreak-save"] + time()
        # stats["confusion_time"] = temp["confusion-save"] + time()
        # stats["slowmotion_time"] = temp["slowmotion-save"] + time()
        # stats["paralyse_time"] = temp["paralyse-save"] + time()
        # stats["shotspeed_time"] = temp["shotspeed-save"] + time()
        # stats["notouch_time"] = temp["notouch-save"] + time()

    def on_tkkeypress(self, event):
        """
        TODO: Add custom key-events using Registry.get_keybindings("press", ...)
        TODO: Make auto-update events
        :return:
        """
        # print(f"PRESS: {event.char}")

        KeyPressEvent(self, event)

    def on_tkkeyrelease(self, event):
        """
        TODO: Add custom key-events using Registry.get_keybindings("press", ...)
        TODO: Make auto-update events
        :return:
        """
        # print(f"RELEASE: {event.char}")

        KeyReleaseEvent(self, event)

    # noinspection PyAttributeOutsideInit
    def movent_change(self):
        """
        TODO: Remove Game.movement_change(...)
        Movement change thread
        :return:
        """

        time2 = time()
        while not self.returnmain:
            time1 = time()

            try:
                # print(time1 - time2)
                # print(1/(time1 - time2))
                self.move_fps = 1 / (time1 - time2)
            except ZeroDivisionError:
                self.move_fps = 1
            time2 = time()
            Thread(None, lambda: self.on_keypress()).start()
            sleep(0.01)

    def _xbox_input(self):
        """
        TODO: Use Registry.get_xboxbinding(...) to check if the event is used
        TODO: Call the XInputEvent(...) here (to update and call event handlers)
        xinput handlers
        :return:
        """

        XInputEvent(self)

        # # TODO: Remove this unused s###
        # time2 = time()
        # while not self.returnmain:
        #     self.xbox.update()
        #     a = [int(self.xbox.LeftJoystickX * 7), int(self.xbox.LeftJoystickY * 7)]
        #     b = [int(self.xbox.RightJoystickX * 7), int(self.xbox.RightJoystickY * 7)]
        #     self.xControl["LeftJoystick"] = a
        #     self.xControl["RightJoystick"] = b
        #     self.xControl["A"] = bool(self.xbox.A)
        #     self.xControl["B"] = bool(self.xbox.B)
        #     self.xControl["X"] = bool(self.xbox.X)
        #     self.xControl["Y"] = bool(self.xbox.Y)
        #     self.xControl["Start"] = bool(self.xbox.Start)
        #     self.xControl["Back"] = bool(self.xbox.Back)
        #     self.xControl["LeftBumper"] = bool(self.xbox.LeftBumper)
        #     self.xControl["RightBumper"] = bool(self.xbox.RightBumper)
        #     self.xControl["LeftTrigger"] = int((self.xbox.LeftBumper + 1) / 2 * 7)
        #     self.xControl["RightTrigger"] = int((self.xbox.RightBumper + 1) / 2 * 7)

    def xboxDeamon(self):
        """
        TODO: Use events for xinput (xbox) events
        TODO: Remove Game.xboxDeamon(...)
        XInput update thread
        :return:
        """

        time2 = time()
        while not self.returnmain:
            time1 = time()

            try:
                # print(time1 - time2)
                # print(1/(time1 - time2))
                self.move_fps = 1 / (time1 - time2)
            except ZeroDivisionError:
                self.move_fps = 1
            time2 = time()
            Thread(None, lambda: self.xMovent()).start()
            sleep(0.01)

    def xMovent(self):
        """
        FIXME: Use XInputEvent(...) instead of Game.xMovent(...)
        TODO: Use XInputEvent(...) in the sprite class, or gui class

        Movement for xinput
        :return:
        """

        if self.modeManager.currentModeName == "present":  # self.modes["present"]:
            if self.xControl["A"]:
                # noinspection PyDeepBugsBinOperator,PyDeepBugsBinOperand
                if False != self.commands["present"] != True:
                    self.commands["present"].exit(self.canvas)
                    self._pauseMode = False
                    self.modes["present"] = False
                    Registry.saveData["Effects"]["scorestate_time"] = self.temp["scorestate-save"] + time()
                    Registry.saveData["Effects"]["secure_time"] = self.temp["secure-save"] + time()
                    Registry.saveData["Effects"]["timebreak_time"] = self.temp["timebreak-save"] + time()
                    Registry.saveData["Effects"]["confusion_time"] = self.temp["confusion-save"] + time()
                    Registry.saveData["Effects"]["slowmotion_time"] = self.temp["slowmotion-save"] + time()
                    Registry.saveData["Effects"]["paralyse_time"] = self.temp["paralyse-save"] + time()
                    Registry.saveData["Effects"]["shotspeed_time"] = self.temp["shotspeed-save"] + time()
                    Registry.saveData["Effects"]["notouch_time"] = self.temp["notouch-save"] + time()

        if (self.modeManager.currentModeName != "teleport") and (self.modeManager.currentModeName != "store") and (
                self.modeManager.currentModeName != "window"):
            if not self._pauseMode:
                if not Registry.saveData["Effects"]["paralyse"]:
                    x, y = get_coords(self.canvas, self.gameMap.player.id)
                    if Registry.saveData["Effects"]["speedboost"]:
                        a = 6
                    else:
                        a = 1

                    self.canvas.move(self.gameMap.player.id,
                                     (Registry.saveData["shipspeed"] / (self.move_fps / 4) + a) * self.xControl[
                                         "LeftJoystick"][0] / 7,
                                     -((Registry.saveData["shipspeed"] / (self.move_fps / 4) + a) * self.xControl[
                                         "LeftJoystick"][1] / 7))

    def shot(self, event):
        # TODO: Remove Game.shot(...) and use on_keyrelease- or on_keypress-events
        # TODO: Use Ammo(...) subclasses for ammo shooting
        if (not self.modeManager.currentMode == "teleport") and (not self.modes["store"]) and (
                not self.modes["window"]):
            if not self._pauseMode:
                if not Registry.saveData["Effects"]["paralyse"]:
                    if event.keysym == "space":
                        # noinspection PyTypeChecker
                        create_shot(self.canvas, self.ammo, self.config, self.ship, Registry.saveData)

    def on_autosave(self):
        # TODO: Use events for Game.on_autosave like AutoSaveEvent(...)
        while not self.returnmain:
            Maintance.auto_save(self.saveName, Registry.saveData)
            print(self.returnmain)
            sleep(2)

    def on_update(self, evt: UpdateEvent):
        if not self._pauseMode:
            self.canvas.tag_raise(self.gameMap.player.id)

        # TODO: Check if collision is needed in pause mode, and if so remove the if statement below.
        if self._pauseMode:
            return

        for index1 in range(len(self.gameMap.get_gameobjects())):
            for index2 in range(index1, len(self.gameMap.get_gameobjects())):
                if index1 != index2:
                    game_obj1: Sprite = self.gameMap.get_gameobjects()[index1]
                    game_obj2: Sprite = self.gameMap.get_gameobjects()[index2]
                    if game_obj1 != game_obj2:
                        # print(f"DISTANCE: {gameObj1.distance(gameObj2)}")
                        # print(f"DISTANCE CALC: {gameObj1.radius + gameObj2.radius}")
                        # if type(gameObj1) != Player:
                        #     print(gameObj1.baseRadius)
                        # elif type(gameObj2) != Player:
                        #     print(gameObj2.baseRadius)
                        if game_obj1.allowCollision is True and game_obj2.allowCollision is True:
                            if game_obj1.distance(game_obj2) < (game_obj1.baseRadius + game_obj2.baseRadius):
                                CollisionEvent(self, game_obj1, game_obj2, self.canvas)
                                CollisionEvent(self, game_obj2, game_obj1, self.canvas)
        # UpdateEvent(self, 0, self.canvas)

    # noinspection PyTypeChecker,PyShadowingNames
    def main(self):
        load_desc_font = Font("Helvetica", 13)
        load_title_font = Font("Helvetica", 46, "bold")

        t0 = self.canvas.create_rectangle(0, 0, Registry.gameData["WindowWidth"], Registry.gameData["WindowHeight"],
                                          fill="#3f3f3f",
                                          outline="#3f3f3f")
        t1 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] - 30,
                                     text="Loading...",
                                     font=load_title_font.get_tuple(), fill="#afafaf")
        t2 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] + 20,
                                     text="Loading Mods",
                                     font=load_desc_font.get_tuple(), fill="#afafaf")
        self.canvas.update()

        Logging.info("GameScene", "Initialize game environment")

        # self.gameMap.player.create(7.5, 7.5)

        # # TODO: Remove when unneeded, i.e. when using gamemaps instead of internal in GameMain.
        # ship_position = Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Position"]

        self.canvas.itemconfig(t1, text="Creating Stats objects")
        self.canvas.itemconfig(t2, text="")

        self.gameMap: GameMap = Registry.get_gamemap(Registry.saveData["Game"]["GameMap"]["id"])
        self.gameMap.load()
        MapInitializeEvent(self, t1, t2, self.saveName)

        self.texts["pause"] = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"],
                                                      fill='Orange',
                                                      font=Font("Helvetica", 56, "bold").get_tuple())
        self.canvas.itemconfig(t2, text="Pauze")
        self.canvas.itemconfig(t2, text="Pauze")

        # Binding key-events for control
        self.canvas.itemconfig(t1, text="Binding Objects")
        self.canvas.itemconfig(t2, text="Main Binding")

        self.canvas.bind_all("<KeyPress>", self.on_tkkeypress)
        self.canvas.bind_all("<KeyRelease>", self.on_tkkeyrelease)
        self.canvas.focus_set()

        self.canvas.itemconfig(t2, text="Player Motion")
        # self.gameMap.player.activate_events()

        stats = Registry.saveData

        self.canvas.itemconfig(t1, text="Reapply effects to player")
        self.canvas.itemconfig(t2, text="")

        # for effectdata in Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Effects"]:
        #     effect: BaseEffect = Registry.get_effect(effectdata["id"])
        #     appliedEffect: AppliedEffect = AppliedEffect(effect, self, effectdata["duration"], effectdata["strength"])
        #     self.gameMap.player.appliedEffects.append(appliedEffect)
        #     self.gameMap.player.appliedEffectTypes.append(effect)
        if Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Attributes"]["score"] < 0:
            log.error("Game.main", "The 'Score' variable under zero.")
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Attributes"]["score"] = 0
        if Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Attributes"]["score"] > Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Attributes"]["highScore"]:
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Attributes"]["highScore"] = Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Attributes"]["score"]

        Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["keyactive"] = True

        # Logging.debug("GameScene", f"GameMap is Initalized: {Registry.saveData['Game']['GameMap']['initialized']}")

        if Registry.saveData["Game"]["GameMap"]["initialized"] is False:
            FirstLoadEvent(self, t1, t2, self.saveName)
            gameDir = Registry.gameData["launcherConfig"]["gameDir"]
            self.gameMap.save_savedata(f"{gameDir}saves/{self.saveName}")

        height = Registry.gameData["WindowHeight"]
        width = Registry.gameData["WindowWidth"]

        self.canvas = self.canvas

        self.canvas.delete(t0)
        self.canvas.delete(t1)
        self.canvas.delete(t2)

        UpdateEvent.bind(self.on_update)
        LoadCompleteEvent(self, self.saveName)
        KeyReleaseEvent.bind(self.on_keyrelease)
        # KeyPressEvent.bind(self.on_keypress)  # Fixme: Add On Key Press event handler to game.

        Logging.info("GameScene", "Save loaded successfully, starting mainloop.")

        t1 = time()

        # Do you know the comment below is there about more than 4 years? Already on the begginings of the code.
        # MAIN GAME LOOP
        while self.gameMap.player.health > 0:
            delta_time = time() - t1
            t1 = time()
            UpdateEvent(self, delta_time, self.canvas)
            CleanUpEvent(self)
            self.root.update()
            self.root.update_idletasks()

        image = ImageGrab.grab(
            (0, 0, self.root.tkScale(Registry.get_window("fake").winfo_screenwidth()), self.root.tkScale(Registry.get_window("fake").winfo_screenheight())),
            True
        )
        tkimage = ImageTk.PhotoImage(image)
        cimage = self.canvas.create_image(0, 0, image=tkimage, anchor="nw")
        ims = []
        tkims = []
        for i in range(1, 21):
            im = image.copy()
            ims.append(im.filter(ImageFilter.GaussianBlur(radius=i)))
            tkims.append(ImageTk.PhotoImage(ims[-1]))
        for tkimage in tkims:
            self.canvas.itemconfig(cimage, image=tkimage)
            # cimage.config(image=tkimage)
            # sleep(0.1)
            self.root.update()
            self.root.update_idletasks()

        # raise NotImplementedError("Game Over is not implemented")
        g1 = self.canvas.create_text(
            Registry.gameData["MiddleX"], Registry.gameData["MiddleY"], text='GAME OVER', fill='Red',
            font=('Helvetica', 60, "bold"))
        g2 = self.canvas.create_text(
            Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] + 60,
            text='Score: ' + str(self.gameMap.player.score), fill='white',
            font=('Helvetica', 30))
        g3 = self.canvas.create_text(
            Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] + 90,
            text='Level: ' + str(Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Attributes"]["level"]), fill='white', font=('Helvetica', 30))
        log.info("Game.main", "Game Over!")
        self.root.update()
        for i in range(40):
            self.root.update()
            self.root.update_idletasks()
            sleep(0.1)
        for gameObject in self.gameMap.get_gameobjects().copy():
            gameObject.delete()
            self.gameMap.get_gameobjects().remove(gameObject)

        self.canvas.delete(g1)
        self.canvas.delete(g2)
        self.canvas.delete(g3)
        del g1, g2, g3
        # Maintance().reset(self.saveName)
        gameDir = Registry.gameData["launcherConfig"]["gameDir"]
        shutil.rmtree(f"{gameDir}saves/{self.saveName}", True)
        os.makedirs(f"{gameDir}saves/{self.saveName}", exist_ok=True)
        self.gameMap.create_savedata(f"{gameDir}saves/{self.saveName}", Registry.saveData["Game"]["GameMap"]["seed"])

        self.gameMap = None
        self.maintance = None

        self.return_main()
