import os
import re
import sys
import time
from tkinter import Tk, Toplevel
from typing import Optional, Callable

from qbubbles.game import default_launchercfg
from qbubbles.load import Load
from qbubbles.registry import Registry


class FakeWindow(Tk):
    def __init__(self):
        """
        Initialize method of FakeWindow class
        """
        super(FakeWindow, self).__init__()

        # Initialize fake-window
        self.attributes('-alpha', 0.0)
        self.bind("<Map>", self.onRootDeiconify)
        self.bind("<Unmap>", self.onRootIconify)

        # Fake-window attributes
        self.child: Optional[Toplevel] = None

    # toplevel follows root taskbar events (minimize, restore)
    def onRootIconify(self, evt):
        """
        Iconify event for fake-window

        :param evt:
        :return:
        """
        if self.child is None:
            return
        self.child.withdraw()

    def onRootDeiconify(self, evt):
        """
        Deiconify event for fake-window

        :param evt:
        :return:
        """

        if self.child is None:
            return
        self.lower()
        self.iconify()
        self.child.deiconify()

    def ready(self):
        self.lower()
        self.iconify()

    def bind_events(self, toplevel):
        """
        Bind events to the child window
        Events:
         :event Destroy: Used for destoring FakeWindow(...) instance when child is destroyed

        :param toplevel:
        :return:
        """

        self.child = toplevel
        self.child.bind("<Destroy>", lambda event: (self.destroy() if event.widget == self.child else None))


def get_hwnd_dpi(window_handle):
    # To detect high DPI displays and avoid need to set Windows compatibility flags
    import os
    if os.name == "nt":
        from ctypes import windll, pointer, wintypes
        windll.shcore.SetProcessDpiAwareness(1)
        DPI100pc = 96  # DPI 96 is 100% scaling
        DPI_type = 0  # MDT_EFFECTIVE_DPI = 0, MDT_ANGULAR_DPI = 1, MDT_RAW_DPI = 2
        winH = wintypes.HWND(window_handle)
        monitorhandle = windll.user32.MonitorFromWindow(winH, wintypes.DWORD(2))  # MONITOR_DEFAULTTONEAREST = 2
        X = wintypes.UINT()
        Y = wintypes.UINT()
        try:
            windll.shcore.GetDpiForMonitor(monitorhandle, DPI_type, pointer(X), pointer(Y))
            return X.value, Y.value, (X.value + Y.value) / (2 * DPI100pc)
        except Exception:
            return 96, 96, 1  # Assume standard Windows DPI & scaling
    else:
        return None, None, 1  # What to do for other OSs?


def tk_geometry_scale(s, cvtfunc):
    patt = r"(?P<W>\d+)x(?P<H>\d+)\+(?P<X>\d+)\+(?P<Y>\d+)"  # format "WxH+X+Y"
    R = re.compile(patt).search(s)
    G = str(cvtfunc(R.group("W"))) + "x"
    G += str(cvtfunc(R.group("H"))) + "+"
    G += str(cvtfunc(R.group("X"))) + "+"
    G += str(cvtfunc(R.group("Y")))
    return G


def make_tk_dpiaware(root: Tk):
    root.dpiX, root.dpiY, root.dpiScaling = get_hwnd_dpi(root.winfo_id())
    root.tkScale = lambda v: int(float(v) * root.dpiScaling)
    root.tkGeometryScale = lambda s: tk_geometry_scale(s, root.tkScale)


class Main(Toplevel):
    def __init__(self):
        os.chdir(os.path.split(__file__)[0])

        self.fakeRoot = FakeWindow()

        self.pre_run()
        super(Main, self).__init__(self.fakeRoot)
        self.fakeRoot.bind_events(self)

        self.dpiX: float
        self.dpiY: float
        self.dpiScaling: float
        self.tkScale: Callable
        self.tkGeometryScale: Callable

        make_tk_dpiaware(self)

        Registry.register_window("fake", self.fakeRoot)
        Registry.register_window("default", self)
        Registry.gameData["startTime"] = time.time()

        # self.wm_attributes("-topmost", True)
        self.overrideredirect(1)
        # width = self.winfo_screenwidth()
        # height = self.winfo_screenheight()
        width = 1920
        height = 1080
        self.geometry(self.tkGeometryScale(f"{width}x{height}+0+0"))
        self.after(30000, lambda: os.kill(os.getpid(), 0))
        # self.wm_protocol("WM_DELETE_WINDOW", ...)

        if "launcherConfig" not in Registry.gameData.keys():
            game_dir: Optional[str] = None
            for argv in sys.argv[1:]:
                if argv.startswith("gameDir="):
                    game_dir = argv[8:]
            if game_dir is None:
                raise RuntimeError("Argument 'gameDir' is not defined, Q-Bubbles cannot continue")
            Registry.gameData["launcherConfig"] = {"gameDir": game_dir}

        Registry.register_scene("LoadScreen", Load(Registry.get_window("default")))

        Load.scenemanager.change_scene("LoadScreen")

    def pre_run(self):
        if "--debug" in sys.argv:
            Registry.gameData["launcherConfig"] = default_launchercfg
            self.debug = True


# class Main(Tk):
#     def __init__(self):
#         self.pre_run()
#         super(Main, self).__init__()
#         Registry.register_window(self)
#
#         self.geometry("1920x1080")
#         # self.after(30000, lambda: os.kill(os.getpid(), 0))
#
#         # self.wm_protocol("WM_DELETE_WINDOW", ...)
#
#         if "launcherConfig" not in Registry.gameData.keys():
#             game_dir: Optional[str] = None
#             for argv in sys.argv[1:]:
#                 if argv.startswith("gameDir="):
#                     game_dir = argv[8:]
#             if game_dir is None:
#                 raise RuntimeError("Argument 'gameDir' is not defined, Q-Bubbles cannot continue")
#             Registry.gameData["launcherConfig"] = {"gameDir": game_dir}
#
#         Registry.register_scene("LoadScreen", Load(Registry.get_window()))
#
#         Load.scenemanager.change_scene("LoadScreen")
#
#     def pre_run(self):
#         if "--debug" in sys.argv:
#             Registry.gameData["launcherConfig"] = default_launchercfg
#             self.debug = True


if __name__ == '__main__':
    main = Main()
    main.mainloop()
