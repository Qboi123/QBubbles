import threading
from random import randint
from threading import Thread
from time import time

from tkinter import *

from qbubbles.config import Reader
from qbubbles.registry import Registry
from qbubbles.scenemanager import CanvasScene
from qbubbles.state import State


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, group, target, name, *args, **kwargs):
        super(StoppableThread, self).__init__(group, target, name, args=args, kwargs=kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class Present:
    """
    Giving a present activated by a bubble
    """

    def __init__(self, canvas, stats, temp, modes, config, icons, foregrounds, log, font):
        # Sets pause, and presentmode for controling information.
        modes["pause"] = True
        modes["present"] = True

        mid_x = config["middle-x"]
        mid_y = config["middle-y"]

        # Sets pause save-variables.
        temp["scorestate-save"] = stats["scorestate_time"] - time()
        temp["secure-save"] = stats["secure_time"] - time()
        temp["timebreak-save"] = stats["timebreak_time"] - time()
        temp["confusion-save"] = stats["confusion_time"] - time()
        temp["slowmotion-save"] = stats["slowmotion_time"] - time()
        temp["paralyse-save"] = stats["paralyse_time"] - time()
        temp["shotspeed-save"] = stats["shotspeed_time"] - time()
        temp["notouch-save"] = stats["notouch_time"] - time()
        temp["special-level-save"] = stats["special-level_time"] - time()

        # Creating ID's for window and information.
        self.lineid = []
        self.bgid2 = canvas.create_rectangle(0, 0, 0, 0, fill="#002713")
        self.bgid = canvas.create_image(mid_x, mid_y + 50, image=foregrounds["present-fg"])
        self.LineImageLength = len(self.lineid)
        self.IconId1 = canvas.create_image(mid_x, 120, image=icons["circle"])
        self.IconId2 = canvas.create_image(mid_x, 120, image=icons["present"])
        self.Diamonds = None
        self.Money = None
        self.textid = canvas.create_text(mid_x, mid_y + 20, font=(font, 30), fill="black")
        self.fgid = canvas.create_image(mid_x, mid_y, image=foregrounds["store-fg"])

        # Ramdomizing Gifts for output
        Thread(None, lambda: self.randomize_gifts(canvas, stats, log)).start()

    def randomize_gifts(self, canvas, stats, log, index=None):
        """
        Randomizing Gifts
        :param log:
        :param stats:
        :param canvas:
        :param index:
        :return:
        """
        if index is None:
            # If parameter "index" was not given.
            index = randint(0, 1000)
        if index == 0:
            # Master Bonus, huge pack of diamonds and coins
            a = randint(0, 44)
            if 0 <= a < 16:
                self.Diamonds = a
            elif 16 <= a < 24:
                self.Diamonds = a * 2
            elif 24 <= a < 32:
                self.Diamonds = a * 3
            elif 32 <= a < 36:
                self.Diamonds = a * 4
            elif 36 <= a < 40:
                self.Diamonds = a * 5
            elif 40 <= a < 42:
                self.Diamonds = a * 6
            elif 42 <= a < 44:
                self.Diamonds = a * 8
            elif 44 <= a < 45:
                self.Diamonds = a * 12

            a = randint(0, 44)
            if 0 <= a < 16:
                self.Money = a
            elif 16 <= a < 24:
                self.Money = a * 10
            elif 24 <= a < 32:
                self.Money = a * 15
            elif 32 <= a < 36:
                self.Money = a * 20
            elif 36 <= a < 40:
                self.Money = a * 25
            elif 40 <= a < 42:
                self.Money = a * 30
            elif 42 <= a < 44:
                self.Money = a * 40
            elif 44 <= a < 45:
                self.Money = a * 60
            text = "You earned:\n" + str(self.Diamonds) + \
                   "diamonds and " + str(self.Money) + " coins."
            canvas.itemconfig(self.textid, text=text)

            stats["diamonds"] += self.Diamonds
            stats["coins"] += self.Money

            # play_sound("versions/"+launcher_config["versionDir"]+"/assets/sounds/Tadaa.wav")
        elif 1 <= index < 200:
            # Teleport
            text = "You earned:\n1 Teleport"
            canvas.itemconfig(self.textid, text=text)
            stats["teleports"] += 1

            # play_sound("versions/"+launcher_config["versionDir"]+"/assets/sounds/Tadaa.wav")
        elif 200 <= index < 360:
            # Giving a Protection
            # Text for information
            text = "You earned:\nA protection"
            canvas.itemconfig(self.textid, text=text)

            # Playing sound for gift.

            # Globals and status setup
            State.set_state(canvas, log, stats, "Protect", backgrounds=None)

            # play_sound("versions/"+launcher_config["versionDir"]+"/assets/sounds/Tadaa.wav")
        else:
            # Nothing gives
            text = "O, oh. There's nothing"
            canvas.itemconfig(self.textid, text=text)

    def exit(self, canvas):
        """
        Exits present screen.
        :return:
        """
        # Deletes line background.
        for i in self.lineid:
            canvas.delete(i)
        canvas.delete(self.bgid)
        canvas.delete(self.textid)
        canvas.delete(self.IconId1)
        canvas.delete(self.IconId2)
        canvas.delete(self.bgid2)
        canvas.delete(self.fgid)


class SpecialMode:
    @staticmethod
    def create_bubble(canvas, config, bubble, stats, bub, id2=None, loc_x=None, loc_y=None, rad=None, spd=None):
        """
        Creates bubble.
        :param spd:
        :param rad:
        :param loc_y:
        :param loc_x:
        :param bubble:
        :param canvas:
        :param config:
        :param stats:
        :param bub:
        :param id2:
        :return:
        """
        if id2 is not None:
            index = id2
        else:
            index = randint(0, 1600)
        if loc_x is None and loc_y is None and rad is None and spd is None:
            loc_x = config["width"] + config["Bubble"]["screen-gap"]
            rad = randint(int(config["Bubble"]["min-radius"]), int(config["Bubble"]["max-radius"]))
            loc_y = randint(72 + rad, (config["height"] - rad))
        else:
            pass
        if 0 <= index < 500:
            ids = [canvas.create_image(loc_x, loc_y, image=bub["Triple"][rad * 2])]
            act = "Triple"
            spd = randint(int(stats["bubspeed"]) + 2, int(stats["bubspeed"]) + 6)
            hardness = 1
        elif 500 <= index < 700:
            if stats["lives"] < 7:
                ids = [canvas.create_image(loc_x, loc_y, image=bub["Up"][rad * 2])]
                act = "Up"
                spd = randint(int(stats["bubspeed"]), int(stats["bubspeed"]) + 3)
                hardness = 1
            else:
                ids = [canvas.create_image(loc_x, loc_y, image=bub["Normal"][rad * 2])]
                act = "Normal"
                spd = randint(int(stats["bubspeed"]) - 3, int(stats["bubspeed"]))
                hardness = 1
        elif 700 <= index < 800:
            ids = [canvas.create_image(loc_x, loc_y, image=bub["Ultimate"][rad * 2])]
            act = "Ultimate"
            spd = randint(int(stats["bubspeed"]) + 4, int(stats["bubspeed"]) + 8)
            hardness = 1
        elif 800 <= index < 950:
            ids = [canvas.create_image(loc_x, loc_y, image=bub["DoubleState"][rad * 2])]
            act = "DoubleState"
            spd = randint(int(stats["bubspeed"]) + 4, int(stats["bubspeed"]) + 8)
            hardness = 1
        elif 950 <= index < 1050:
            ids = [canvas.create_image(loc_x, loc_y, image=bub["TimeBreak"][rad * 2])]
            act = "TimeBreak"
            spd = randint(int(stats["bubspeed"]) + 4, int(stats["bubspeed"]) + 8)
            hardness = 1
        elif 1050 <= index < 1100:
            ids = [canvas.create_image(loc_x, loc_y, image=bub["HyperMode"][rad * 2])]
            act = "HyperMode"
            spd = randint(int(stats["bubspeed"]) - 3, int(stats["bubspeed"]))
            hardness = 1
        elif 1100 <= index < 1200:
            rad = 20
            ids = [canvas.create_image(loc_x, loc_y, image=bub["Present"][40])]
            act = "Present"
            spd = randint(int(stats["bubspeed"]), int(stats["bubspeed"]) + 2)
            hardness = 1
        elif 1200 <= index < 1500:
            ids = [canvas.create_image(loc_x, loc_y, image=bub["Coin"])]
            rad = 20
            act = "Coin"
            spd = randint(int(stats["bubspeed"]), int(stats["bubspeed"]) + 2)
            hardness = 2
        elif 1500 <= index < 1600:
            ids = [canvas.create_image(loc_x, loc_y, image=bub["Diamond"][36])]
            rad = 18
            act = "Diamond"
            spd = randint(int(stats["bubspeed"]) + 2, int(stats["bubspeed"]) + 4)
            hardness = 1
        else:
            ids = [canvas.create_image(loc_x, loc_y, image=bub["Normal"][rad * 2])]
            act = "Normal"
            spd = randint(int(stats["bubspeed"]) - 3, int(stats["bubspeed"]))
            hardness = 1
        bubble["bub-special"].append(True)
        bubble["bub-index"].append(index)
        bubble["bub-position"].append([loc_x, loc_y])
        bubble["bub-hardness"].append(hardness)
        bubble["bub-action"].append(act)
        bubble["bub-radius"].append(rad)
        bubble["bub-speed"].append(spd)
        bubble["bub-id"].append(ids)
        index = bubble["bub-id"].index(ids, 0, len(bubble["bub-id"]))
        if not bubble["active2"][index]:
            bubble["active2"][index] = True
            bubble["active"] += 1
        # Thread(None, lambda: movebubble_thread(ids, bubble, spd, act, ids[0], r, c, stats, input_modes)).start()


class Store(CanvasScene):
    """
    Base Store Class.
    This class is for the in-game store.
    The store contains items to buy with
    virtual money (Coins and Diamonds).
    """
    
    def __init__(self):
        super(Store, self).__init__(Registry.get_window("default"))
    
    def show_scene(self, log, config, modes, stats, icons, foregrounds, font, launcher_cfg):
        """
        Set store menu.
        Base of menu control

        (Used for creating bg, items and icons)
        :rtype: object
        """
        
        # Logging information for debug.
        self.l_cfg = launcher_cfg
        self.foregrounds = foregrounds
        log.info("Store.__init__", "Player Opened the store")

        # Setup for store, the pause and controls.

        # Set storemode to ON (True)
        # and the pause ON (True). So the bubbles / ship can't moving.
        Registry.get_scene("GameScene").pause = True
        
        self.canvas.focus_set()
        self.canvas.bind("<Key-Down>", )
        
        # Background color (Can be changed by fill=<color-string>
        self.bg = self.canvas.create_rectangle(0, 0, config["width"], config["height"], fill="white")
        self.title = self.canvas.create_rectangle(-1, -1, config["width"] + 1, 48, fill="#373737")

        # Selection
        self.maximal = 3
        self.selected = 0

        # Info / icons dictionaries
        self.button = {}
        self.frame = {}
        self.item = {}
        self.name = {}
        self.d_icon = {}
        self.info = {}
        self.price = {}
        self.c_icon = {}
        self.coins = {}

        # Number of diamonds you have:
        self.vDiamonds = self.canvas.create_text(25, 25, text="Diamonds: " + str(stats["diamonds"]), fill="white", anchor=W,
                                            font=(font, 18))

        # Setups items and price.
        info = Reader("versions/"+launcher_cfg["versionDir"]+"/config/store.nzt").get_decoded()

        i = 0

        self.maximal = len(info) - 1

        y = 50
        x = 2
        
        index = 0

        for x in range(int(Registry.gameData["WindowWidth"]/200)):
            for y in range(50):
                self.button[index] = self.canvas2.create_rectangle(50 + x, 1 + y, 100 + x, 51 + y, outline="white",
                                                              fill="white")
                self.frame[index] = self.canvas2.create_rectangle(
                    0 + x, 0 + y, 190 + x, 140 + y, outline="#cfcfcf", fill="white")
                self.item[index] = self.canvas2.create_image(
                    100 + x, 26 + y, image=None)
                self.name[index] = self.canvas2.create_text(
                    100 + x, 75 + y, text=info[index]["name"], fill="#7f7f7f", anchor=CENTER)
                self.d_icon[index] = self.canvas2.create_image(
                    170 + x, 117 + y, image=Registry.get_storeicon(), anchor=E)
                self.info[index] = self.canvas2.create_text(
                    150 + x, 117 + y, text=str(int(info[index]["diamonds"])), fill="#7f7f7f", anchor=E)
                self.c_icon[index] = self.canvas2.create_image(
                    20 + x, 117 + y, image=icons["store-coin"], anchor=W)
                self.coins[index] = self.canvas2.create_text(
                    40 + x, 117 + y, text=info[index]["coins"], fill="#7f7f7f", anchor=W)

                self.price[i] = int(info[index]["diamonds"])

        for b in info:
            if y > config["height"] - 160:
                y -= 900
                x += 200
            self.button[i] = self.canvas.create_rectangle(50 + x, 1 + y, 100 + x, 51 + y, outline="white",
                                                     fill="white")
            self.frame[i] = self.canvas.create_rectangle(0 + x, 0 + y, 190 + x, 140 + y, outline="#cfcfcf",
                                                    fill="white")
            self.item[i] = self.canvas.create_image(100 + x, 26 + y, image=icons["store-pack"][i])
            self.name[i] = self.canvas.create_text(100 + x, 75 + y, text=b["name"], fill="#7f7f7f", anchor=CENTER)
            self.d_icon[i] = self.canvas.create_image(170 + x, 117 + y, image=icons["store-diamond"], anchor=E)
            self.info[i] = self.canvas.create_text(150 + x, 117 + y, text=str(int(b["diamonds"])), fill="#7f7f7f",
                                              anchor=E)
            self.price[i] = int(b["diamonds"])
            self.c_icon[i] = self.canvas.create_image(20 + x, 117 + y, image=icons["store-coin"], anchor=W)
            self.coins[i] = self.canvas.create_text(40 + x, 117 + y, text=b["coins"], fill="#7f7f7f", anchor=W)
            y += 150
            i += 1

        # Sets up the selected, the first.
        self.canvas.itemconfig(self.button[self.selected], fill="#7f7f7f", outline="#373737")
        self.canvas.itemconfig(self.frame[self.selected], fill="#7f7f7f", outline="#7f7f7f")
        self.canvas.itemconfig(self.info[self.selected], fill="#373737")
        self.canvas.itemconfig(self.coins[self.selected], fill="#373737")

        # Foreground for fade
        # self.fg = self.canvas.create_image(mid_x, mid_y, image=foregrounds["store-fg"])
        self.w = None
        self.b = None
        self.b2 = None
        self.close = None

    def set_selected(self, x):
        """
        Set selected item
        i = select var to be moved
            if i is 1 then switch one down
            else if i is -1 then switch one up
            can't switch if i is out of range.
        :param self.canvas:
        :param x:
        :return:
        """

        # Sets slected item color.
        if self.maximal >= self.selected + x > -1:
            # Sets old color

            self.canvas.itemconfig(self.button[self.selected], fill="white", outline="white")
            self.canvas.itemconfig(self.frame[self.selected], fill="white", outline="#cfcfcf")
            self.canvas.itemconfig(self.name[self.selected], fill="#7f7f7f")
            self.canvas.itemconfig(self.info[self.selected], fill="#7f7f7f")
            self.canvas.itemconfig(self.coins[self.selected], fill="#7f7f7f")

            # Sets selected variable
            self.selected += x

            # Sets new selected color
            self.canvas.itemconfig(self.button[self.selected], fill="#7f7f7f", outline="#7f7f7f")
            self.canvas.itemconfig(self.frame[self.selected], fill="#7f7f7f", outline="#121212")
            self.canvas.itemconfig(self.name[self.selected], fill="#373737")
            self.canvas.itemconfig(self.info[self.selected], fill="#373737")
            self.canvas.itemconfig(self.coins[self.selected], fill="#373737")

    def buy(self, log, modes, stats, bubble, backgrounds, temp, texts, commands, root, panels):
        """
        Buying a item and accepting buying the item
        activates the last phase.
        This phase sets the Diamonds and the Coins variables
        by buying a item.
        If you have no coins / diamonds it does nothing.
        """
        # Sets storemode controls
        modes["store"] = True

        # Deletes window
        self.w.destroy(modes, self.canvas)
        self.b.destroy()
        self.b2.destroy()
        # self.close.destroy()
        # Log information
        log.info("Store", "Player bought item nr. " + str(self.selected) + " for " + str(self.price[self.selected]) +
                 " diamonds, and" + self.canvas.itemcget(self.coins[self.selected], "text") + " coins.")

        # Checking if you have enough money / diamonds
        if stats["diamonds"] >= self.price[self.selected] and stats["coins"] >= int(self.canvas.itemcget(
                self.coins[self.selected], "text")):
            stats["diamonds"] -= self.price[self.selected]
            stats["coins"] -= int(self.canvas.itemcget(self.coins[self.selected], "text"))
            if self.selected == 0:
                Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] += 1000
            if self.selected == 1:
                stats["teleport"] += 1
            if self.selected == 2:
                stats["confusion"] = False
                stats["confusion_time"] = time()
                stats["paralyse"] = False
                stats["paralyse_time"] = time()
                State.set_state(self.canvas, log, stats, "Protect", backgrounds)
            if self.selected == 3:
                stats["diamonds"] += 1
            if self.selected == 4:
                stats["lives"] += 1
            if self.selected == 5:
                from qbubbles.extras import pop_bubble
                self.exit(self.canvas, log, modes, stats, temp, commands)
                n = 0
                self.canvas.bind_all("<ButtonPress-1>", lambda event: pop_bubble(self.canvas, log, bubble, commands,
                                                                            root, stats, temp, backgrounds, texts,
                                                                            event))
                while n < 3:
                    if temp["found-bubble"]:
                        n += 1
                        # print("Inner-"+str(n))
                    # print("Outer-"+str(n))
                    root.update()
                self.canvas.unbind_all("<ButtonPress-1>")
            if self.selected == 6:
                stats["lives"] += 2
            if self.selected == 7:
                State.set_state(self.canvas, log, stats, "SpeedBoost", backgrounds)
            if self.selected == 8:
                self.canvas.itemconfig(backgrounds["id"], image=backgrounds["special"])
                self.canvas.itemconfig(panels["game/top"], fill="#3f3f3f")
                stats["special-level"] = True
                stats["special-level_time"] = time() + 40
                log.info("State", "(CollFunc) Special Level State is ON!!!")
                # play_sound("versions/"+launcher_config["versionDir"]+"/assets/sounds/specialmode.mp3")
            if self.selected == 9:
                stats["scorestate"] = 2
                stats["scorestate_time"] = time() + randint(20, 40)
            if self.selected == 10:
                Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] += 10
            if self.selected == 11:
                Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] += 100
            if self.selected == 12:
                Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] += 200
            if self.selected == 13:
                Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] += 500
            self.canvas.itemconfig(self.vDiamonds, text="Diamonds: " + str(stats["diamonds"]))
            modes["window"] = False
        else:
            pass

    def buy_selected(self, config, modes, log, root, stats, bubble, backgrounds, texts, commands, temp, panels):
        """
        Creates a window for accepting to bought a item.
        """
        # Storemode controls off.
        modes["store"] = False

        mid_x = config["middle-x"]

        def storemode_on():
            modes["store"] = True

        # Creates window
        self.w = Window(self.canvas, self.l_cfg, config, title="Continue?", height=50, width=200, parent_is_store=True,
                        close_event=lambda: (
                            self.b.destroy(), self.b2.destroy(), None, storemode_on()), root=root)

        # Creates buttons
        log.debug("Store", "mid_x - 80 = " + str(mid_x - 80))
        self.b = Button(self.w.root, text="Yes", bg="#3c3c3c", fg="#afafaf", relief="flat", width=7,
                        command=lambda: self.buy(self.canvas, log, modes, stats, bubble, backgrounds, temp, texts,
                                                 commands, root, panels))
        self.b2 = Button(self.w.root, text="No", bg="#3c3c3c", fg="#afafaf", relief="flat", width=7,
                         command=lambda: (self.w.destroy(modes, self.canvas), self.b.destroy(), self.b2.destroy(), None,
                                          storemode_on()))
        # Places buttons
        self.w.child.append(self.b)
        self.w.child.append(self.b2)
        self.b.pack(side=LEFT, anchor=W, padx=10)
        self.b2.pack(side=RIGHT, anchor=E, padx=10)

        # Sets windowmode controls
        modes["window"] = True

    def exit(self, log, modes, stats, temp, commands):
        """
        Exits the store

        _todo: Removing it's self by exit. *edit: this is impossible
        """
        # Sets windowmode off. If it isn't off.
        modes["window"] = False

        # Deletes item-boxes and items.
        for i in range(self.maximal + 1):
            log.debug("Store", "Del attributes: " + str((self.button[i], self.frame[i], self.item[i], self.info[i],
                                                         self.d_icon[i], self.name[i], self.price[i],
                                                         self.c_icon[i], self.coins[i])))
            self.canvas.delete(self.button[i])
            self.canvas.delete(self.frame[i])
            if self.canvas.option_get("image", self.item[i]) is not None:
                self.canvas.delete(self.item[i])
            self.canvas.delete(self.info[i])
            self.canvas.delete(self.d_icon[i])
            self.canvas.delete(self.name[i])
            # c.delete(self.price[i])
            self.canvas.delete(self.c_icon[i])
            self.canvas.delete(self.coins[i])
        # Deletes back- and foreground.
        self.canvas.delete(self.bg)

        # Deletes the view of diamonds you have.
        self.canvas.delete(self.vDiamonds)
        self.canvas.delete(self.title)
        #
        # # Globals for the pause of game and control of store-items.
        # global pause, storemode
        #
        # # Deletes self-variables
        # del self.button, self.frame, self.item, self.info
        # del self.name, self.price, self.c_icon, self.coins
        # del self.bg, self.fg, self.vDiamonds
        #
        # # Pause and store controls.
        modes["pause"] = False
        modes["store"] = False

        # Pause variables.
        stats["scorestate_time"] = temp["scorestate-save"] + time()
        stats["secure_time"] = temp["secure-save"] + time()
        stats["timebreak_time"] = temp["timebreak-save"] + time()
        stats["confusion_time"] = temp["confusion-save"] + time()
        stats["slowmotion_time"] = temp["slowmotion-save"] + time()
        stats["paralyse_time"] = temp["paralyse-save"] + time()
        stats["shotspeed_time"] = temp["shotspeed-save"] + time()
        stats["notouch_time"] = temp["notouch-save"] + time()

        # Log.
        log.info("Store", "Player exited the store.")
        commands["store"] = None


class Window:
    """
    Creates a virtual window in the canvas.
    """

    def __init__(self, canvas, launcher_cfg, config, title="window", height=600, width=800, parent_is_store=False,
                 close_event=object, root=Tk):
        # Window variables
        self.canvas = canvas
        self.x1 = config["middle-x"] - width / 2
        self.y1 = config["middle-y"] - height / 2 - 20
        self.x2 = config["middle-x"] + width / 2
        self.y2 = config["middle-y"] + height / 2
        t_x = config["middle-x"]
        t_y = config["middle-y"] - height / 2 - 10
        self.selected_x = 0
        self.selected_y = 0
        self.id = list()
        self.is_store_parent = parent_is_store
        self.close_event = close_event

        # Creates window.
        self.title_mid = PhotoImage(file="versions/"+launcher_cfg["versionDir"]+"/assets/borders/titlebar-mid-focused.png")
        self.title_left = PhotoImage(file="versions/"+launcher_cfg["versionDir"]+"/assets/borders/titlebar-left-focused.png")
        self.title_right = PhotoImage(file="versions/"+launcher_cfg["versionDir"]+"/assets/borders/titlebar-right-focused.png")

        self.border_left = PhotoImage(file="versions/"+launcher_cfg["versionDir"]+"/assets/borders/frame-left-focused.png")
        self.border_right = PhotoImage(file="versions/"+launcher_cfg["versionDir"]+"/assets/borders/frame-right-focused.png")
        self.border_bottom_mid = PhotoImage(file="versions/"+launcher_cfg["versionDir"]+"/assets/borders/frame-bottom-mid-focused.png")
        self.border_bottom_left = PhotoImage(file="versions/"+launcher_cfg["versionDir"]+"/assets/borders/frame-bottom-left-focused.png")
        self.border_bottom_right = PhotoImage(file="versions/"+launcher_cfg["versionDir"]+"/assets/borders/frame-bottom-right-focused.png")
        self.close = PhotoImage(file="versions/"+launcher_cfg["versionDir"]+"/assets/borders/button-close.png")
        self.close_press = PhotoImage(file="versions/"+launcher_cfg["versionDir"]+"/assets/borders/button-close-prelight.png")

        self.id.append(canvas.create_rectangle(self.x1 - 6, self.y1 + 14, self.x2 + 6, self.y2 + 6, fill="lightgray",
                                               outline="#272727"))

        self.root = Frame(root, bg="black")
        self._root = canvas.create_window(self.x1-5, self.y1+15, window=self.root, anchor='nw', height=height+11, width=width+11)

        self.id.append(canvas.create_image(self.x1 - 4, self.y1, image=self.title_left))
        self.id.append(canvas.create_image(self.x2 + 4, self.y1, image=self.title_right))

        for i in range(0, int(width), 8):
            self.id.append(canvas.create_image(self.x1 + i, self.y1, image=self.title_mid))
            self.id.append(canvas.create_image(self.x1 + i, self.y2 + 7, image=self.border_bottom_mid))

        self.id.append(canvas.create_image(self.x2 - 2, self.y1, image=self.title_mid))
        self.id.append(canvas.create_image(self.x2 + 2, self.y2 + 7, image=self.border_bottom_mid))

        for i in range(16, int(height), 16):
            self.id.append(canvas.create_image(self.x1 - 7, self.y1 + i, image=self.border_left))
            self.id.append(canvas.create_image(self.x2 + 7, self.y1 + i, image=self.border_right))

        self.id.append(canvas.create_image(self.x1 - 7, self.y2 - 6, image=self.border_left))
        self.id.append(canvas.create_image(self.x2 + 7, self.y2 - 6, image=self.border_right))

        self.id.append(canvas.create_image(self.x1 - 7, self.y2 + 7, image=self.border_bottom_left))
        self.id.append(canvas.create_image(self.x2 + 7, self.y2 + 7, image=self.border_bottom_right))
        self.id.append(canvas.create_image(self.x2 - 5, self.y1 - 3, image=self.close))
        # button1PressIndex.append((self.x2 - 5 - self.close.width() / 2, self.x2 - 5 + self.close.width() / 2,
        #                           self.y1 - 3 - self.close.height() / 2, self.y1 - 3 + self.close.height() / 2,
        #                           self.closeButtonEvent, None))
        # button1ReleaseIndex.append((self.x2 - 5 - self.close.width() / 2, self.x2 - 5 + self.close.width() / 2,
        #                             self.y1 - 3 - self.close.height() / 2, self.y1 - 3 + self.close.height() / 2,
        #                             self.closeButtonEvent, None))

        # self.id.append(c.create_rectangle(self.x1, self.y1, self.x2, self.y1 + 20, fill="#272727", outline="#272727"))

        # Creates Title
        self.id.append(canvas.create_text(t_x, t_y - 12, text=title, fill="#D9D9D9", anchor=CENTER))

        # Sets child-variables.
        self.child = []

    def close_button_press_event(self, canvas):
        canvas.itemconfig(self.id[-2], image=self.close_press)

    def close_button_event(self, canvas, modes):
        self.close_event()
        self.destroy(canvas, modes)

    def destroy(self, modes, canvas):
        """
        Destroys (deletes) virtual window and child modules.
        If the child-id isn't a child, it will raise a exception.
        """

        # Deletes window
        for i in self.id:
            try:
                i.destroy()
            except AttributeError:
                canvas.delete(i)

        # Deletes title

        # Deletes all childs.
        for i in self.child:
            try:
                canvas.delete(i)
            except TclError:
                i.destroy()
            # except TclError:
            #     # If it isn't a Canvas-item.
            #     log.fatal("Window", "Child isn't a child. Id: " + str(i) + ".")
            # raise ChildProcessError("Child isn't a child. Id: " + str(i) + ".")
        modes["window"] = False
        canvas.delete(self._root)
        # self.root.destroy()
        if self.is_store_parent:
            modes["store"] = True

    class Label:
        """
        Label-child for the virtual window.
        """

        def __init__(self, canvas, parent, x, y, text="", color="black", font=(), anchor=CENTER):
            self.canvas = canvas
            # Creates label.
            self.id = self.canvas.create_text(x, y, text=text, fill=color, font=font, anchor=anchor)

            # Creates label-configuraion variables
            self.__text = text
            self.__color = color
            self.__font = font
            self.__anchor = anchor

            # Creates a child by its parent.
            parent.child.append(self.id)

        def get(self):
            """
            Gets text value of the Label.
            :return:
            """

            # Gets text if the label.
            return self.canvas.itemcget(self.id, "text")

        def config(self, text=None, color=None, font=None, anchor=None):
            """
            Configure Label.
            :param text:
            :param color:
            :param font:
            :param anchor:
            """
            if text is None:
                text = self.__text
            if color is None:
                color = self.__color
            if font is None:
                font = self.__font
            if anchor is None:
                anchor = self.__anchor
            self.canvas.itemconfig(self.id, text=text, fill=color, font=font, anchor=anchor)
            self.__text = text
            self.__color = color
            self.__font = font
            self.__anchor = anchor

        def destroy(self):
            """
            Destroys Label
            """
            self.canvas.delete(self.id)


class CheatEngine:
    def __init__(self):
        """
        Cheat Engine init. Sets only the 'text' variable on the self.
        """
        self.text = ""
        self.text_id = None
        self.a = None

    def event_handler(self, canvas, modes, stats, config, temp, log, backgrounds, bubble, event, bub, font):
        """
        The "/" key event obj.
        :param font:
        :param log:
        :param log:
        :param bub:
        :param bubble:
        :param backgrounds:
        :param temp:
        :param config:
        :param stats:
        :param modes:
        :param canvas:
        :rtype: object
        :param event:
        """
        modes["pause"] = True
        modes["cheater"] = True
        temp["scorestate-save"] = stats["scorestate_time"] - time()
        temp["secure-save"] = stats["secure_time"] - time()
        temp["timebreak-save"] = stats["timebreak_time"] - time()
        temp["confusion-save"] = stats["confusion_time"] - time()
        temp["slowmotion-save"] = stats["slowmotion_time"] - time()
        temp["paralyse-save"] = stats["paralyse_time"] - time()
        temp["shotspeed-save"] = stats["shotspeed_time"] - time()
        temp["notouch-save"] = stats["notouch_time"] - time()
        temp["special-level-save"] = stats["special-level_time"] - time()

        self.text = ""
        self.text_id = canvas.create_text(10, config["height"] - 100, text="> ", font=(font, 24), anchor=SW)
        self.a = canvas.bind("<Key>",
                             lambda: self.input_event_handler(canvas, log, stats, backgrounds, bubble, event,
                                                              config, bub,
                                                              temp, modes))
        # c.bind_all("<Return>", self.ExecuteEventHandler)

    def close(self, canvas, stats, modes, temp):
        """
        If closing the command input. It will be done here.
        :rtype: object
        """
        canvas.delete(self.text_id)
        modes["pause"] = False
        modes["cheater"] = False
        stats["scorestate_time"] = temp["scorestate-save"] + time()
        stats["secure_time"] = temp["secure-save"] + time()
        stats["timebreak_time"] = temp["timebreak-save"] + time()
        stats["confusion_time"] = temp["confusion-save"] + time()
        stats["slowmotion_time"] = temp["slowmotion-save"] + time()
        stats["paralyse_time"] = temp["paralyse-save"] + time()
        stats["shotspeed_time"] = temp["shotspeed-save"] + time()
        stats["notouch_time"] = temp["notouch-save"] + time()

    def input_event_handler(self, canvas, log, stats, backgrounds, bubble, event, config, bub, temp, modes):
        """
        Keys input eventhandler. All alphabetical symobols will be shown.
        And will also be inserted in the CheatEngine().text variable.

        The Backspace is also used to delete the most right character.
        :param log:
        :param log:
        :param modes:
        :param temp:
        :param bub:
        :param config:
        :param canvas:
        :param stats:
        :param backgrounds:
        :param bubble:
        :rtype: object
        :param event:
        """
        if event.keysym == "BackSpace":
            self.text = self.text[0:-1]
        if event.keysym == "space":
            self.text += " "
        if len(event.char) > 0:
            if 127 > ord(event.char) > 32:
                self.text += event.char
        if event.keysym == "Return":
            self.execute_event_handler(canvas, log, stats, backgrounds, bubble, config, bub, modes, temp)
        # print(event.char)
        canvas.itemconfig(self.text_id, text="> " + self.text)
        canvas.update()

    @staticmethod
    def add_level_key(stats, config, bubble, canvas, modes, bub, params):
        """
        Adds Level Key. This is only used for the Cheat.
        :param bub:
        :param modes:
        :param canvas:
        :param bubble:
        :param config:
        :param stats:
        :rtype: object
        :param params:
        """
        from qbubbles.bubble import create_bubble
        if len(params) == 1:
            if params[0].isnumeric() and "." not in params[0]:
                a = int(params[0])
                if 0 <= a < 10:
                    for i in range(0, a):
                        Thread(None, lambda: create_bubble(stats, config, bub, canvas, bubble)).start()

    @staticmethod
    def clean_all_bubbles(bubble, canvas, params):
        """
        Cleans all bubbles. This is a Cheat.
        :param canvas:
        :param bubble:
        :rtype: object
        :param params:
        """
        from qbubbles.bubble import clean_all
        if len(params) == 0:
            Thread(None, lambda: clean_all(bubble, canvas)).start()

    @staticmethod
    def add_bubble(stats, config, bub, canvas, bubble, modes, params):
        """
        Adds a bubble using this cheat.
        :param modes:
        :param bubble:
        :param canvas:
        :param bub:
        :param config:
        :param stats:
        :rtype: object
        :param params:
        """
        from qbubbles.bubble import create_bubble
        act = ["Double", "Kill", "Triple", "Normal", "SpeedDown", "SpeedUp", "Up", "Ultimate", "Teleporter",
               "SlowMotion", "HyperMode", "Protect", "ShotSpdStat", "TimeBreak", "DoubleState", "Confusion", "Paralyse",
               "StoneBub", "NoTouch", "Coin", "Diamond"]
        if 2 >= len(params) >= 1:
            if params[0] in act:
                p = params[0]
                i = 0
                if p == "Normal":
                    i = 0
                elif p == "Double":
                    i = 800
                elif p == "Kill":
                    i = 830
                elif p == "Triple":
                    i = 930
                elif p == "SpeedUp":
                    i = 940
                elif p == "SpeedDown":
                    i = 950
                elif p == "Up":
                    i = -2
                elif p == "Ultimate":
                    i = 973
                elif p == "DoubleState":
                    i = 974
                elif p == "Protect":
                    i = 979
                elif p == "SlowMotion":
                    i = 981
                elif p == "TimeBreak":
                    i = 984
                elif p == "HyperMode":
                    i = 1100
                elif p == "ShotSpdStat":
                    i = 1101
                elif p == "Confusion":
                    i = 985
                elif p == "Paralyse":
                    i = 1085
                elif p == "Teleporter":
                    i = 1120
                elif p == "Diamond":
                    i = 1121
                elif p == "Coin":
                    i = 1124
                elif p == "NoTouch":
                    i = 1130
            else:
                i = 0
            if len(params) == 2:
                p = params[1]
            else:
                p = "1"
            if p.isnumeric():
                if i:
                    for _ in range(int(float(p))):
                        Thread(None, lambda: create_bubble(stats, config, bub, canvas, bubble, float(i))).start()
        if len(params) == 5:
            i = 0
            if params[0] in act:
                p = params[0]
                if p == "Normal":
                    i = 0
                elif p == "Double":
                    i = 800
                elif p == "Kill":
                    i = 830
                elif p == "Triple":
                    i = 930
                elif p == "SpeedUp":
                    i = 940
                elif p == "SpeedDown":
                    i = 950
                elif p == "Up":
                    i = -2
                elif p == "Ultimate":
                    i = 973
                elif p == "DoubleState":
                    i = 974
                elif p == "Protect":
                    i = 979
                elif p == "SlowMotion":
                    i = 981
                elif p == "TimeBreak":
                    i = 984
                elif p == "HyperMode":
                    i = 1100
                elif p == "ShotSpdStat":
                    i = 1101
                elif p == "Confusion":
                    i = 985
                elif p == "Paralyse":
                    i = 1085
                elif p == "Teleporter":
                    i = 1120
                elif p == "Diamond":
                    i = 1121
                elif p == "Coin":
                    i = 1124
                elif p == "NoTouch":
                    i = 1130
            else:
                i = 0
            if params[1].isnumeric() and params[2].isnumeric() and params[3].isnumeric() and params[4].isnumeric():
                if i:
                    for _ in range(int(float(params[1]))):
                        Thread(None, lambda: create_bubble(stats, config, bub, canvas, bubble, i, float(params[2]),
                                                           float(params[3]), float(params[4]))).start()

    @staticmethod
    def add_lives(stats, params):
        """
        Adds lives. (Cheat.)
        :param stats:
        :rtype: object
        :param params:
        """
        if len(params) == 1:
            if params[0].isnumeric():
                stats["lives"] += int(float(params[0]))

    @staticmethod
    def add_state(canvas, log, stats, params, backgrounds):
        """
        Adds a State. Yeah, this is also a cheat.
        :param log:
        :param log:
        :param backgrounds:
        :param stats:
        :param canvas:
        :rtype: object
        :param params:
        """
        if len(params) == 1:
            State.set_state(canvas, log, stats, params[0], backgrounds)

    @staticmethod
    def add_coins(stats, params):
        if len(params) == 1:
            if params[0].isnumeric():
                stats["coins"] += int(float(params[0]))
        print(len(params))
        print(params[0].isnumeric())
        print(int(float(params[0])))

    def execute_event_handler(self, canvas, log, stats, backgrounds, bubble, config, bub, modes, temp):
        """
        If you pressed the Return key. This will be executed.
        :param log:
        :param log:
        :param temp:
        :param modes:
        :param bub:
        :param config:
        :param bubble:
        :param backgrounds:
        :param stats:
        :param canvas:
        :rtype: object
        """
        from qbubbles.bubble import clean_all
        cmd_and_param_list = self.text.split(sep=" ")
        command = cmd_and_param_list[0]
        params = cmd_and_param_list[1:]
        print(command)
        print(params)
        if command == "/AddLevelKey":
            self.add_level_key(stats, config, bubble, canvas, params=params, modes=modes, bub=bub)
        elif command == "/CleanAllBubbles":
            clean_all(bubble, canvas)
        elif command == "/AddBubble":
            self.add_bubble(stats, config, bub, canvas, bubble, modes, params)
        elif command == "/AddLives":
            self.add_lives(stats, params)
        elif command == "/AddState":
            self.add_state(canvas, log, stats, params, backgrounds)
        elif command == "/AddCoins":
            self.add_coins(stats, params)
        else:
            pass
        self.close(canvas, stats, modes, temp)
