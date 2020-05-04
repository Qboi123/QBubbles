import json
import os as _os
import string
import sys
import zipimport
from tkinter import PhotoImage
from typing import Type
import typing as _t

import PIL as _PIL
import yaml

import qbubbles.bubbleSystem as _bubSystem
import qbubbles.components as _components
import qbubbles.config as _config
import qbubbles.events as _evts
import qbubbles.game as _game
import qbubbles.gameIO as _gameIO
import qbubbles.globals as _g
import qbubbles.init.bubblesInit as _bubblesInit
import qbubbles.init.effectsInit as _effectsInit
import qbubbles.init.mapsInit as _mapsInit
import qbubbles.init.spritesInit as _spritesInit
import qbubbles.menus.titleMenu as _titleMenu
import qbubbles.modloader as _modloader
import qbubbles.registry as _reg
import qbubbles.resources as _res
import qbubbles.scenemanager as _scenemngr
import qbubbles.scenes as _scenes
import qbubbles.utils as _utils
from qbubbles.effects import BaseEffect


class Load(_scenemngr.CanvasScene):
    def __init__(self, root):
        super(Load, self).__init__(root)

    def __repr__(self):
        return super(_scenemngr.CanvasScene, self).__repr__()

    def pre_initialize(self):
        pass

    def show_scene(self, *args, **kwargs):
        super(Load, self).show_scene(*args, **kwargs)
        self.initialize()

    # noinspection PyPep8Naming
    def initialize(self):
        config_ = _config.Reader(
            "config/startup.nzt").get_decoded()

        _gameIO.Logging(_os.path.join(_reg.Registry.gameData['launcherConfig']['gameDir'], "logs"))
        _gameIO.Logging.info("GameLoader", "Logging started.")

        with open("lang/" + config_["Game"]["language"] + ".yaml", "r") as file:
            lang_ = yaml.safe_load(file.read())

        _reg.Registry.gameData["config"] = config_
        _reg.Registry.gameData["language"] = lang_

        # Config resolution / positions
        root = _reg.Registry.get_window("default")
        # root = root
        _reg.Registry.gameData["WindowWidth"] = root.tkScale(root.winfo_screenwidth())
        _reg.Registry.gameData["WindowHeight"] = root.tkScale(root.winfo_screenheight())
        if "--travis" in sys.argv:
            _reg.Registry.gameData["WindowWidth"] = 1920
            _reg.Registry.gameData["WindowHeight"] = 1080
        _reg.Registry.gameData["MiddleX"] = _reg.Registry.gameData["WindowWidth"] / 2
        _reg.Registry.gameData["MiddleY"] = _reg.Registry.gameData["WindowHeight"] / 2

        _gameIO.Logging.info("GameLoader", f"Initialized window geometry: {_reg.Registry.gameData['WindowWidth']}x{_reg.Registry.gameData['WindowHeight']}")

        # # Register Xbox-Bindings
        # Registry.register_xboxbinding("A", game.close_present)
        # print("[Game]:", "Starting XboxController")
        # self.xbox = xbox.XboxController()
        # print("[Game]:", "Started XboxController")
        #
        # self.xControl = dict()
        #
        # a = [int(self.xbox.LeftJoystickX * 7), int(self.xbox.LeftJoystickY * 7)]
        # b = [int(self.xbox.RightJoystickX * 7), int(self.xbox.RightJoystickY * 7)]
        # self.xControl["LeftJoystick"] = a
        # self.xControl["RightJoystick"] = b
        # self.xControl["A"] = bool(self.xbox.A)
        # self.xControl["B"] = bool(self.xbox.B)
        # self.xControl["x"] = bool(self.xbox."x")
        # self.xControl[""y""] = bool(self.xbox."y")
        # self.xControl["Start"] = bool(self.xbox.Start)
        # self.xControl["Back"] = bool(self.xbox.Back)
        # self.xControl["LeftBumper"] = bool(self.xbox.LeftBumper)
        # self.xControl["RightBumper"] = bool(self.xbox.RightBumper)
        # self.xControl["LeftTrigger"] = int((self.xbox.LeftBumper + 1) / 2 * 7)
        # self.xControl["RightTrigger"] = int((self.xbox.RightBumper + 1) / 2 * 7)

        title_font = _utils.Font("Helvetica", 50, "bold")
        descr_font = _utils.Font("Helvetica", 15)

        _reg.Registry.register_scene("qbubbles:ErrorScene", _scenes.ErrorScene())
        _reg.Registry.register_scene("qbubbles:CrashScene", _scenes.CrashScene())

        sys.excepthook = _scenes.custom_excepthook
        root.report_callback_exception = _scenes.report_callback_exception
        _reg.Registry.get_window("fake").report_callback_exception = _scenes.report_callback_exception

        t0 = self.canvas.create_rectangle(0, 0, _reg.Registry.gameData["WindowWidth"], _reg.Registry.gameData["WindowHeight"], fill="#3f3f3f",
                                          outline="#3f3f3f")
        t1 = self.canvas.create_text(_reg.Registry.gameData["MiddleX"], _reg.Registry.gameData["MiddleY"] - 2,
                                     text="Loading Mods", anchor="s",
                                     font=title_font.get_tuple(), fill="#afafaf")
        t2 = self.canvas.create_text(_reg.Registry.gameData["MiddleX"], _reg.Registry.gameData["MiddleY"] + 2,
                                     text="", anchor="n",
                                     font=descr_font.get_tuple(), fill="#afafaf")
        self.canvas.update()

        _gameIO.Logging.info("GameLoader", f"Started on loading game.")

        mods_dir = f"{_reg.Registry.gameData['launcherConfig']['gameDir']}addons/{_g.GAME_VERSION}"

        if not _os.path.exists(mods_dir):
            _os.makedirs(mods_dir)

        _gameIO.Logging.info("ModLoader", f"Searching for addons in {repr(mods_dir)}")

        # mods_path = os.path.abspath(f"{mods_dir}").replace("\\", "/")
        # sys.path.insert(0, mods_path)
        modules = {}
        mainPackageNames = []

        try:
            for file in _os.listdir(mods_dir):
                # print(file, os.path.isfile(f"{mods_dir}/{file}"), f"{mods_dir}/{file}")
                # print(file)
                if _os.path.isfile(f"{mods_dir}/{file}"):
                    if file.endswith(".pyz"):
                        a = zipimport.zipimporter(f"{mods_dir}/{file}")  # f"{file}.main", globals(), locals(), [])
                        # print(dir(a))
                        try:
                            mainPackage = json.loads(a.get_data("qbubble-addoninfo.json"))["mainPackage"]
                        except OSError:
                            _gameIO.Logging.warning("ModLoader", f"Found non-addon file: {file}")
                            continue
                        if mainPackage in mainPackageNames:
                            raise RuntimeError(f"Illegal package name '{mainPackage}'. "
                                               f"Package name is already in use")

                        if '.' in mainPackage:
                            _gameIO.Logging.error("ModLoader", f"Illegal package name: '{mainPackage}'. "
                                     f"Package name contains a dot")
                            continue
                        error = False
                        for char in mainPackage[1:]:
                            if char not in string.ascii_letters+string.digits:
                                _gameIO.Logging.error("ModLoader", f"Illegal package name: '{mainPackage}'. "
                                         f"Package name contains invalid character '{char}'")
                                error = True
                        if error:
                            continue

                        mainPackageNames.append(mainPackage)

                        module = a.load_module(mainPackage)
                        # _locals = {firstname: module}
                        # _globals = {}
                        # module = eval(f"{mainPackage}", _globals, _locals)
                        # module = module.qplaysoftware.exampleaddon
                        if a.find_module("qbubbles") is not None:
                            raise RuntimeError("Illegal module name: 'qbubbles'")
                        modules[module.ADDONID] = a
                        # print(a)
                    else:
                        if file.endswith(".disabled"):
                            continue
                        _gameIO.Logging.warning("ModLoader", f"Found non-addon file: {file}")
        except Exception as e:
            import traceback
            _gameIO.Logging.fatal("ModLoader", "".join(list(traceback.format_exception(e.__class__, e, e.__traceback__))))
            self.scenemanager.change_scene(
                "qbubbles:ErrorScene",
                "Addon loading failed",
                "".join(list(traceback.format_exception_only(e.__class__, e)))
            )

            # self.canvas.itemconfig(t0, fill="#ff0000")
            # self.canvas.itemconfig(t1, text="Addon loading failed!", fill="#ffa7a7")
            # self.canvas.itemconfig(t2, text=,
            #                        fill="#ffa7a7")
            # self.canvas.create_text(Registry.gameData["WindowWidth"]-16, Registry.gameData["WindowHeight"]-16,
            #                         text="Press any key or mouse button to continue", anchor="se",
            #                         font=("Helvetica", Registry.get_window("default").tkScale(16), 'bold'), fill="#ffa7a7")
            # Registry.get_window("default").focus_set()
            # self.canvas.bind_all("<Key>", lambda evt: os.kill(os.getpid(), 1))
            # self.canvas.bind_all("<Button>", lambda evt: os.kill(os.getpid(), 1))
            # Registry.get_window("default").protocol("WM_DELETE_WINDOW", lambda: None)
            # self.canvas.mainloop()
        # sys.path.remove(mods_path)

        addon_ids = _reg.Registry.get_all_addons()

        if len(addon_ids) > 0:
            _gameIO.Logging.info("ModLoader", f"Attempting to load the following addons: {', '.join(list(addon_ids).copy())}")
        else:
            _gameIO.Logging.info("ModLoader", f"No addons found.")

        # print(list(addon_ids))

        addons = []
        for addon_id in list(addon_ids):
            # print(repr(addon_id), type(addon_id))
            if _reg.Registry.mod_exists(addon_id):
                addon = _reg.Registry.get_module(addon_id)["addon"]
                addon: Type[_modloader.AddonSkeleton]
                self.canvas.itemconfig(t2, text=addon.name)
                addon.zipimport = None
                if addon.modID in modules.keys():
                    addon.zipimport = modules[addon.modID]
                addons.append(addon())

        # print(addons)

        _evts.PreInitializeEvent(self, self.canvas, t1, t2)

        # # Pre-Initialize
        # self.mod_loader.pre_initialize(self)

        # =----- GAME MAPS -----= #
        self.canvas.itemconfig(t1, text="Loading Gamemaps")
        self.canvas.itemconfig(t2, text="Initialize gamemaps")
        self.canvas.update()

        _gameIO.Logging.info("GameLoader", f"Loading Gamemaps...")

        try:
            gameMaps = _mapsInit.init_gamemaps()
            i = 1
            for gamemap in gameMaps:
                self.canvas.itemconfig(t2, text=f"Register gamemap {i}/{len(gameMaps)}")
                self.canvas.update()

                _reg.Registry.register_gamemap(gamemap.get_uname(), gamemap)
                i += 1
        except Exception as e:
            import traceback
            _gameIO.printerr("".join(list(traceback.format_exception_only(e.__class__, e))))
            self.scenemanager.change_scene(
                "qbubbles:ErrorScene",
                "Initialize Game Maps failed",
                "".join(list(traceback.format_exception_only(e.__class__, e)))
            )

        # =----- SPRITES -----= #
        self.canvas.itemconfig(t1, text="Loading Sprites")
        self.canvas.itemconfig(t2, text="Initialize sprites")
        self.canvas.update()

        _gameIO.Logging.info("GameLoader", f"Loading Sprites...")

        try:
            sprites = _spritesInit.init_sprites()
            i = 1
            for sprite in sprites:
                self.canvas.itemconfig(t2, text=f"Register sprite {i}/{len(gameMaps)}")
                self.canvas.update()

                _reg.Registry.register_sprite(sprite.get_sname(), sprite)
                i += 1
        except Exception as e:
            import traceback
            _gameIO.printerr("".join(list(traceback.format_exception_only(e.__class__, e))))
            self.scenemanager.change_scene(
                "qbubbles:ErrorScene",
                "Initialize Sprites failed"
                "".join(list(traceback.format_exception_only(e.__class__, e)))
            )

        self.canvas.itemconfig(t1, text="Loading Bubbles")
        self.canvas.itemconfig(t2, text="Initialize bubbles")
        self.canvas.update()

        _gameIO.Logging.info("GameLoader", f"Loading Bubbles...")

        try:
            bubbleObjects = _bubblesInit.init_bubbles()
            for bubbleObject in bubbleObjects:
                self.canvas.itemconfig(t2, text=f"Register bubble {bubbleObject.get_uname()}")
                _reg.Registry.register_bubble(bubbleObject.get_uname(), bubbleObject)
            _bubSystem.BubbleSystem.init()
        except Exception as e:
            import traceback
            _gameIO.printerr("".join(list(traceback.format_exception_only(e.__class__, e))))
            self.scenemanager.change_scene(
                "qbubbles:ErrorScene",
                "Initialize Bubbles failed!",
                "".join(list(traceback.format_exception_only(e.__class__, e)))
            )

        self.canvas.itemconfig(t2, text="Loading bubble models")
        self.canvas.update()

        _gameIO.Logging.info("GameLoader", f"Loading Bubble Models...")

        try:
            modelLoader = _res.ModelLoader()
            modelsBubble = modelLoader.load_models("bubble")

            for bubbleObject in bubbleObjects:
                if bubbleObject.get_uname().count(":") > 1:
                    _gameIO.printerr(f"Illegal uname: {bubbleObject.get_uname()} has multiple ':' characters")
                    self.scenemanager.change_scene(
                        "qbubbles:ErrorScene",
                        "Loading Bubble Models failed",
                        f"Illegal uname: {bubbleObject.get_uname()} has multiple ':' characters")
                uname = bubbleObject.get_uname().split(":")[-1]
                modid = bubbleObject.get_uname().split(":")[0]
                self.canvas.itemconfig(t2, text=f"Generating bubble image: qbubbles:{uname}")
                self.canvas.update()
                if bubbleObject.get_uname().split(":")[-1] not in modelsBubble.keys():
                    _gameIO.printwrn(f"Bubble object with uname '{bubbleObject.get_uname().split(':')[-1]}' have no bubble model")
                    continue

                images = {}
                images = modelLoader.generate_bubble_images(bubbleObject.minRadius, bubbleObject.maxRadius,
                                                            modelsBubble[uname])
                # for radius in range(bubbleObject.minRadius, bubbleObject.maxRadius):
                #     colors = modelsBubble[uname]["Colors"]
                #     images[radius] = utils.createbubble_image((radius, radius), None, *colors)
                for radius, texture in images.items():
                    _reg.Registry.register_texture("qbubbles:bubble", bubbleObject.get_uname(), texture, radius=radius)
                _reg.Registry.register_bubble(bubbleObject.get_uname(), bubbleObject)
        except Exception as e:
            import traceback
            _gameIO.printerr("".join(list(traceback.format_exception_only(e.__class__, e))))
            self.scenemanager.change_scene(
                "qbubbles:ErrorScene",
                "Loading Bubble Models failed!",
                "".join(list(traceback.format_exception_only(e.__class__, e)))
            )

        self.canvas.itemconfig(t1, text="Loading Sprites")
        self.canvas.itemconfig(t2, text="Load sprite models")
        self.canvas.update()

        _gameIO.Logging.info("GameLoader", f"Loading Sprite Models...")

        try:
            modelsSprite = modelLoader.load_models("sprite")
            self.playerModel = modelsSprite["player"]

            for spriteName, spriteData in modelsSprite.items():
                if spriteData["Rotation"]:
                    degrees = spriteData['RotationDegrees']
                    self.canvas.itemconfig(t2, text=f"Load images for {spriteName} 0 / {int(360 / degrees)}")
                    self.canvas.update()
                    image = _PIL.Image.open(f"assets/textures/sprites/{spriteData['Image']['Name']}.png")
                    for degree in range(0, 360, spriteData["RotationDegrees"]):
                        self.canvas.itemconfig(
                            t2, text=f"Load images for {spriteName} {int(degree / degrees)} / {int(360 / degrees)}")
                        self.canvas.update()
                        image_c: _PIL.Image.Image = image.copy()
                        image_c = image_c.rotate(degree, resample=_PIL.Image.BICUBIC)
                        _reg.Registry.register_texture("sprite", spriteName, _PIL.ImageTk.PhotoImage(image_c), rotation=degree)
                    # print(Registry._registryTextures)
        except Exception as e:
            import traceback
            _gameIO.printerr("".join(list(traceback.format_exception_only(e.__class__, e))))
            self.scenemanager.change_scene(
                "qbubbles:ErrorScene",
                "Loading Sprite Models failed!",
                "".join(list(traceback.format_exception_only(e.__class__, e)))
            )


        # # TODO: Remove this and use Registry.get_bubresource(...) as above (with .yml files for bubble-models)
        # self.canvas.itemconfig(t2, text="Creating Dicts")
        # self.canvas.update()
        #
        # # Adding the dictionaries for the bubbles. With different res.
        # Registry.gameData["BubbleImage"] = dict()
        # Registry.gameData["BubbleImage"]["Normal"] = dict()
        # Registry.gameData["BubbleImage"]["Triple"] = dict()
        # Registry.gameData["BubbleImage"]["Double"] = dict()
        # Registry.gameData["BubbleImage"]["Kill"] = dict()
        # Registry.gameData["BubbleImage"]["SpeedUp"] = dict()
        # Registry.gameData["BubbleImage"]["SpeedDown"] = dict()
        # Registry.gameData["BubbleImage"]["Ultimate"] = dict()
        # Registry.gameData["BubbleImage"]["Up"] = dict()
        # Registry.gameData["BubbleImage"]["Teleporter"] = dict()
        # Registry.gameData["BubbleImage"]["SlowMotion"] = dict()
        # Registry.gameData["BubbleImage"]["DoubleState"] = dict()
        # Registry.gameData["BubbleImage"]["Protect"] = dict()
        # Registry.gameData["BubbleImage"]["ShotSpdStat"] = dict()
        # Registry.gameData["BubbleImage"]["HyperMode"] = dict()
        # Registry.gameData["BubbleImage"]["TimeBreak"] = dict()
        # Registry.gameData["BubbleImage"]["Confusion"] = dict()
        # Registry.gameData["BubbleImage"]["Paralyse"] = dict()
        # Registry.gameData["BubbleImage"]["StoneBub"] = dict()
        # Registry.gameData["BubbleImage"]["NoTouch"] = dict()
        # Registry.gameData["BubbleImage"]["Key"] = dict()
        # Registry.gameData["BubbleImage"]["Diamond"] = dict()
        # Registry.gameData["BubbleImage"]["Present"] = dict()
        # Registry.gameData["BubbleImage"]["SpecialKey"] = dict()
        #
        # _min = 21
        # _max = 80
        #
        # # Adding the different resolutions to the bubbles.
        # for i in range(_min, _max + 1):
        #     Registry.gameData["BubbleImage"]["Normal"][i] = utils.createbubble_image((i, i), None, "white")
        #     Registry.gameData["BubbleImage"]["Double"][i] = utils.createbubble_image((i, i), None, "gold")
        #     Registry.gameData["BubbleImage"]["Triple"][i] = utils.createbubble_image((i, i), None, "blue", "#007fff", "#00ffff", "white")
        #     Registry.gameData["BubbleImage"]["SpeedDown"][i] = utils.createbubble_image((i, i), None, "#ffffff", "#a7a7a7", "#7f7f7f", "#373737")
        #     Registry.gameData["BubbleImage"]["SpeedUp"][i] = utils.createbubble_image((i, i), None, "#ffffff", "#7fff7f", "#00ff00", "#007f00")
        #     Registry.gameData["BubbleImage"]["Up"][i] = utils.createbubble_image((i, i), None, "#00ff00", "#00ff00", "#00000000", "#00ff00")
        #     Registry.gameData["BubbleImage"]["Ultimate"][i] = utils.createbubble_image((i, i), None, "gold", "gold", "orange", "gold")
        #     Registry.gameData["BubbleImage"]["Kill"][i] = utils.createbubble_image((i, i), None, "#7f0000", "#7f007f", "#7f0000",)
        #     Registry.gameData["BubbleImage"]["Teleporter"][i] = utils.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#ff1020", "#373737")
        #     Registry.gameData["BubbleImage"]["SlowMotion"][i] = utils.createbubble_image((i, i), None, "#ffffffff", "#00000000", "#000000ff")
        #     Registry.gameData["BubbleImage"]["DoubleState"][i] = utils.createbubble_image((i, i), None, "gold", "#00000000", "gold", "gold")
        #     Registry.gameData["BubbleImage"]["Protect"][i] = utils.createbubble_image((i, i), None, "#00ff00", "#3fff3f", "#7fff7f", "#9fff9f")
        #     Registry.gameData["BubbleImage"]["ShotSpdStat"][i] = utils.createbubble_image((i, i), None, "#ff7f00", "#ff7f00", "gold")
        #     Registry.gameData["BubbleImage"]["HyperMode"][i] = utils.createbubble_image((i, i), None, "black", "black", "white", "black")
        #     Registry.gameData["BubbleImage"]["TimeBreak"][i] = utils.createbubble_image((i, i), None, "red", "orange", "yellow", "white")
        #     Registry.gameData["BubbleImage"]["Confusion"][i] = utils.createbubble_image((i, i), None, "black", "purple", "magenta", "white")
        #     Registry.gameData["BubbleImage"]["Paralyse"][i] = utils.createbubble_image((i, i), None, "#ffff00", "#ffff00", "#ffff7f", "#ffffff")
        #     Registry.gameData["BubbleImage"]["StoneBub"][i] = utils.createbubble_image((i, i), None, "black", "orange", "yellow")
        #     Registry.gameData["BubbleImage"]["NoTouch"][i] = utils.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#7f7f7f", "#373737")
        #
        #     self.canvas.itemconfig(t1, text="Loading Bubbles Sizes")
        #     self.canvas.itemconfig(t2, text="Loading %s of %s" % (i - _min, _max - 1 - _min))
        #     self.canvas.update()
        #
        # # Adding the static-resolution-bubbles.
        # Registry.gameData["BubbleImage"]["Key"][60] = PhotoImage(file="assets/bubbles/Key.png")
        # Registry.gameData["BubbleImage"]["Diamond"][36] = PhotoImage(
        #     file="assets/bubbles/Diamond.png")
        # Registry.gameData["BubbleImage"]["Present"][40] = PhotoImage(
        #     file="assets/bubbles/Present.png")
        # # noinspection PyTypeChecker
        # Registry.gameData["BubbleImage"]["Coin"] = PhotoImage(file="assets/CoinBub.png")
        # Registry.gameData["BubbleImage"]["SpecialKey"][48] = PhotoImage(
        #     file="assets/bubbles/SpecialMode.png")

        # # TODO: Remove this.
        # for i in Registry.gameData["BubbleImage"].keys():
        #     print("%s: %s" % (i, repr(Registry.gameData["BubbleImage"][i])))

        # -=================== INTITIALIZE EFFECTS ===================- #
        self.canvas.itemconfig(t1, text="Loading Effects")
        self.canvas.itemconfig(t2, text="Initialize effects")
        self.canvas.update()

        _gameIO.Logging.info("GameLoader", f"Loading Effects...")

        baseEffects: _t.List[BaseEffect] = _effectsInit.init_effects()
        for baseEffect in baseEffects:
            self.canvas.itemconfig(t2, text=f"Register effect {baseEffect.get_uname()}")
            _reg.Registry.register_effect(baseEffect.get_uname(), baseEffect)

        # -================== INITIALIZE GUI IMAGES ==================- #
        self.canvas.itemconfig(t1, text="Loading Other Images")
        self.canvas.itemconfig(t2, text="Loading GUI Images")
        self.canvas.update()

        _gameIO.Logging.info("GameLoader", f"Loading GUI Images...")

        _reg.Registry.register_texture(
            "gui", "qbubbles:effect_bar", PhotoImage(file="assets/textures/gui/classic_map/effect_bar.png"),
            gamemap="qbubbles:classic_map")

        self.canvas.itemconfig(t1, text="Loading Other Images")
        self.canvas.itemconfig(t2, text="Loading Effect Images")
        self.canvas.update()

        _gameIO.Logging.info("GameLoader", f"Loading Effect Images...")

        _reg.Registry.register_default_texture("effect", texture=PhotoImage(file="assets/textures/icons/effect/default.png"))

        for item in _os.listdir("assets/textures/icons/effect/"):
            image = PhotoImage(file=f"assets/textures/icons/effect/{item}")
            _reg.Registry.register_texture("effect", f"qbubbles:{_os.path.splitext(item)[0]}", image, gamemap="qbubbles:classic_map")

        # -===================== INITIALIZE ICONS ====================- #
        # Adding ship image...                                          #
        _reg.Registry.register_image("ShipImage", PhotoImage(file="assets/Ship.png"))

        self.canvas.itemconfig(t1, text="Loading Other Images")
        self.canvas.itemconfig(t2, text="Loading Icons")
        self.canvas.update()

        _gameIO.Logging.info("GameLoader", f"Loading Icons...")

        try:
            # Adding Store Item Icons. (SII)
            _reg.Registry.register_storeitem("Key", PhotoImage(file="assets/Images/StoreItems/Key.png"))
            self.canvas.itemconfig(t2, text="Loading Icons - Store Item: Key")
            self.canvas.update()
            _reg.Registry.register_storeitem("Teleport", PhotoImage(file="assets/Images/StoreItems/Teleport.png"))
            self.canvas.itemconfig(t2, text="Loading Icons - Store Item: Teleport")
            self.canvas.update()
            _reg.Registry.register_storeitem("Shield", PhotoImage(file="assets/Images/StoreItems/Shield.png"))
            self.canvas.itemconfig(t2, text="Loading Icons - Store Item: Shield")
            self.canvas.update()
            _reg.Registry.register_storeitem("Diamond", PhotoImage(file="assets/Images/StoreItems/DiamondBuy.png"))
            self.canvas.itemconfig(t2, text="Loading Icons - Store Item: Diamond")
            self.canvas.update()
            _reg.Registry.register_storeitem("BuyACake", PhotoImage(file="assets/Images/StoreItems/BuyACake.png"))
            self.canvas.itemconfig(t2, text="Loading Icons - Store Item: Buy A Cake")
            self.canvas.update()
            _reg.Registry.register_storeitem("Pop3Bubbles", PhotoImage(file="assets/Images/StoreItems/Pop_3_bubs.png"))
            self.canvas.itemconfig(t2, text="Loading Icons - Store Item: Pop 3 Bubbles")
            self.canvas.update()
            _reg.Registry.register_storeitem("PlusLife", PhotoImage(file="assets/Images/StoreItems/PlusLife.png"))
            self.canvas.itemconfig(t2, text="Loading Icons - Store Item: PlusLife")
            self.canvas.update()
            _reg.Registry.register_storeitem("Speedboost", PhotoImage(file="assets/Images/StoreItems/SpeedBoost.png"))
            self.canvas.itemconfig(t2, text="Loading Icons - Store Item: Speedboost")
            self.canvas.update()
            _reg.Registry.register_storeitem("SpecialMode", PhotoImage(file="assets/Images/StoreItems/SpecialMode.png"))
            self.canvas.itemconfig(t2, text="Loading Icons - Store Item: Special Mode")
            self.canvas.update()
            _reg.Registry.register_storeitem("DoubleScore", PhotoImage(file="assets/Images/StoreItems/DoubleScore.png"))
            self.canvas.itemconfig(t2, text="Loading Icons - Double Score")
            self.canvas.update()
        except Exception as e:
            import traceback
            _gameIO.printerr("".join(list(traceback.format_exception_only(e.__class__, e))))
            self.scenemanager.change_scene(
                "qbubbles:ErrorScene",
                "Loading Icons Stage 1 failed!",
                "".join(list(traceback.format_exception_only(e.__class__, e)))
            )

        try:

            _gameIO.Logging.info("GameLoader", f"Loading Backgrounds...")

            # Loading backgrounds
            self.canvas.itemconfig(t1, text="Loading Other Images")
            self.canvas.itemconfig(t2, text="Loading Background - Line")
            self.canvas.update()
            _reg.Registry.register_background("Line", PhotoImage(file="assets/LineIcon.png"))

            self.canvas.itemconfig(t1, text="Loading Other Images")
            self.canvas.itemconfig(t2, text="Loading Background - Normal")
            self.canvas.update()
            _reg.Registry.register_background("Normal", PhotoImage(file="assets/Images/Backgrounds/GameBG2.png"))

            self.canvas.itemconfig(t1, text="Loading Other Images")
            self.canvas.itemconfig(t2, text="Loading Background - Special Mode")
            self.canvas.update()
            _reg.Registry.register_background("Special", PhotoImage(file="assets/Images/Backgrounds/GameBG Special2.png"))
        except Exception as e:
            import traceback
            _gameIO.printerr("".join(list(traceback.format_exception_only(e.__class__, e))))
            self.scenemanager.change_scene(
                "qbubbles:ErrorScene",
                "Loading Background failed",
                "".join(list(traceback.format_exception_only(e.__class__, e)))
            )

        try:

            _gameIO.Logging.info("GameLoader", f"Loading Foregrounds...")

            # Loading foregrounds
            self.canvas.itemconfig(t1, text="Loading Other Images")
            self.canvas.itemconfig(t2, text="Loading Foreground - For Bubble Gift")
            self.canvas.update()
            _reg.Registry.register_foreground("BubbleGift", PhotoImage(file="assets/EventBackground.png"))

            self.canvas.itemconfig(t1, text="Loading Other Images")
            self.canvas.itemconfig(t2, text="Loading Foreground - Store FG")
            self.canvas.update()
            _reg.Registry.register_foreground("StoreFG", PhotoImage(file="assets/FG2.png"))
        except Exception as e:
            import traceback
            _gameIO.printerr("".join(list(traceback.format_exception_only(e.__class__, e))))
            self.scenemanager.change_scene(
                "qbubbles:ErrorScene",
                "Loading Foregounds failed",
                "".join(list(traceback.format_exception_only(e.__class__, e)))
            )

        try:

            _gameIO.Logging.info("GameLoader", f"Loading Icons...")

            # Loading Icons
            self.canvas.itemconfig(t1, text="Loading Other Images")
            self.canvas.itemconfig(t2, text="Loading Icons - Present Circle")
            self.canvas.update()
            _reg.Registry.register_icon("PresentCircle", PhotoImage(file="assets/Circle.png"))

            self.canvas.itemconfig(t1, text="Loading Other Images")
            self.canvas.itemconfig(t2, text="Loading Icons - Present Chest")
            self.canvas.update()
            _reg.Registry.register_icon("PresentChest", PhotoImage(file="assets/Present.png"))

            self.canvas.itemconfig(t1, text="Loading Other Images")
            self.canvas.itemconfig(t2, text="Loading Icons - Store: Diamond & Coin")
            self.canvas.update()
            _reg.Registry.register_icon("StoreDiamond", PhotoImage(file="assets/Diamond.png"))
            _reg.Registry.register_icon("StoreCoin", PhotoImage(file="assets/Coin.png"))

            self.canvas.itemconfig(t1, text="Loading Other Images")
            self.canvas.itemconfig(t2, text="Loading Icons - Pause")
            self.canvas.update()
            _reg.Registry.register_icon("Pause", PhotoImage(file="assets/Pause.png"))

            self.canvas.itemconfig(t1, text="Loading Other Images")
            self.canvas.itemconfig(t2, text="Loading Icons - SlowMotion")
            self.canvas.update()
            _reg.Registry.register_icon("EffectSlowmotion", PhotoImage(file="assets/SlowMotionIcon.png"))
        except Exception as e:
            import traceback
            _gameIO.printerr("".join(list(traceback.format_exception_only(e.__class__, e))))
            self.scenemanager.change_scene(
                "qbubbles:ErrorScene",
                "Loading Icons Stage 2 failed",
                "".join(list(traceback.format_exception_only(e.__class__, e)))
            )

        # Loading fonts
        _reg.Registry.gameData["fonts"] = {}

        _gameIO.Logging.info("GameLoader", f"Loading Fonts...")

        self.canvas.itemconfig(t1, text="Loading Fonts")
        self.canvas.itemconfig(t2, text="Title Fonts")
        self.canvas.update()
        _reg.Registry.gameData["fonts"]["titleButtonFont"] = _utils.Font("Helvetica", 15)

        self.canvas.itemconfig(t1, text="Loading Fonts")
        self.canvas.itemconfig(t2, text="Slots Menu Fonts")
        self.canvas.update()
        _reg.Registry.gameData["fonts"]["slotsButtonFont"] = _utils.Font("Helvetica", 12)

        _evts.InitializeEvent(self, self.canvas, t1, t2)

        for bubble in _reg.Registry.get_bubbles():
            if _reg.Registry.bubresource_exists(bubble.get_uname()):
                continue

        _gameIO.Logging.info("GameLoader", f"Loading Scenes...")

        # Register Scenes
        self.canvas.itemconfig(t1, text="Loading Scenes")
        self.canvas.itemconfig(t2, text="Title Screen")
        _reg.Registry.register_scene("TitleScreen", _titleMenu.TitleMenu())
        self.canvas.itemconfig(t2, text="Saves Menu")
        _reg.Registry.register_scene("SaveMenu", _scenes.SavesMenu())
        self.canvas.itemconfig(t2, text="Store")
        _reg.Registry.register_scene("Store", _components.Store())
        self.canvas.itemconfig(t2, text="Game")
        _reg.Registry.register_scene("Game", _game.Game())

        # Registry.register_mode("teleport", TeleportMode())

        _evts.PostInitializeEvent(self, self.canvas, t1, t2)

        self.canvas.itemconfig(t1, text="DONE!")
        self.canvas.itemconfig(t2, text="")

        self.scenemanager.change_scene("TitleScreen")
        return

        # # Setting background from nothing to normal.
        # self.back["id"] = self.canvas.create_image(0, 0, anchor="nw", image=self.back["normal"])
        #
        # # Creating shi
        # self.ship["id"] = self.canvas.create_image(7.5, 7.5, image=self.ship["image"])
        # print(self.ship["id"])
        #
        # # Moving ship to position
        # self.canvas.move(self.ship["id"],
        #     self.Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Position"][0],
        #     self.Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Position"][1]
        # )
        #
        # self.canvas.itemconfig(t1, text="Creating Stats objects")
        # self.canvas.itemconfig(t2, text="")
        #
        # # Initializing the panels for the game.
        # self.panels["game/top"] = self.canvas.create_rectangle(
        #     -1, -1, Registry.gameData["WindowWidth"], 69, fill="darkcyan"
        # )
