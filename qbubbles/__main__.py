import os
import re
import sys
import time
from tkinter import Tk, Toplevel, Frame, Label, font
from typing import Optional, Callable, Union

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
        frame = Frame(self, bg="#373737")
        frame.pack(fill="both", expand=True)
        self.wm_geometry("180x40+0+0")
        font1 = font.nametofont("TkFixedFont")
        family = font1.cget("family")
        # print()
        Label(frame, bg="#373737", fg="#a7a7a7", text="FakeWindow", font=(family, 20)).pack()
        self.bind("<Map>", self.onRootDeiconify)
        self.bind("<Unmap>", self.onRootIconify)

        # self.bind("<FocusOut>", self.onRootIconify)
        self.bind("<FocusIn>", self.onRootDeiconify)

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
        self.child.wm_attributes("-alpha", 0)
        self.child.deiconify()
        self.child.wm_attributes("-alpha", 1)

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
        self.child.bind("<Destroy>", lambda event: (self.destroy() if (event.widget == self.child) or (event.widget == self) else None))

        # self.child.bind("<FocusOut>", lambda event: self.onRootIconify(event) if event.widget == self.child and self.child.focus_get() else None)
        self.child.bind("<FocusIn>", lambda event: self.onRootDeiconify(event) if event.widget == self.child and not self.child.focus_get() else None)


def get_hwnd_dpi(window_handle):
    """
    To detect high DPI displays and avoid need to set Windows compatibility flags

    :param window_handle:
    :return:
    """

    import os
    if os.name == "nt":
        from ctypes import windll, pointer, wintypes
        windll.shcore.SetProcessDpiAwareness(1)
        dpi100pc = 96  # DPI 96 is 100% scaling
        dpi_type = 0  # MDT_EFFECTIVE_DPI = 0, MDT_ANGULAR_DPI = 1, MDT_RAW_DPI = 2
        win_h = wintypes.HWND(window_handle)
        monitorhandle = windll.user32.MonitorFromWindow(win_h, wintypes.DWORD(2))  # MONITOR_DEFAULTTONEAREST = 2
        x = wintypes.UINT()
        y = wintypes.UINT()
        # noinspection PyBroadException
        try:
            windll.shcore.GetDpiForMonitor(monitorhandle, dpi_type, pointer(x), pointer(y))
            return x.value, y.value, (x.value + y.value) / (2 * dpi100pc)
        except Exception:
            return 96, 96, 1  # Assume standard Windows DPI & scaling
    else:
        return None, None, 1  # What to do for other OSs?


def tk_geometry_scale(s, cvtfunc):
    """
    Scaled geometry for Tk-window

    :param s:
    :param cvtfunc:
    :return:
    """

    patt = r"(?P<W>\d+)x(?P<H>\d+)\+(?P<X>\d+)\+(?P<Y>\d+)"  # format "WxH+X+Y"
    r = re.compile(patt).search(s)
    g = str(cvtfunc(r.group("W"))) + "x"
    g += str(cvtfunc(r.group("H"))) + "+"
    g += str(cvtfunc(r.group("X"))) + "+"
    g += str(cvtfunc(r.group("Y")))
    return g


def make_tk_dpiaware(root: Union[Tk, Toplevel]):
    """
    Used for configure a Tk-window to make it DPI-aware

    :param root:
    :return:
    """
    root.dpiX, root.dpiY, root.dpiScaling = get_hwnd_dpi(root.winfo_id())
    root.tkScale = lambda v: int(float(v) * root.dpiScaling)
    root.tkGeometryScale = lambda s: tk_geometry_scale(s, root.tkScale)


class Main(Toplevel):
    def __init__(self):
        """
        Main-class constructor for Q-Bubbles
        """

        if "launcherConfig" not in Registry.gameData.keys():
            game_dir: Optional[str] = None
            for argv in sys.argv[1:]:
                if argv.startswith("gameDir="):
                    game_dir = argv[8:]
            if game_dir is None:
                raise RuntimeError("Argument 'gameDir' is not defined, Q-Bubbles cannot continue")
            if not game_dir.endswith("/"):
                game_dir += "/"
            Registry.gameData["launcherConfig"] = {"gameDir": game_dir}

        try:
            os.chdir(os.path.split(__file__)[0])  # ...\qbubbles
        except FileNotFoundError:
            os.chdir(os.path.join(Registry.gameData["launcherConfig"]["gameDir"], "data/1.0-alpha1"))

        self.fakeRoot = FakeWindow()

        self.debug = False
        self.pre_run()
        super(Main, self).__init__(self.fakeRoot)
        self.fakeRoot.bind_events(self)
        # self.protocol("WM_DELETE_WINDOW", self.fakeRoot.destroy)

        self.dpiX: float
        self.dpiY: float
        self.dpiScaling: float
        self.tkScale: Callable
        self.tkGeometryScale: Callable

        make_tk_dpiaware(self)

        Registry.register_window("fake", self.fakeRoot)
        Registry.register_window("default", self)
        Registry.gameData["startTime"] = time.time()

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.wm_attributes("-alpha", 0)
        self.geometry(self.tkGeometryScale(f"{width}x{height}+0+0"))
        self.wm_protocol("WM_DELETE_WINDOW", lambda: os.kill(os.getpid(), 0))
        self.update()
        self.deiconify()
        self.overrideredirect(1)
        self.wm_attributes("-alpha", 1)

        # os.chdir(game_dir)

        Registry.register_scene("LoadScreen", Load(Registry.get_window("default")))

        Load.scenemanager.change_scene("LoadScreen")

    def pre_run(self):
        """
        Pre-run method for some features
        Features:
         - Debug mode uses the --debug commandline argument

        :return:
        """

        if "--debug" in sys.argv:
            Registry.gameData["launcherConfig"] = default_launchercfg
            Registry.gameData["launcherConfig"]["debug"] = True
            self.debug = True


if __name__ == '__main__':
    main = Main()
    main.mainloop()
