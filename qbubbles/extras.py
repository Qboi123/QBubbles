# import pygame
from tkinter import TclError


def dict2class(obj: dict):
    import sys
    class DictClass:
        def __init__(self):
            pass

    print("Object: %s" % obj)

    dictClass = DictClass()

    print("Keys: %s" % list(obj.keys()))

    for index in range(len(list(obj.keys()))):
        key = list(obj.keys())[index]
        value = list(obj.values())[index]
        print("Key: %s | Value: %s" % (key, value))
        if type(key) == dict:
            print("ERROR: Key is a Dict!", file=sys.stderr)
            exit(1)
        if type(value) == dict:
            value = dict2class(value)
        dictClass.__dict__[key] = value

    return dictClass


class Logging:
    """
    Logging class for logs
    """

    def __init__(self, save_path="", stdout=True, stderr=False):
        self.stderr = stderr
        self.stdout = stdout
        self.save_path = save_path
        return
        # from time import strftime
        # import os
        #
        # self.os = os
        # self.tme = strftime
        # self.save_file = save_path + self.tme("/log_%d_%m_%Y_-_%H_%M_%S.log")
        # self.pos = 1
        # self.log_var = ""
        # self.stdout = stdout
        # self.stderr = stderr

    def log(self, prior, cmd, msg):
        return
        # from threading import Thread
        # import sys
        # Thread(None, lambda: self._log(prior, cmd, msg, sys.stdout)).start()

    def _log(self, priority, cmd, msg, std):
        return
        # """
        # Logs a message
        # :param priority:
        # :param cmd:
        # :param msg:
        # :return:
        # """
        # priority = str(priority)
        # cmd = str(cmd)
        # msg = str(msg)
        # out = "[" + self.tme("%H:%M:%S") + "] - [" + priority.upper() + "] [" + cmd + "]: " + msg + "\n"
        # if self.log:
        #     print(out[0:-1], file=std)
        # self.log_var += out
        # self.save()

    def debug(self, cmd, message):
        return
        # from threading import Thread
        # import sys
        # Thread(None, lambda: self._log("DEBUG", cmd, message, sys.stdout)).start()

    def info(self, cmd, message):
        return
        # from threading import Thread
        # import sys
        # Thread(None, lambda: self._log("INFO", cmd, message, sys.stdout)).start()

    def warning(self, cmd, message):
        return
        # from threading import Thread
        # import sys
        # Thread(None, lambda: self._log("WARNING", cmd, message, sys.stderr)).start()

    def error(self, cmd, message):
        return
        # from threading import Thread
        # import sys
        # Thread(None, lambda: self._log("ERROR", cmd, message, sys.stderr)).start()

    def fatal(self, cmd, message):
        return
        # from threading import Thread
        # import sys
        # Thread(None, lambda: self._log("FATAL", cmd, message, sys.stderr)).start()
        # exit(1)

    def save(self):
        return
        # """
        # slots the log
        # :return:
        # """
        # fa = open(self.save_file, "w")
        # fa.write(self.log_var)
        # fa.close()


def load_data_int(file_path, if_none=0.0):
    """
    Loading assets in int format
    :param file_path:
    :param if_none:
    :return:
    """
    fo = open(file_path, "r+")
    data = fo.read(100)
    fo.close()
    if data == "":
        return if_none
    try:
        data2 = int(data)
    except ValueError:
        try:
            data2 = float(data)
        except ValueError:
            data2 = if_none
    return data2


def load_data_str(file_path):
    """
    Load assets in string-format
    :param file_path:
    :return:
    """
    fo = open(file_path, "r+")
    data = fo.read(1024)
    fo.close()
    return data


def load_data_bool(file_path, if_none=False):
    """
    Load assets in boolean-format
    :param file_path:
    :param if_none:
    :return:
    """
    try:
        fo = open(file_path, "r+")
        data = fo.read(10)
        fo.close()
        if data == "True":
            data = True
        elif data == "False":
            data = False
        else:
            raise ValueError("Can't convert '" + data + "' to Boolean!")
    except ValueError:
        data = if_none
    return data


def load_data_bytes(file_path):
    """
    Load assets in bytes-format
    :param file_path:
    :return:
    """
    fo = open(file_path, "r+")
    data = fo.read(100).encode()
    fo.close()
    return data


class Extra:
    """
    Extras for the game.
    """

    @staticmethod
    def bool_convert(boolean):
        """
        Boolean convertion tp ON/OFF string.
        :param boolean:
        :return:
        """
        if type(boolean) != bool:
            return "ERROR"
        if boolean:
            return "ON"
        elif not boolean:
            return "OFF"
        else:
            return "ERROR"

    @staticmethod
    def wave_sound(file):
        """
        Plays a .wav sound.
        :param file:
        :return:
        """
        from winsound import PlaySound
        from threading import Thread
        Thread(None, lambda: PlaySound(file, 0))


# noinspection PyTypeChecker
def replace_list(list_name=list, index=int, item=None):
    """
    Replacelist function
    :param list_name:
    :param index:
    :param item:
    """
    if type(list_name) == tuple:
        list_name = list(list_name)
    list_name.pop(index)
    list_name.insert(index, item)


def get_coords(c, id_num):
    """
    Gets the coords by id number of item.
    :param c:
    :param id_num:
    :return:
    """
    try:
        pos = c.coords(id_num)
        if len(pos) == 2:
            x = pos[0]
            y = pos[1]
        else:
            x = (pos[0] + pos[2]) / 2
            y = (pos[1] + pos[3]) / 2
        return x, y
    except AttributeError:
        exit(0)
    except TclError:
        exit(0)


def distance(canvas, log, id1, id2):
    """
    Calculates the distance of the ids.
    :param canvas:
    :param log:
    :param id1:
    :param id2:
    :return:
    """
    from math import sqrt
    try:
        x1, y1 = get_coords(canvas, id1)
        x2, y2 = get_coords(canvas, id2)
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    except IndexError:
        # print(id1, id2)
        # print(get_coords(id1))
        # print(get_coords(id2))
        log.fatal("distance", "IndexError excepted in distance()-module")


def refresh(stats, config, bubble, bub, canvas, backgrounds, texts, modes, panels):
    """
    Refresh Object. Refreshing in a Thread for faster mainloop.
    :return:
    """
    from random import randint
    from threading import Thread
    from qbubbles.bubble import create_bubble
    from qbubbles.info import show_info
    if Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] / config["Game"]["level-score"] > stats["level"]:
        if randint(0, 125) == 0:
            if not bubble["key-active"]:
                Thread(None, lambda: create_bubble(stats, config, bub, canvas, bubble, i=-1)).start()
                config["Bubble"]["max-speed"] += 0.2
                bubble["key-active"] = True
    Thread(None, lambda: refresh_state(stats, bubble, canvas, backgrounds, panels)).start()
    Thread(None, lambda: show_info(canvas, texts, stats)).start()


def refresh_state(stats, bubbles, canvas, backgrounds, panels):
    """
    Refreshing the states. So as normal, in a Thread.
    :rtype: object
    """
    from time import time, sleep
    if stats["slowmotion"]:
        sleep(0.5)
    if stats["scorestate_time"] <= time():
        stats["scorestate"] = 1
        stats["scorestate_time"] = time()
    if stats["secure_time"] <= time():
        stats["secure"] = False
        stats["secure_time"] = time()
    if stats["slowmotion_time"] <= time():
        stats["slowmotion"] = False
        stats["slowmotion_time"] = time()
    if stats["timebreak_time"] <= time():
        stats["timebreak"] = False
        stats["timebreak_time"] = time()
    if stats["confusion_time"] <= time():
        stats["confusion"] = False
        stats["confusion_time"] = time()
    if stats["speedboost_time"] <= time():
        stats["speedboost"] = False
        stats["speedboost_time"] = time()
    if stats["paralyse_time"] <= time():
        stats["paralyse"] = False
        stats["paralyse_time"] = time()
    if stats["shotspeed_time"] <= time():
        stats["shotspeed"] = 0.1
        stats["shotspeed_time"] = time()
    if stats["notouch_time"] <= time():
        stats["notouch"] = False
        stats["notouch_time"] = time()
    if stats["special-level_time"] <= time():
        stats["special-level"] = False
        stats["special-level_time"] = time()
        try:
            canvas.itemconfig(backgrounds["id"], image=backgrounds["normal"])
            canvas.itemconfig(panels["game/top"], fill="darkcyan")
        except AttributeError:
            exit(0)
        except TclError:
            exit(0)
    if Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] > Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["high-score"]:
        Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["high-score"] = Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"]
    Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"] = int(Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["score"])
    Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["high-score"] = int(Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["high-score"])
    if stats["confusion"] and not stats["secure"]:
        shuffling(bubbles)


class LogException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


def pop_bubble(canvas, log, bubble, commands, root, stats, temp, backgrounds, texts, event):
    from qbubbles.bubble import Collision, del_bubble
    from math import sqrt
    for index_bub in range(len(bubble["bub-id"])-1, -1, -1):

        x1, y1 = event.x, event.y
        x2, y2 = get_coords(canvas, bubble["bub-id"][index_bub][0])
        dist = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if dist < (bubble["bub-radius"][index_bub]):
            # Sets score / status etc. and deletes bubble
            Collision().coll_func(index_bub, canvas, commands, root, log, stats, (bubble["bub-radius"][index_bub] +
                                                                                  bubble["bub-speed"][index_bub]),
                                  bubble["bub-action"][index_bub], bubble, backgrounds, texts, True)
            del_bubble(index_bub, bubble, canvas)
            temp["found-bubble"] = True
            return
    temp["found-bubble"] = False
    return


def shuffling(bubble):
    """
    Shuffles the Bubble-actions.
    This is been used by aa confuse-bubble
    """
    from random import shuffle
    shuffle(bubble["bub-action"])


def play_sound(filename):
    return
    # pygame.mixer.music.load(filename)
    # pygame.mixer.music.play()


# pygame.init()
