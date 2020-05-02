from threading import Thread, Event

from pyGoogleSearch import Google as GoogleSearch


class Console(object):
    def __init__(self):
        """
        Minimal Windows console (command prompt)

        """
        import os
        import subprocess
        self._os = os
        self._subps = subprocess

    @staticmethod
    def _parse_command(file, *args):
        """
        Parses file and arguments into a string command.

        :param file:
        :param args:
        :return:
        """

        command = [file]

        for arg in args:
            if " " in arg:
                arg = '"' + arg + '"'
            command.append(arg)

        command_str = " ".join(command)
        return command_str

    def execute(self, file, *args):
        """
        Execute a file with arguments

        :param file:
        :param args:
        :return:
        """

        command = self._parse_command(file, *args)
        self._os.system(command)

    def subprocess(self, file, *args):
        """
        Create a subprocess of a file with arguments

        :param file:
        :param args:
        :return:
        """

        self._subps.run([file, *args])


class Std(object):
    def __init__(self):
        """
        STD I/O Base class
        """

        import sys
        self._sys = sys

    def out(self, string):
        """
        STD Output

        :param string:
        :return:
        """
        self._sys.stdout.write(string)

    def err(self, string):
        """
        STD Error

        :param string:
        :return:
        """
        self._sys.stderr.write(string)

    def in_(self, n):
        """
        STD Input

        :param n:
        :return:
        """

        self._sys.stdin.read(n)


class PythonPath(object):
    def __init__(self):
        """
        Python path class
        """

        import sys
        import os
        self._sys = sys
        self._os = os

    def _fix_path(self, path):
        """
        Fixes path for python path

        :param path:
        :return:
        """

        return self._os.path.abspath(path)

    def add(self, path):
        """
        Adds a path to the python path

        :param path:
        :return:
        """

        self._sys.path.append(self._fix_path(path))

    def remove(self, path):
        """
        Removes a path from the python path

        :param path:
        :return:
        """

        self._sys.path.remove(self._fix_path(path))

    def inpath(self, path):
        """
        Checks if a path is already in the python path

        :param path:
        :return:
        """

        return self._fix_path(path) in self._sys.path


class GoogleImages(object):
    def __init__(self):
        """
        Google images scraper
        """

        from googleimagedownloader import googleimagedownloader as googleimg
        self._googleimg = googleimg

    def download(self, query, n):
        """
        Download images from google

        :param query:
        :param n:
        :return:
        """

        self._googleimg.GoogleImageDownloader(query, n)


class Google(object):
    @staticmethod
    def google_search(query, num=10, start=0, recent=None, pages=1, sleep=False):
        """
        Google searcher

        :param query:
        :param num:
        :param start:
        :param recent:
        :param pages:
        :param sleep:
        :return:
        """
        return GoogleSearch(query, num, start, recent, '', pages, sleep)

    @staticmethod
    def google_images():
        """
        Google images scraper

        :return:
        """

        return GoogleImages()


class StoppableThread(Thread):
    def __init__(self, group=None, target=lambda: None, name="", args=None, kwargs=None, daemon=None):
        """
        Thread class with a stop() method. The thread itself has to check
        regularly for the stopped() condition.

        Code:
        # -- BEGIN -- #
        def funct():
            while not testthread.stopped():
                time.sleep(1)
                print("Hello")

        testthread = StoppableThread()
        testthread.start()
        time.sleep(5)
        testthread.stop()
        # --- END --- #

        :param group:
        :param target:
        :param name:
        :param args:
        :param kwargs:
        :param daemon:
        """
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

        super(StoppableThread, self).__init__(group, target, name, args, kwargs, daemon=daemon)

        self._stopEvent = Event()

    def stop(self):
        self._stopEvent.set()

    def stopped(self):
        self._stopEvent.is_set()


class Notification(object):
    iconNames = ["info", "error", "warn"]

    def __init__(self, title, message, icon):
        import wx.adv
        self._wx_adv = wx.adv
        self.app = wx.App()

        if icon not in self.iconNames:
            raise ValueError(f"Icon is not any of '{self.iconNames}'")
        if icon == "info":
            flags = wx.ICON_INFORMATION
        elif icon == "error":
            flags = wx.ICON_ERROR
        elif icon == "warn":
            flags = wx.ICON_WARNING
        else:
            raise ValueError(f"Icon is not any of '{self.iconNames}'")

        self._notify: wx.adv.NotificationMessage
        self._notify = wx.adv.NotificationMessage(title=title, message=message, flags=flags)

        self._title: str = title
        self._message: str = message

    def show(self):
        self._notify.Show(-1)
        self.app.Destroy()

    def close(self):
        self._notify.Close()

    def set_title(self, title):
        self._notify.SetTitle(title)
        self._title = title

    def get_title(self):
        return self._title

    def set_message(self, message):
        self._notify.SetTitle(message)
        self._message = message

    def get_message(self):
        return self._message

    settitle = set_title
    gettitle = get_title
    setmessage = set_message
    getmessage = get_message
    setmsg = set_message
    getmsg = get_message
    SetTitle = set_title
    GetTitle = get_title
    SetMessage = set_message
    GetMessage = get_message
    SetMsg = set_message
    GetMsg = get_message
    Close = close
    setTitle = set_title
    getTitle = get_title
    setMessage = set_message
    getMessage = get_message
    setMsg = set_message
    getMsg = get_message


class ScreenInfo(object):
    def __init__(self):
        import screeninfo
        self._screeninfo = screeninfo

    def get_monitors(self):
        monitors = self._screeninfo.get_monitors()
        return monitors

    getmonitors = get_monitors
    GetMonitors = get_monitors
    getMonitors = get_monitors


class TTS(object):
    def __init__(self, language, slow=False):
        self._lang = language
        self.slow = slow

    def speak(self, text):
        from gtts import gTTS
        from playsound import playsound
        import os
        from qbubbles.advUtils.advRandom import Random

        filename = f'temp_{Random().randomhex(range(0x10000000000, 0xFFFFFFFFFFF))[2:]}.mp3'
        # print(filename)
        # exit(0)

        tts = gTTS(text, lang=self._lang, slow=self.slow, lang_check=True)
        tts.save(filename)
        playsound(filename)
        os.remove(filename)

    def pspeak(self, text):
        print(text)
        self.speak(text)


class Translate(object):
    def __init__(self, from_, to_):
        self.langFrom = from_
        self.langTo = to_

    def translate(self, text):
        pass


if __name__ == '__main__':
    tts = TTS("en")

    # try:
    #     exec("hgur hfrkejgreg")
    # except Exception as e:
    #     a = f"Failed executing. {e.__class__.__name__}"
    #     print(a)
    #     tts.speak(a)

    tts.speak("Hello, mr. error")
    tts.speak("""Hoi""")
    # tts.speak(" ".join(["Oops we have a problem,"] * 10))
    # tts.speak("")
