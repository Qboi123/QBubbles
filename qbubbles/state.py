from threading import Thread
from random import randint
from time import time
from qbubbles.extras import play_sound


class State:
    """
    Status for the game
    """

    @staticmethod
    def __set_state__(canvas, log, stats, act, backgrounds):
        """
        Sets the status by Bubble-Action
        :param act:
        :return:
        """
        # log.info("State", "Give the player, status: '" + act + "'.")
        if act == "DoubleState":
            stats["scorestate"] = 2
            stats["scorestate_time"] = time() + randint(5, 20)
        if act == "Protect":
            stats["secure"] = True
            stats["secure_time"] = time() + randint(10, 15)
        if act == "SlowMotion":
            stats["slowmotion"] = True
            stats["slowmotion_time"] = time() + randint(15, 23)
        if act == "Confusion":
            stats["confus"] = True
            stats["confus_time"] = time() + randint(5, 10)
        if act == "TimeBreak":
            stats["timebreak"] = True
            stats["timebreak_time"] = time() + randint(10, 20)
        if act == "SpeedBoost":
            stats["speedboost"] = True
            stats["speedboost_time"] = time() + randint(10, 20)
        if act == "Paralyse":
            stats["paralyse"] = True
            stats["paralyse_time"] = time() + randint(5, 7)
        if act == "HyperMode":
            stats["confus"] = False
            stats["confus_time"] = time()
            stats["paralyse"] = False
            stats["paralyse_time"] = time()
            stats["timebreak"] = True
            stats["scorestate"] = 10
            stats["timebreak_time"] = time() + randint(24, 32)
            stats["scorestate_time"] = time() + randint(24, 32)
        if act == "ShotSpdStat":
            stats["shotspeed"] = 0.2
            stats["shotspeed_time"] = time() + randint(13, 15)
        if act == "NoTouch":
            stats["notouch"] = True
            stats["notouch_time"] = time() + randint(10, 15)
        if act == "Ultimate":
            stats["scorestate"] = 10
            stats["scorestate_time"] = time() + 15
            stats["slowmotion"] = True
            stats["slowmotion_time"] = time() + randint(7, 10)
        if act == "SpecialLevel":
            canvas.itemconfig(backgrounds["id"], image=backgrounds["special"])
            stats["special-level"] = True
            stats["special-level_time"] = time() + 20
            log.info("State", "Special Level State is ON!!!")
            play_sound("versions/"+self.launcher_cfg["versionDir"]+"/assets/sounds/specialmode.mp3")

    @staticmethod
    def set_state(canvas, log, stats, action, backgrounds):
        Thread(None, lambda: State.__set_state__(canvas, log, stats, action, backgrounds)).start()

    @staticmethod
    def del_state(canvas, stats, action, backgrounds):
        """
        Removes a status
        *This is for future game
        :param canvas:
        :param stats:
        :param backgrounds:
        :param action:
        :return:
        """
        # Set the status of the player
        if action == "DoubleState":
            stats["scorestate"] = 1
            stats["scorestate_time"] = time()
        if action == "Protect":
            stats["secure"] = False
            stats["secure_time"] = time()
        if action == "SlowMotion":
            stats["slowmotion"] = False
            stats["slowmotion_time"] = time()
        if action == "Confusion":
            stats["confusion"] = False
            stats["confusion_time"] = time()
        if action == "TimeBreak":
            stats["timebreak"] = False
            stats["timebreak_time"] = time()
        if action == "SpeedBoost":
            stats["speedboost"] = False
            stats["speedboost_time"] = time()
        if action == "Paralyse":
            stats["paralyse"] = False
            stats["paralyse_time"] = time()
        if action == "HyperMode":
            stats["timebreak"] = False
            stats["timebreak_time"] = time()
            stats["scorestate"] = 1
            stats["scorestate_time"] = time()
        if action == "ShotSpdStat":
            stats["shotspeed"] = 25
            stats["shotspeed_time"] = time()
        if action == "SpecialLevel":
            canvas.itemconfig(backgrounds["id"], image=backgrounds["normal"])
            stats["special-level"] = False
            stats["special-level_time"] = time()
