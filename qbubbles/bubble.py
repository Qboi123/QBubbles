from qbubbles.ammo import *
from qbubbles.components import *
from qbubbles.info import *


def place_bubble(c, bub, x, y, r, act):
    """
    Places a bubble.
    The bubble can't moving or removed (only by closing game).
    :param c:
    :param bub:
    :param x:
    :param y:
    :param r:
    :param act:
    """

    if act == "Normal":
        return c.create_image(x, y, image=bub["Normal"][r * 2])
    if act == "Double":
        return c.create_image(x, y, image=bub["Double"][r * 2])
    if act == "Kill":
        return c.create_image(x, y, image=bub["Kill"][r * 2])
    if act == "Triple":
        return c.create_image(x, y, image=bub["Triple"][r * 2])
    if act == "SpeedUp":
        return c.create_image(x, y, image=bub["SpeedUp"][r * 2])
    if act == "SpeedDown":
        return c.create_image(x, y, image=bub["SpeedDown"][r * 2])
    if act == "Up":
        return c.create_image(x, y, image=bub["Up"][r * 2])
    if act == "Ultimate":
        return c.create_image(x, y, image=bub["Ultimate"][r * 2])
    if act == "DoubleState":
        return c.create_image(x, y, image=bub["DoubleState"][r * 2])
    if act == "Protect":
        return c.create_image(x, y, image=bub["Protect"][r * 2])
    if act == "SlowMotion":
        return c.create_image(x, y, image=bub["SlowMotion"][r * 2])
    if act == "TimeBreak":
        return c.create_image(x, y, image=bub["TimeBreak"][r * 2])
    if act == "Confusion":
        return c.create_image(x, y, image=bub["Confusion"][r * 2])
    if act == "HyperMode":
        return c.create_image(x, y, image=bub["HyperMode"][r * 2])
    if act == "ShotSpdStat":
        return c.create_image(x, y, image=bub["ShotSpdStat"][r * 2])
    if act == "Teleporter":
        return c.create_image(x, y, image=bub["Teleporter"][r * 2])
    if act == "Coin":
        return c.create_image(x, y, image=bub["Coin"])
    if act == "NoTouch":
        return c.create_image(x, y, image=bub["NoTouch"][r * 2])
    if act == "LevelKey":
        return c.create_image(x, y, image=bub["Key"][60])
    if act == "Paralyse":
        return c.create_image(x, y, image=bub["Paralyse"][r * 2])
    if act == "SpecialKey":
        return c.create_image(x, y, image=bub["SpecialKey"][48])
    if act == "Diamond":
        return c.create_image(x, y, image=bub["Diamond"][36])
    if act == "StoneBub":
        return c.create_image(x, y, image=bub["StoneBub"][r * 2])
    if act == "Present":
        return c.create_image(x, y, image=bub["Present"][40])


def create_bubble(stats, config, bub, c, bubble, i=None, x=None, y=None, r=None, s=None):
    """
    Creates a bubble that can moving and removing by touching with the ship
    :param s:
    :param bubble:
    :param c:
    :param bub:
    :param config:
    :param stats:
    :param i:
    :param x:
    :param y:
    :param r:
    Todo: Add more bubbles.
    """
    from random import randint
    if x is None:
        x = config["width"] + config["Bubble"]["screen-gap"]
    else:
        x = x
    if r is None:
        r = randint(int(config["Bubble"]["min-radius"]), int(config["Bubble"]["max-radius"]))
    else:
        r = r
    if y is None:
        y = randint(72 + r, (config["height"] - r))
    else:
        y = y
    if i is None:
        i = randint(0, 1600)
    else:
        i = i
    if Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["level"] <= 100:
        level_dat = Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["level"]
    else:
        level_dat = 100
    if 0 <= i < 800:
        ids = [c.create_image(x, y, image=bub["Normal"][r * 2])]
        act = "Normal"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) - 3, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]))
        hardness = 1
    elif 800 <= i < 830:
        ids = [c.create_image(x, y, image=bub["Double"][r * 2])]
        act = "Double"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) - 3, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]))
        hardness = 1
    elif 830 <= i < 930:
        ids = [c.create_image(x, y, image=bub["Kill"][r * 2])]
        act = "Kill"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) - 3, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]))
        hardness = 1
    elif 930 <= i < 940:
        ids = [c.create_image(x, y, image=bub["Triple"][r * 2])]
        act = "Triple"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 2, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 6)
        hardness = 1
    elif 940 <= i < 950:
        ids = [c.create_image(x, y, image=bub["SpeedUp"][r * 2])]
        act = "SpeedUp"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]), int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 3)
        hardness = 1
    elif 950 <= i < 960:
        ids = [c.create_image(x, y, image=bub["SpeedDown"][r * 2])]
        act = "SpeedDown"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]), int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 3)
        hardness = 1
    elif 960 <= i < 965:
        if Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["lives"] < 7:
            ids = [c.create_image(x, y, image=bub["Up"][r * 2])]
            act = "Up"
            spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]), int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 3)
            hardness = 1
        else:
            ids = [c.create_image(x, y, image=bub["Normal"][r * 2])]
            act = "Normal"
            spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) - 3, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]))
            hardness = 1
    elif 973 <= i < 974:
        ids = [c.create_image(x, y, image=bub["Ultimate"][r * 2])]
        act = "Ultimate"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 4, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 8)
        hardness = 1
    elif 974 <= i < 976:
        ids = [c.create_image(x, y, image=bub["DoubleState"][r * 2])]
        act = "DoubleState"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 4, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 8)
        hardness = 1
    elif 979 <= i < 981:
        ids = [c.create_image(x, y, image=bub["Protect"][r * 2])]
        act = "Protect"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 4, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 8)
        hardness = 1
    elif 981 <= i < 984:
        ids = [c.create_image(x, y, image=bub["SlowMotion"][r * 2])]
        act = "SlowMotion"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 4, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 8)
        hardness = 1
    elif 984 <= i < 985:
        ids = [c.create_image(x, y, image=bub["TimeBreak"][r * 2])]
        act = "TimeBreak"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 4, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 8)
        hardness = 1
    elif 1100 <= i < 1101:
        ids = [c.create_image(x, y, image=bub["HyperMode"][r * 2])]
        act = "HyperMode"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) - 3, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]))
        hardness = 1
    elif 1101 <= i < 1120:
        ids = [c.create_image(x, y, image=bub["ShotSpdStat"][r * 2])]
        act = "ShotSpdStat"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) - 3, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]))
        hardness = 1
    elif 985 <= i < 1085:
        ids = [c.create_image(x, y, image=bub["Confusion"][r * 2])]
        act = "Confusion"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) - 3, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]))
        hardness = 1
    elif 1085 <= i < 1100:
        ids = [c.create_image(x, y, image=bub["Paralyse"][r * 2])]
        act = "Paralyse"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) - 3, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]))
        hardness = 1
    elif 1100 <= i < 1101:
        ids = [c.create_image(x, y, image=bub["HyperMode"][r * 2])]
        act = "HyperMode"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) - 3, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]))
        hardness = 1
    elif 1101 <= i < 1120:
        ids = [c.create_image(x, y, image=bub["ShotSpdStat"][r * 2])]
        act = "ShotSpdStat"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) - 3, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]))
        hardness = 1
    elif 1120 <= i < 1121 and Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["level"] > 19:
        ids = [c.create_image(x, y, image=bub["Teleporter"][r * 2])]
        act = "Teleporter"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]), int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 2)
        hardness = 1
    elif 1121 <= i < 1123 and Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["level"] > 4:
        ids = [c.create_image(x, y, image=bub["Diamond"][36])]
        r = 18
        act = "Diamond"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 2, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 4)
        hardness = 1
    elif 1124 <= i < 1130 and Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["level"] > 4:
        ids = [c.create_image(x, y, image=bub["Coin"])]
        r = 20
        act = "Coin"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]), int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 2)
        hardness = 2
    elif 1130 <= i < 1150 and Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["level"] > 4:
        r = 20
        ids = [c.create_image(x, y, image=bub["NoTouch"][r * 2])]
        act = "NoTouch"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]), int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 2)
        hardness = 1
    elif 1150 <= i < 1160 and Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["level"] > 4:
        r = 20
        ids = [c.create_image(x, y, image=bub["Present"][40])]
        act = "Present"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]), int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 2)
        hardness = 1
    elif 1160 <= i < 1263 + (197 * level_dat / 100):
        ids = [c.create_image(x, y, image=bub["StoneBub"][r * 2])]
        act = "StoneBub"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 4, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 8)
        hardness = 3 + int(level_dat / 2)
        # elif 1360 <= i < ???:
    elif 1460 <= i < 1491:
        ids = [c.create_image(x, y, image=bub["Coin"])]
        r = 20
        act = "Coin"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]), int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 2)
        hardness = 2
    elif 1491 <= i < 1492:
        ids = [c.create_image(x, y, image=bub["SpecialKey"][48])]
        r = 24
        act = "SpecialKey"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 5, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 8)
        hardness = 1
    elif i == -1:
        ids = [c.create_image(x, y, image=bub["Key"][60])]
        r = 26
        act = "LevelKey"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 4, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 8)
        hardness = 1
    elif i == -2:
        ids = [c.create_image(x, y, image=bub["Up"][r * 2])]
        act = "Up"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]), int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) + 3)
        hardness = 1
    else:
        ids = [c.create_image(x, y, image=bub["Normal"][r * 2])]
        act = "Normal"
        spd = randint(int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]) - 3, int(stats["Sprites"]["qbubbles:bubble"]["speedMultiplier"]))
        hardness = 1

    if s is not None:
        spd = s
    bubble["bub-special"].append(False)
    bubble["bub-index"].append(i)
    bubble["bub-position"].append([x, y])
    bubble["bub-hardness"].append(hardness)
    bubble["bub-action"].append(act)
    bubble["bub-id"].append(ids)
    bubble["bub-radius"].append(r)
    bubble["bub-speed"].append(spd)
    index = bubble["bub-id"].index(ids, 0, len(bubble["bub-id"]))
    try:
        if not bubble["active2"][index]:
            bubble["active2"][index] = True
            bubble["active"] += 1
    except IndexError:
        pass
    # Thread(None, lambda: movebubble_thread(ids, bubble, spd, act, ids[0], r, c, stats, input_modes)).start()


def move_bubbles(bubble, stats, root, canvas):
    """
    The base of motion for the bubbles
    """
    try:
        for i in range(len(bubble["bub-id"])):
            Thread(None, lambda: Collision.move_bubble(i, bubble, canvas, stats, root)).start()
    except IndexError:
        pass
    except TclError:
        exit(0)


def del_bubble(index, bubble, canvas):
    """
    Removes a bubble.
    :param canvas:
    :param bubble:
    :param index:
    """
    del bubble["bub-radius"][index]
    del bubble["bub-speed"][index]
    for j in bubble["bub-id"][index]:
        canvas.delete(j)
    del bubble["bub-id"][index]
    if bubble["bub-action"][index] == "LevelKey":
        bubble["key-active"] = False
    del bubble["bub-action"][index]
    del bubble["bub-hardness"][index]
    del bubble["bub-position"][index]
    del bubble["bub-index"][index]


def clean_up_bubs(bubble, canvas):
    """
    Removes bubbles that's out of screen. If x is lower than -100
    """
    try:
        for index in range(len(bubble["bub-id"]) - 1, -1, -1):
            x, y = get_coords(canvas, bubble["bub-id"][index][0])
            if x < -100:
                # Checks if the Level-key is active.
                # If it's active then sets it the variable
                # for the key-bubble to off.
                if bubble["bub-action"][index] == "LevelKey":
                    bubble["key-active"] = False
                del_bubble(index, bubble, canvas)
    except IndexError:
        pass


def clean_level_keys(bubble, canvas):
    """
    Removes all Level-Keybubble.
    :param bubble:
    :param canvas:
    :return:
    """
    for index in range(len(bubble["bub-action"]) - 1, -1, -1):
        try:
            if bubble["bub-action"][index] == "LevelKey":
                del_bubble(index, bubble, canvas)
        except TypeError:
            pass
        except IndexError:
            pass


class Collision:
    def __init__(self):
        self.shot = None
        self.bub = None

    @staticmethod
    def move_bubble(index, bubble, canvas, stats, root):
        """
        Moves 1 bubble.
        :param root:
        :param stats:
        :param canvas:
        :param bubble:
        :param index:
        :rtype: object
        """
        try:
            for j in range(len(bubble["bub-id"][index]) - 1, -1, -1):
                if not bubble["bub-action"][index] == "Null":
                    if stats["Effects"]["slowmotion"]:
                        canvas.move(bubble["bub-id"][index][j], -bubble["bub-speed"][index] / 10, 0)
                    else:
                        canvas.move(bubble["bub-id"][index][j], -bubble["bub-speed"][index], 0)
                    root.update()
                x, y, = get_coords(canvas, bubble["bub-id"][index][j])
                bubble["bub-position"][index] = [x, y]
                canvas.update()
        except IndexError:
            pass
        except TclError:
            exit(0)
        except AttributeError:
            exit(0)

    @staticmethod
    def move_ammo(index, ammo, canvas, log):
        """
        Moves 1 ammo.
        :param log:
        :param canvas:
        :param ammo:
        :param index:
        :rtype: object
        """
        try:
            canvas.move(ammo["ammo-id"][index], ammo["ammo-speed"][index], 0)
        except IndexError:
            log.warning("move_ammo", "Can't move ammo index '" + str(index) + "'.")

    @staticmethod
    def coll_func(index, canvas, commands, root, log, stats, bubscore, action, bubble, backgrounds, texts, panels,
                  accept_negative):
        """
        Collision.
        All bubbles have a function.
        This Method sets a state or sets a variable.
        :param panels:
        :param log:
        :param log:
        :param index:
        :param texts:
        :param commands:
        :param root:
        :param canvas:
        :param backgrounds:
        :param bubble:
        :param bubscore:
        :param stats:
        :param action:
        :param accept_negative:
        :return:
        """
        if action == "Normal":
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] += bubscore * stats["Effects"]["scorestate"]
        if action == "Double":
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] += bubscore * 2 * stats["Effects"]["scorestate"]
        if action == "Triple":
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] += bubscore * 3 * stats["Effects"]["scorestate"]
        if (not stats["Effects"]["secure"]) and accept_negative:
            if action == "Kill":
                Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["lives"] -= 1
            if action == "Min":
                Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] -= bubscore
            if action == "SpeedDown":
                if Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["speed"] == 5:
                    return
                Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["speed"] -= 5
            if action == "Confusion":
                State.set_state(canvas, log, stats, "Confusion", backgrounds)
            if action == "Paralyse":
                State.set_state(canvas, log, stats, "Paralyse", backgrounds)
            if action == "NoTouch":
                Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] += bubscore * stats["Effects"]["scorestate"]
                State.set_state(canvas, log, stats, action, backgrounds)
        if action == "DoubleState":
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "TripleState":
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "SpeedUp":
            if Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["speed"] == 20:
                return
            elif Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["speed"] == 25:
                return
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["speed"] += 5
        if action == "Up":
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["lives"] += 1
        if action == "Protect":
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "SlowMotion":
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "TimeBreak":
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "Ultimate":
            if Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["lives"] < 7:
                Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["lives"] += 1
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["speed"] = 25
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "HyperMode":
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["lives"] += 2
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["speed"] = 25
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] += bubscore * 30 * stats["Effects"]["scorestate"]
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "ShotSpdStat":
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] += bubscore * stats["Effects"]["scorestate"]
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "Diamond":
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Money"]["diamonds"] += 1
        if action == "Coin":
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Money"]["coins"] += 1
        if action == "Teleporter":
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Abilities"]["teleports"] += 1
        if action == "StoneBub":
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] += int((bubscore * bubble["bub-hardness"][index]))
        if action == "LevelKey":
            Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["level"] += 1
            # clean_level_keys()
            bubble["key-active"] = False
            view_level(canvas, root, texts, Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["level"])
        if action == "Present":
            commands["present"] = True
        # play_sound("versions/"+launcher_config["versionDir"]+"/assets/sounds/bubpop.mp3")
        if action == "SpecialKey":
            canvas.itemconfig(backgrounds["id"], image=backgrounds["special"])
            canvas.itemconfig(panels["game/top"], fill="#3f3f3f")
            stats["Effects"]["special-level"] = True
            stats["Effects"]["special-level_time"] = time() + 30
            log.info("State", "(CollFunc) Special Level State is ON!!!")
            # play_sound("versions/"+self.launcher_config["versionDir"]+"/assets/sounds/specialmode.mp3")
        log.debug("CollFunc", "Bubble popped with id: "+str(index)+" | action: "+action)

    @staticmethod
    def clean_up_bub(canvas, index, bubble, config, log):
        """
        Cleans 1 bubble.
        :param log:
        :param config:
        :param bubble:
        :param canvas:
        :rtype: object
        :param index:
        """
        try:
            x, y = get_coords(canvas, bubble["bub-id"][index][0])
            if x < -config["Bubble"]["screen-gap"]:
                # Checks if the Level-key is active.
                # If it's active then sets it the variable
                # for the key-bubble to off.
                if bubble["bub-action"][index] == "LevelKey":
                    bubble["keyactive"] = False
                del_bubble(index, bubble, canvas)
        except IndexError as e:
            log.error("Collision.clean_up_bub", "IndexError: '"+e.args[0]+"' on line no. "+str(e.__traceback__.tb_lineno))

    @staticmethod
    def clean_up_shot(canvas, index, ammo, config):
        """
        Cleans 1 shot.
        :param canvas:
        :param config:
        :param ammo:
        :rtype: object
        :param index:
        """
        x, y = get_coords(canvas, ammo["ammo-id"][index])
        if x > config["width"] + config["Bubble"]["screen-gap"]:
            del_ammo(canvas, index, ammo)

    def check_collision(self, root, commands, bubble, config, stats, ammo, ship, canvas, log, backgrounds, texts,
                        panels):
        """
        Collision bubble by touching or shooting the bubble
        :rtype: object
        """
        from qbubbles.extras import distance, replace_list
        from threading import Thread
        for index_bub in range(len(bubble["bub-id"].copy()) - 1, -1, -1):
            # print(distance(canvas, log, ship["id"], bubble["bub-id"][index_bub][0]) - (config["Game"]["ship-radius"] + bubble["bub-radius"][index_bub]))
            self.bub = index_bub
            try:
                if distance(canvas, log, ship["id"], bubble["bub-id"][index_bub][0]) < (
                        config["Game"]["ship-radius"] + bubble["bub-radius"][index_bub]):
                    if not stats["Effects"]["notouch"]:
                        # Sets score / status etc. and deletes bubble
                        if bubble["bub-hardness"][index_bub] == 1:
                            Thread(None, lambda: self.coll_func(index_bub, canvas, commands, root, log, stats,
                                                                (bubble["bub-radius"][index_bub] +
                                                                 bubble["bub-speed"][index_bub]),
                                                                bubble["bub-action"][index_bub], bubble, backgrounds,
                                                                texts, panels, True)).start()
                            del_bubble(index_bub, bubble, canvas)
                        elif bubble["bub-hardness"][index_bub] > 1:
                            replace_list(bubble["bub-hardness"], index_bub, bubble["bub-hardness"][index_bub] - 1)
                if not stats["Effects"]["timebreak"]:
                    self.move_bubble(index_bub, bubble, canvas, stats, root)
                    canvas.update()
                    self.clean_up_bub(canvas, index_bub, bubble, config, log)
                # Collision with ammo
                for ammo_index in range(len(ammo["ammo-id"].copy()) - 1, -1, -1):
                    pass
            except TypeError:
                pass
            except IndexError:
                pass
            except TclError:
                exit(0)
            except AttributeError:
                exit(0)


def movebubble_thread(index, bubble, speed, action, id, radius, canvas, stats, modes):
    # print("start")
    index = bubble["bub-id"].index(index, 0, len(bubble["bub-id"]))
    while True:
        try:
            # print("ID: "+str(index)+"phase 1")
            if not stats["Effects"]["timebreak"] and not modes["pause"]:
                # print("ID: "+str(index)+"phase 2")
                if not action == "Null":
                    # print("ID: "+str(index)+"phase 3")
                    if stats["Effects"]["slowmotion"]:
                        canvas.move(id, -speed / 10, 0)
                        # print("ID: "+str(index)+'phase 4a')
                    else:
                        canvas.move(id, -speed, 0)
                        # list.
                        # print("phase 4b")
                    # print("ID: "+str(index)+str(bubble["active2"]))
                    # print("ID: "+str(index)+str(len(bubble["active2"])))
                    if not bubble["active2"][index]:
                        bubble["active2"][index] = True
                        bubble["active"] += 1
                        print(bubble["active"])
                    # print("Active:", bubble["active"])
                    # print("ID: "+str(index)+"phase 5")
                try:
                    x, y, = get_coords(canvas, id)
                    # print("ID: " + str(index) + "phase 6")
                    bubble["bub-position"][index] = [x, y]
                    # print("ID: "+str(index)+"phase 7")
                    # print(radius)
                    if x < -radius:
                        del_bubble(index, bubble, canvas)
                        return
                except IndexError:
                    pass
                # print("ID: "+str(index)+"move")
                canvas.update()
        except IndexError as e:
            print("ID: "+str(index), e.args)
            # print(bubble["bub-id"][0][0])
            return
        except TclError:
            # print("exit")
            exit(0)
        except AttributeError:
            # print("exit")
            exit(0)


def clean_all(bubble, canvas):
    """
    Deletes removes bubbles out of the game.
    """
    for i in len(bubble["bub-id"]) - 1, -1, -1:
        del_bubble(i, bubble, canvas)
