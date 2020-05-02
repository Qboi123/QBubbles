import re


def Get_HWND_DPI(window_handle):
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


def TkGeometryScale(s, cvtfunc):
    patt = r"(?P<W>\d+)x(?P<H>\d+)\+(?P<X>\d+)\+(?P<Y>\d+)"  # format "WxH+X+Y"
    R = re.compile(patt).search(s)
    G = str(cvtfunc(R.group("W"))) + "x"
    G += str(cvtfunc(R.group("H"))) + "+"
    G += str(cvtfunc(R.group("X"))) + "+"
    G += str(cvtfunc(R.group("Y")))
    return G


def MakeTkDPIAware(TKGUI):
    TKGUI.DPI_X, TKGUI.DPI_Y, TKGUI.DPI_scaling = Get_HWND_DPI(TKGUI.winfo_id())
    TKGUI.TkScale = lambda v: int(float(v) * TKGUI.DPI_scaling)
    TKGUI.tk_geometry_scale = lambda s: TkGeometryScale(s, TKGUI.TkScale)


if __name__ == '__main__':
    def test1():
        # Example use:
        import tkinter

        GUI = tkinter.Tk()
        MakeTkDPIAware(GUI)  # Sets the windows flag + gets adds .DPI_scaling property
        GUI.geometry(GUI.TkGeometryScale("600x200+200+100"))
        gray = "#cccccc"
        DemoFrame = tkinter.Frame(GUI, width=GUI.TkScale(580), height=GUI.TkScale(180), background=gray)
        DemoFrame.place(x=GUI.TkScale(10), y=GUI.TkScale(10))
        DemoFrame.pack_propagate(False)
        LabelText = "Scale = " + str(GUI.DPI_scaling)
        DemoLabel = tkinter.Label(DemoFrame, text=LabelText, width=10, height=1, font=("Arial", GUI.TkScale(10)))
        DemoLabel.pack(pady=GUI.TkScale(70))
        GUI.mainloop()

    def test2():
        from tkinter import Tk, Button, Label
        root = Tk()
        MakeTkDPIAware(root)
        root.geometry(root.TkGeometryScale("200x24+100+100"))
        button = Button(root, text="HoiHallo", font=("Helvetica", int(10*root.DPI_scaling)))
        button.pack()
        root.mainloop()

    test1()
    test2()
