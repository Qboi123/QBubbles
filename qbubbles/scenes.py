import os
import random
import string
import sys
import tkinter as _tk
import tkinter.font as _font
import tkinter.ttk as _ttk
import typing as _t

import yaml as _yml

import qbubbles.config as _conf
import qbubbles.gameIO as _gameIO
import qbubbles.gui as _gui
import qbubbles.maps as _maps
import qbubbles.registry as _reg
import qbubbles.scenemanager as _scenemgr
import qbubbles.special as _special
import qbubbles.utils as _utils

TREEVIEW_BG = "#7f7f7f"
TREEVIEW_FG = "#9f9f9f"
TREEVIEW_SEL_BG = "#00a7a7"
TREEVIEW_SEL_FG = "white"

BUTTON_BG = "#7f7f7f"
BUTTON_BG_FOC = "#00a7a7"
BUTTON_BG_DIS = "#5c5c5c"
BUTTON_FG = "#a7a7a7"
BUTTON_FG_FOC = "white"
BUTTON_FG_DIS = "#7f7f7f"
BUTTON_BD_COL = "#00a7a7"
BUTTON_RELIEF = "flat"
BUTTON_BD_WID = 0

ENTRY_BG = "#5c5c5c"
ENTRY_BG_FOC = "#00a7a7"
ENTRY_BG_DIS = "#7f7f7f"
ENTRY_FG = "#7f7f7f"
ENTRY_FG_FOC = "white"
ENTRY_FG_DIS = "#a7a7a7"
ENTRY_BD_COL = "#00a7a7"
ENTRY_RELIEF = "flat"
ENTRY_BD_WID = 0
ENTRY_SEL_BG = "#00c9c9"
ENTRY_SEL_BG_FOC = "#00dada"
ENTRY_SEL_BG_DIS = "#a7a7a7"
ENTRY_SEL_FG = "#7f7f7f"
ENTRY_SEL_FG_FOC = "white"
ENTRY_SEL_FG_DIS = "#ffffff"


# noinspection PyAttributeOutsideInit
class SavesMenu(_scenemgr.Scene):
    def __init__(self, reload=False):
        root = _reg.Registry.get_window("default")

        if not reload:
            super(SavesMenu, self).__init__(root)

        self.btnFont = _reg.Registry.gameData["fonts"]["slotsButtonFont"]
        self.lang = _reg.Registry.gameData["language"]

        controlsFont = _utils.Font("Helvetica", 10)
        cFontT = controlsFont.get_tuple()

        style = _ttk.Style()
        style.theme_settings("default", {
            "TEntry": {
                "configure": {"font": cFontT, "relief": "flat", "selectborderwidth": 0, "padding": 10},
                "map": {
                    "relief": [("active", ENTRY_RELIEF),
                               ("focus", ENTRY_RELIEF),
                               ("!disabled", ENTRY_RELIEF)],
                    "bordercolor": [("active", ENTRY_BD_COL),
                                    ("focus", ENTRY_BD_COL),
                                    ("!disabled", ENTRY_BD_COL)],
                    "background": [("active", ENTRY_BG),
                                   ("focus", ENTRY_BG_FOC),
                                   ("!disabled", ENTRY_BG_DIS)],
                    "fieldbackground": [("active", ENTRY_BG),
                                        ("focus", ENTRY_BG_FOC),
                                        ("!disabled", ENTRY_BG_DIS)],
                    "foreground": [("active", ENTRY_FG),
                                   ("focus", ENTRY_FG_FOC),
                                   ("!disabled", ENTRY_FG_DIS)],
                    "selectbackground": [("active", ENTRY_SEL_BG),
                                         ("focus", ENTRY_SEL_BG_FOC),
                                         ("!disabled", ENTRY_SEL_BG_DIS)],
                    "selectforeground": [("active", ENTRY_SEL_FG),
                                         ("focus", ENTRY_SEL_FG_FOC),
                                         ("!disabled", ENTRY_SEL_FG_DIS)]
                }
            },
            "TLabel": {
                "configure": {"background": "#5c5c5c",
                              "foreground": "#7f7f7f",
                              "font": cFontT}
            },
            "TButton": {
                "configure": {"font": cFontT, "relief": BUTTON_RELIEF, "bd": 1},
                "map": {
                    "background": [("active", BUTTON_BG_FOC),
                                   ("focus", BUTTON_BG),
                                   ("!disabled", BUTTON_BG)],
                    "bordercolor": [("active", BUTTON_BD_COL),
                                    ("focus", BUTTON_BG_FOC),
                                    ("!disabled", BUTTON_BD_COL)],
                    "foreground": [("active", BUTTON_FG_FOC),
                                   ("focus", BUTTON_FG_FOC),
                                   ("!disabled", BUTTON_FG)],
                }
            },
            "Treeview": {
                "configure": {"padding": 0, "font": cFontT, "relief": "flat", "border": 0,
                              "rowheight": 24},
                "map": {
                    "background": [("active", TREEVIEW_BG),
                                   ("focus", TREEVIEW_SEL_BG),
                                   ("!disabled", TREEVIEW_BG),
                                   ("selected", TREEVIEW_BG)],
                    "fieldbackground": [("active", TREEVIEW_BG),
                                        ("focus", TREEVIEW_BG),
                                        ("!disabled", TREEVIEW_BG)],
                    "foreground": [("active", TREEVIEW_FG),
                                   ("focus", TREEVIEW_SEL_FG),
                                   ("!disabled", TREEVIEW_FG),
                                   ("selected", TREEVIEW_FG)],
                    "relief": [("focus", "flat"),
                               ("active", "flat"),
                               ("!disabled", "flat")]
                }
            },
            "Treeview.Item": {
                "configure": {"padding": 0},
                "map": {
                    "background": [("active", TREEVIEW_SEL_BG),
                                   ("!disabled", TREEVIEW_SEL_BG),
                                   ("!selected", TREEVIEW_SEL_BG)],
                    "fieldbackground": [("!disabled", TREEVIEW_SEL_BG),
                                        ("active", TREEVIEW_SEL_BG),
                                        ("!selected", TREEVIEW_SEL_BG)],
                    "foreground": [("active", TREEVIEW_SEL_BG),
                                   ("focus", TREEVIEW_SEL_FG),
                                   ("!disabled", TREEVIEW_SEL_FG),
                                   ("selected", TREEVIEW_SEL_BG)],
                    "relief": [("focus", "flat"),
                               ("active", "flat"),
                               ("!disabled", "flat")]
                }
            },
            "Treeview.Cell": {
                "configure": {"padding": 0},
                "map": {
                    "background": [("active", TREEVIEW_SEL_BG),
                                   ("!disabled", TREEVIEW_SEL_BG),
                                   ("!selected", TREEVIEW_SEL_BG)],
                    "fieldbackground": [("!disabled", TREEVIEW_SEL_BG),
                                        ("active", TREEVIEW_SEL_BG),
                                        ("!selected", TREEVIEW_SEL_BG)],
                    "foreground": [("focus", TREEVIEW_SEL_FG),
                                   ("!disabled", TREEVIEW_SEL_FG),
                                   ("!selected", TREEVIEW_SEL_BG)],
                    "relief": [("focus", "flat"),
                               ("active", "flat"),
                               ("!disabled", "flat")]
                }
            }
        })
        # print(style.map("Treeview"))
        # print(style.configure("Treeview"))
        # print(style.co("Treeview"))

        # style.configure("BW.TTreeview", foreground=", background="white")
        #
        # foreground = "black", background = "white"
        # sty
        style.theme_use("default")
        style.configure('TEntry', relief='flat', bd=0, borderwidth=0)

        # print(style.layout("TEntry"))

        #   lets try to change this structure
        style.layout('TEntry', [
            ('Entry.highlight', {
                "border": 0,
                'sticky': 'nswe',
                'children': [('Entry.border', {
                    'border': 0,
                    'sticky': 'nswe',
                    'children':
                        [('Entry.padding', {
                            'sticky': 'nswe',
                            'children':
                                [('Entry.textarea', {
                                    'sticky': 'nswe',
                                    "border": 0})]
                        })]
                }), ('Entry.bd', {
                    'sticky': 'nswe',
                    'children': [(
                        'Entry.padding', {
                            'sticky': 'nswe',
                            'children': [(
                                'Entry.textarea', {
                                    'sticky': 'nswe'})]
                        })],
                    'border': 0})
                             ]
            })])
        style.configure('TEntry', relief='flat', bd=0)

        # style.map("TTreeview", foreground="")
        # print(style)
        self.buttons = []
        self.names = {}

        self.oFrame = _tk.Frame(self.frame, bg="#5c5c5c")

        # for shell in SHELLS: self.buttons.append(Button(self.oFrame, text=shell["name"], bg="#4f4f4f", fg="#7f7f7f",
        # command=lambda path=shell["path"]: self.open_shell(path), width=10, relief="flat", border=0,
        # font=("Helvetica", 16))) self.buttons[-1].pack(fill="both", expand=True, pady=2, padx=4)
        #
        # self.oFrame.pack(fill="both", expand=True)

        # Frame for adding slots.
        self.frame2 = _tk.Frame(self.oFrame, bg="#5c5c5c", height=94, width=720)

        self.controlsFrame = _tk.Frame(self.frame2, height=92, width=720)
        self.controlsFrameA = _tk.Frame(self.controlsFrame, bg="#5c5c5c", width=720, height=36)

        # Add-button and -entry (Input)
        self.openBtn = _ttk.Button(self.controlsFrameA, text="Open",  # relief="flat", bg="#7f7f7f", fg="white",
                                   command=self.open_save, width=24)  # , font=["Helvetica", 10], bd=5)
        self.openBtn.pack(side="left", padx=1, pady=1, fill="both", expand=True)
        self.renameBtn = _ttk.Button(self.controlsFrameA, text="Add",  # relief="flat", bg="#7f7f7f", fg="white",
                                     command=self.add_save, width=24)  # , font=["Helvetica", 10], bd=5)
        self.renameBtn.pack(side="left", padx=1, pady=1, fill="both", expand=True)
        self.controlsFrameA.pack()
        self.controlsFrameA.pack_propagate(0)
        self.controlsFrameA.update()

        self.controlsFrameB = _tk.Frame(self.controlsFrame, bg="#5c5c5c", width=720, height=36)

        # Add-button and -entry (Input)
        self.removeBtn = _ttk.Button(self.controlsFrameB, text="Remove",  # relief="flat", bg="#7f7f7f", fg="white",
                                     command=self.remove_save,
                                     width=12)  # , font=["Helvetica", 10], bd=5)
        self.removeBtn.pack(side="left", padx=1, pady=1, fill="both", expand=True)
        # Add-button and -entry (Input)
        self.removeBtn = _ttk.Button(self.controlsFrameB, text="Remove",  # relief="flat", bg="#7f7f7f", fg="white",
                                     command=self.rename_save,
                                     width=12)  # , font=["Helvetica", 10], bd=5)
        self.removeBtn.pack(side="left", padx=1, pady=1, fill="both", expand=True)
        self.resetBtn = _ttk.Button(self.controlsFrameB, text="Reset",
                                    command=self.reset_save,
                                    width=12)
        self.resetBtn.pack(side="left", padx=1, pady=1, fill="both", expand=True)

        self.backBtn = _ttk.Button(self.controlsFrameB, text="Back",
                                   command=self.back_title, width=12)
        self.backBtn.pack(side="left", padx=1, pady=1, fill="both", expand=True)

        # self.rename = Button(self.controlsFrameA, text="Rename Shell", relief="flat", bg="#7f7f7f", fg="white",
        #                   command=self.add_shell, font=["Helvetica", 10], bd=5)
        # self.rename.pack(side="left", padx=2, pady=5, fill="both", expand=True)
        self.controlsFrameB.pack()
        self.controlsFrameB.pack_propagate(0)
        self.controlsFrameB.update()

        root.update()
        root.update_idletasks()

        self.controlsFrame.pack(padx=1, pady=1)
        self.controlsFrame.pack_propagate(0)

        # print(self.controlsFrameA.winfo_reqwidth())
        # self.add_input = Entry(self.frame2, bd=5, fg="#3c3c3c", bg="#7f7f7f", relief="flat", font=("helvetica", 10))
        # self.add_input.pack(side=LEFT, fill="x", expand=True, padx=2, pady=5)
        # self.add_input.bind("<Return>", self.add_shell)

        # Update root GUI.
        self.update()

        # Packing the config frame for adding a slot.
        self.frame2.pack(side="bottom", fill="x", padx=2)

    def show_scene(self, *args, **kwargs):
        super(SavesMenu, self).show_scene(*args, **kwargs)
        # # print(0)
        _gameIO.Logging.info("SavesMenu", "Showing SavesMenu()-scene")

        self.initialize_scene()

    def initialize_scene(self):
        root = _reg.Registry.get_window("default")

        # # print(1)

        # Main frame.
        self.main_f = _tk.Frame(self.oFrame, background="#3c3c3c", height=_reg.Registry.gameData["WindowHeight"] - 100)
        self.main_f.pack(fill="both", expand=True)

        # Slots frame.
        self.s_frame = _tk.Frame(self.main_f, height=self.main_f.winfo_height() - 100, width=root.tkScale(700))
        self.s_frame.pack(fill="y", expand=True)

        # # print(2)

        # Scrollwindow for the slots frame
        self.sw = _special.ScrolledWindow(self.s_frame, 700, self.oFrame.winfo_height() + 0, expand=True, fill="both")

        self.sw.vbar.configure(bg="#3c3c3c", fg="#7f7f7f")

        # Configurate the canvas from the scrollwindow
        self.canv = self.sw.canv
        self.canv.config(bg="#2e2e2e")

        # self.oFrame.
        self.frame_sw = self.sw.scrollwindow
        self.frames = []

        # print(3)

        # Defining the list of widgets
        self._id = {}
        self.index = {}
        self.canvass = []
        self.buttons = []

        # print(4)

        self.oldSelected: _t.Optional[_tk.Canvas] = None
        self.selectedCanvas: _t.Optional[_tk.Canvas] = None
        self._hoverCanvasOld: _t.Optional[_tk.Canvas] = None
        self._hoverCanvas: _t.Optional[_tk.Canvas] = None

        # print(5)

        titlefont = _utils.Font("Helvetica", 25, "bold")
        infofont = _utils.Font("Helvetica", 16)

        # print(6)

        # Get slots
        if not os.path.exists(f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/"):
            os.makedirs(f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/")
        names = os.listdir(f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/")

        # Information variables for each slot.
        infos = {"dates": [], "score": [], "level": []}

        # print(7)

        import time

        # Prepare info variables
        for i in names.copy():
            if not os.path.exists(f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/" + i + "/bubble.nzt"):
                names.remove(i)
                continue
            mtime = os.path.getmtime(f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/" + i + "/bubble.nzt")
            a = time.localtime(mtime)

            b = list(a)

            if a[4] < 10:
                b[4] = "0" + str(a[4])
            else:
                b[4] = str(a[4])
            if a[5] < 10:
                b[5] = "0" + str(a[5])
            else:
                b[5] = str(a[5])

            # tme_var = "%i/%i/%i %i:%s:%s" % (a[2], a[1], a[0], a[3], b[4], b[5])
            tme_var = f"{a[2]}/{a[1]}/{a[0]} {a[3]}:{a[4]}:{a[5]}"
            infos["dates"].append(tme_var)

            a = _conf.Reader(
                f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/" + i + "/game.nzt").get_decoded()

            try:
                infos["score"].append(a["Player"]["score"])
                infos["level"].append(a["Player"]["level"])
            except KeyError:
                try:
                    infos["score"].append(a["Game"]["Player"]["score"])
                    infos["level"].append(a["Game"]["Player"]["level"])
                except KeyError:
                    infos["score"].append("ERROR")
                    infos["level"].append("ERROR")
        # print(infos)

        # print(8)

        self.item_info = names

        # Define the index variable.
        i = 0

        # print(9)

        # Startloop
        for name in names:
            # print(i)
            self.frames.append(_tk.Frame(self.frame_sw, height=200, width=700))
            self.canvass.append(
                _tk.Canvas(self.frames[-1], height=200, width=700, bg="#7f7f7f", highlightthickness=0))
            self.canvass[-1].pack()
            self._id[self.canvass[-1]] = {}
            self._id[self.canvass[-1]]["Title"] = self.canvass[-1].create_text(10, 10, text=name,
                                                                               fill="#a7a7a7", anchor="nw",
                                                                               font=titlefont.get_tuple())
            self.canvass[-1].create_rectangle(0, 0, 699, 201, outline="#3c3c3c")
            subids = [self.canvass[-1].create_text(10, 50, text=infos["dates"][i], fill="#afafaf", anchor="nw",
                                                   font=infofont.get_tuple()),
                      self.canvass[-1].create_text(240, 50, text="Level: " + str(infos["level"][i]), fill="#afafaf",
                                                   anchor="nw", font=infofont.get_tuple()),
                      self.canvass[-1].create_text(370, 50, text="Score: " + str(infos["score"][i]), fill="#afafaf",
                                                   anchor="nw", font=infofont.get_tuple())]
            self._id[self.canvass[-1]]["Infos"] = subids
            self.canvass[-1].bind("<ButtonRelease-1>",
                                  lambda event, c=self.canvass[-1]: self._on_canv_lclick(c))
            self.canvass[-1].bind("<Double-Button-1>", lambda event, n_=name: self.open_direct(n_))
            self.canvass[-1].bind("<Motion>", lambda event, c=self.canvass[-1]: self._on_canv_motion(c))
            self.canvass[-1].bind("<Leave>", lambda event, c=self.canvass[-1]: self._on_canv_leave(c))
            self.names[self.canvass[-1]] = name
            self.index[self.canvass[-1]] = i
            self.frames[-1].grid(row=i)

            i += 1

        # print(10)

        self.oFrame.pack(fill="both", expand=True)

    def hide_scene(self):
        self.main_f.destroy()
        self.oFrame.pack_forget()

        super(SavesMenu, self).hide_scene()

    def _on_canv_leave(self, hover_canvas):
        if self._hoverCanvasOld is not None:
            if self.selectedCanvas != self._hoverCanvasOld:
                self._hoverCanvasOld.config(bg="#7f7f7f")
                self._hoverCanvasOld.itemconfig(self._id[self._hoverCanvasOld]["Title"], fill="#a7a7a7")
                for subid in self._id[self._hoverCanvasOld]["Infos"]:
                    self._hoverCanvasOld.itemconfig(subid, fill="#a7a7a7")
            else:
                self._hoverCanvasOld.config(bg="darkcyan")
                self._hoverCanvasOld.itemconfig(self._id[hover_canvas]["Title"], fill="#00bfbf")
                for subid in self._id[self._hoverCanvasOld]["Infos"]:
                    self._hoverCanvasOld.itemconfig(subid, fill="#00a7a7")
        self._hoverCanvasOld = None

    def _on_canv_motion(self, hover_canvas):
        if self._hoverCanvasOld == hover_canvas:
            return
        if self._hoverCanvasOld is not None:
            if self.selectedCanvas != self._hoverCanvasOld:
                self._hoverCanvasOld.config(bg="#7f7f7f")
                self._hoverCanvasOld.itemconfig(self._id[self._hoverCanvasOld]["Title"], fill="#a7a7a7")
                for subid in self._id[self._hoverCanvasOld]["Infos"]:
                    self._hoverCanvasOld.itemconfig(subid, fill="#939393")
            else:
                self._hoverCanvasOld.config(bg="darkcyan")
                self._hoverCanvasOld.itemconfig(self._id[hover_canvas]["Title"], fill="#007f7f")
                for subid in self._id[self._hoverCanvasOld]["Infos"]:
                    self._hoverCanvasOld.itemconfig(subid, fill="#00a7a7")
        # print(self.selectedCanvas, self._hoverCanvasOld)
        # print(self.selectedCanvas == self._hoverCanvasOld)
        # print(self.selectedCanvas == hover_canvas)
        self._hoverCanvasOld = hover_canvas

        if hover_canvas != self.selectedCanvas:
            hover_canvas.config(bg="#a7a7a7")
            hover_canvas.itemconfig(self._id[hover_canvas]["Title"], fill="#ffffff")
            for subid in self._id[hover_canvas]["Infos"]:
                hover_canvas.itemconfig(subid, fill="#dadada")
        else:
            hover_canvas.config(bg="#00a7a7")
            hover_canvas.itemconfig(self._id[hover_canvas]["Title"], fill="#7fffff")
            for subid in self._id[hover_canvas]["Infos"]:
                hover_canvas.itemconfig(subid, fill="#00dada")
        self._hoverCanvas = hover_canvas

    def _on_canv_lclick(self, c: _tk.Canvas):
        if self.oldSelected is not None:
            self.oldSelected.config(bg="#7f7f7f")
            self.oldSelected.itemconfig(self._id[self.oldSelected]["Title"], fill="#a7a7a7")
            for subid in self._id[self.oldSelected]["Infos"]:
                self.oldSelected.itemconfig(subid, fill="#939393")
        self.oldSelected = c

        c.config(bg="#00a7a7")
        c.itemconfig(self._id[c]["Title"], fill="#7fffff")
        for subid in self._id[c]["Infos"]:
            c.itemconfig(subid, fill="#00dada")

        self.selectedCanvas = c

    def reset_save(self):
        if self.selectedCanvas is None:
            return
        else:
            src = self.names[self.selectedCanvas]

        root = _reg.Registry.get_window("default")

        self.oFrame.destroy()
        self.oFrame = _tk.Frame(self.frame, bg="#5c5c5c")
        self.titleCanvas = _tk.Canvas(self.oFrame, bg="#5c5c5c", highlightthickness=0, width=480, height=48)
        self.titleCanvas.create_text(0, 0, text=f"Are you sure you want to reset the save'{src}'?", fill="cyan",
                                     anchor="nw", font=_utils.Font("Helvetica", 24).get_tuple())
        self.titleCanvas.place(x=int(_reg.Registry.gameData["WindowWidth"] / 2) - 240, y=320 - 48, anchor="nw")
        self.optionsFrame = _tk.Frame(self.oFrame, bg="#5c5c5c", width=480)
        self.buttonFrame = _tk.Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        self.noBtn = _ttk.Button(self.buttonFrame, command=lambda: self.close_options_frame(), text="No")
        self.yesBtn = _ttk.Button(self.buttonFrame, command=lambda: self.reset_action(src), text="Yes")
        self.noBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)
        self.yesBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)
        self.buttonFrame.pack(fill='x', side="bottom", expand=True)

        root.update()
        root.update_idletasks()
        self.optionsFrame.place(x=int(_reg.Registry.gameData["WindowWidth"] / 2) - 240, y=320, anchor="nw", width=480)

        self.textInput = _ttk.Entry()
        self.oFrame.pack(fill="both", expand=True)

    def remove_save(self):
        if self.selectedCanvas is None:
            return
        else:
            src = self.names[self.selectedCanvas]

        root = _reg.Registry.get_window("default")

        self.oFrame.destroy()
        self.oFrame = _tk.Frame(self.frame, bg="#5c5c5c")
        self.titleCanvas = _tk.Canvas(self.oFrame, bg="#5c5c5c", highlightthickness=0, width=480, height=48)
        self.titleCanvas.create_text(0, 0, text=f"Are you sure you want to remove the save '{src}'?", fill="cyan",
                                     anchor="nw", font=_utils.Font("Helvetica", 24).get_tuple())
        self.titleCanvas.place(x=int(_reg.Registry.gameData["WindowWidth"] / 2) - 240, y=320 - 48, anchor="nw")
        self.optionsFrame = _tk.Frame(self.oFrame, bg="#5c5c5c", width=480)
        self.buttonFrame = _tk.Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        self.noBtn = _ttk.Button(self.buttonFrame, command=lambda: self.close_options_frame(),
                                 # bg="#7f7f7f", fg="#a7a7a7",
                                 text="No")  # , relief="flat", border=0, bd=5)
        self.yesBtn = _ttk.Button(self.buttonFrame, command=lambda: self.remove_action(src),
                                  # bg="#7f7f7f", fg="#a7a7a7",
                                  text="Yes")  # , relief="flat", border=0, bd=5)
        self.noBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)  # , height=20)
        self.yesBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)  # , height=20)
        self.buttonFrame.pack(fill='x', side="bottom", expand=True)

        root.update()
        root.update_idletasks()
        # print("Width:", self.buttonFrame.winfo_width())
        self.optionsFrame.place(x=int(_reg.Registry.gameData["WindowWidth"] / 2) - 240, y=320, anchor="nw", width=480)

        self.textInput = _ttk.Entry()
        self.oFrame.pack(fill="both", expand=True)

    def close_options_frame(self):
        self.oFrame.destroy()
        self.__init__(reload=True)
        self.initialize_scene()

    def add_save(self):
        """
        Add-save menu.

        :return:
        """

        root = _reg.Registry.get_window("default")

        def update(event):
            if event.char in string.digits:
                pass
            elif event.keysym.lower() == "backspace":
                pass
            else:
                return "break"

        self.oFrame.destroy()
        self.oFrame = _tk.Frame(self.frame, bg="#5c5c5c")
        self.titleCanvas = _tk.Canvas(
            self.oFrame, bg="#5c5c5c", highlightthickness=0, width=480, height=48)
        self.titleCanvas.create_text(
            0, 0, text="Add shell", fill="cyan", anchor="nw", font=_utils.Font("Helvetica", 24).get_tuple())
        self.titleCanvas.place(
            x=int(_reg.Registry.gameData["WindowWidth"] / 2) - 240, y=320 - 48, anchor="nw")
        self.optionsFrame = _tk.Frame(self.oFrame, bg="#5c5c5c", width=480)

        self.nameEntryFrame = _tk.Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        self.nameLabel = _ttk.Label(self.nameEntryFrame, relief="flat", width=8, text="Name:", anchor="w")
        self.nameLabel.pack(side="left")
        self.nameEntry = _ttk.Entry(self.nameEntryFrame)
        self.nameEntry.pack(side="left", fill="x", expand=True)
        self.nameEntryFrame.pack(fill="x", expand=True, padx=1, pady=1)

        self.seedEntryFrame = _tk.Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        self.seedLabel = _ttk.Label(self.seedEntryFrame, relief="flat", width=8, text="Seed:", anchor="w")
        self.seedLabel.pack(side="left")
        self.seedEntry = _ttk.Entry(self.seedEntryFrame)
        self.seedEntry.pack(side="left", fill="x", expand=True)
        self.seedEntry.bind("<Key>", update)
        self.seedEntryFrame.pack(fill="x", expand=True, padx=1, pady=1)

        self.gameMapsEntryFrame = _tk.Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        # self.gameMapsScrollWindow = ScrolledWindow(self.gameMapsEntryFrame, 400, 200)

        i = 0

        class Self2:
            selectedCanvas: _tk.Canvas = None
            hoverCanvasOld: _tk.Canvas = None
            oldSelected: _tk.Canvas = None
            id_ = {}

        def on_canv_leave(hover_canvas):
            if Self2.hoverCanvasOld is not None:
                if Self2.selectedCanvas != Self2.hoverCanvasOld:
                    Self2.hoverCanvasOld.config(bg="#434343")
                    Self2.hoverCanvasOld.itemconfig(Self2.id_[Self2.hoverCanvasOld]["Title"], fill="#7f7f7f")
                    # for subid in Self2.id_[Self2.hoverCanvasOld]["Infos"]:
                    #     Self2.hoverCanvasOld.itemconfig(subid, fill="#7f7f7f")
                else:
                    Self2.hoverCanvasOld.config(bg="darkcyan")
                    Self2.hoverCanvasOld.itemconfig(Self2.id_[hover_canvas]["Title"], fill="#00bfbf")
                    # for subid in Self2.id_[Self2.hoverCanvasOld]["Infos"]:
                    #     Self2.hoverCanvasOld.itemconfig(subid, fill="#00a7a7")
            Self2.hoverCanvasOld = None

        def on_canv_motion(hover_canvas):
            if Self2.hoverCanvasOld == hover_canvas:
                return
            if Self2.hoverCanvasOld is not None:
                if Self2.selectedCanvas != Self2.hoverCanvasOld:
                    Self2.hoverCanvasOld.config(bg="#434343")
                    Self2.hoverCanvasOld.itemconfig(Self2.id_[Self2.hoverCanvasOld]["Title"], fill="#7f7f7f")
                    # for subid in Self2.id_[Self2.hoverCanvasOld]["Infos"]:
                    #     Self2.hoverCanvasOld.itemconfig(subid, fill="#939393")
                else:
                    Self2.hoverCanvasOld.config(bg="darkcyan")
                    Self2.hoverCanvasOld.itemconfig(Self2.id_[hover_canvas]["Title"], fill="#007f7f")
                    # for subid in Self2.id_[Self2.hoverCanvasOld]["Infos"]:
                    #     Self2.hoverCanvasOld.itemconfig(subid, fill="#00a7a7")
            # print(Self2.selectedCanvas, Self2.hoverCanvasOld)
            # print(Self2.selectedCanvas == Self2.hoverCanvasOld)
            # print(Self2.selectedCanvas == hover_canvas)
            Self2.hoverCanvasOld = hover_canvas

            if hover_canvas != Self2.selectedCanvas:
                hover_canvas.config(bg="#5c5c5c")
                hover_canvas.itemconfig(Self2.id_[hover_canvas]["Title"], fill="#a7a7a7")
                # for subid in Self2.id_[hover_canvas]["Infos"]:
                #     hover_canvas.itemconfig(subid, fill="#dadada")
            else:
                hover_canvas.config(bg="#43a7a7")
                hover_canvas.itemconfig(Self2.id_[hover_canvas]["Title"], fill="#ffffff")
                # for subid in Self2.id_[hover_canvas]["Infos"]:
                #     hover_canvas.itemconfig(subid, fill="#00dada")
            Self2.hoverCanvas = hover_canvas

        def on_canv_lclick(c: _tk.Canvas):
            if Self2.oldSelected is not None:
                Self2.oldSelected.config(bg="#434343")
                Self2.oldSelected.itemconfig(Self2.id_[Self2.oldSelected]["Title"], fill="#434343")
                # for subid in Self2.id_[Self2.oldSelected]["Infos"]:
                #     Self2.oldSelected.itemconfig(subid, fill="#939393")
            Self2.oldSelected = c

            c.config(bg="#43a7a7")
            c.itemconfig(Self2.id_[c]["Title"], fill="#ffffff")
            # for subid in Self2.id_[c]["Infos"]:
            #     c.itemconfig(subid, fill="#00dada")

            Self2.selectedCanvas = c

        vlw = 400

        game_maps = _reg.Registry.get_gamemap_objects()

        self.gameMapCanv = {}

        self.seedLabel = _ttk.Label(self.gameMapsEntryFrame, relief="flat", width=8, text="Seed:", anchor="w")
        self.seedLabel.pack(side="left")

        # Main frame.
        Self2.main_f = _tk.Frame(self.gameMapsEntryFrame, background="#434343", height=200)
        Self2.main_f.pack(side="left", fill="x")

        # Slots frame.
        Self2.s_frame = _tk.Frame(Self2.main_f, height=200, width=vlw)
        Self2.s_frame.pack(fill="x")

        # Scrollwindow for the slots frame
        Self2.sw = _special.ScrolledWindow(Self2.s_frame, vlw, 200, expand=True, fill="both")

        Self2.sw.vbar.configure(bg="#434343", fg="#7f7f7f")

        # Configurate the canvas from the scrollwindow
        Self2.canv = Self2.sw.canv
        Self2.canv.config(bg="#434343")

        # Self2.oFrame.
        Self2.frame_sw = Self2.sw.scrollwindow
        Self2.frames = []
        Self2.canvass = []
        Self2.index = {}

        self.self2 = Self2

        # Creates items in the versions menu.
        for gameMap in game_maps:
            gameMap: _maps.GameMap
            Self2.frames.append(_tk.Frame(Self2.frame_sw, height=32, width=vlw, bd=0))
            Self2.canvass.append(
                _tk.Canvas(Self2.frames[-1], height=32, width=vlw, bg="#434343", highlightthickness=0, bd=0))
            Self2.canvass[-1].pack()
            Self2.id_[Self2.canvass[-1]] = {}
            self.gameMapCanv[Self2.canvass[-1]] = gameMap
            # Self2.._id[Self2..canvass[-1]]["Icon"] = Self2..canvass[-1].create_image(0, 0, image=Self2..iconMinecraft,
            #                                                                    anchor="nw")
            Self2.id_[Self2.canvass[-1]]["Title"] = Self2.canvass[-1].create_text(5, 15, text=_reg.Registry.get_lname(
                "gamemap", gameMap.get_uname().split(":")[-1], "name"),
                                                                                  fill="#7f7f7f", anchor="w",
                                                                                  font=("helvetica", 11))
            Self2.canvass[-1].bind(
                "<ButtonRelease-1>", lambda event, c=Self2.canvass[-1]: on_canv_lclick(c))
            # Self2.canvass[-1].bind(
            #     "<Double-Button-1>", lambda event, v=profile.name: Self2.add_action(v))
            Self2.canvass[-1].bind(
                "<Motion>", lambda event, c=Self2.canvass[-1]: on_canv_motion(c))
            Self2.canvass[-1].bind(
                "<Leave>", lambda event, c=Self2.canvass[-1]: on_canv_leave(c))
            Self2.index[Self2.canvass[-1]] = i
            Self2.frames[-1].pack(side="top")

            i += 1

        Self2.s_frame.pack()
        Self2.s_frame.pack_propagate(1)

        self.gameMapsEntryFrame.pack(fill="x", expand=True, padx=1, pady=1)

        self.buttonFrame = _tk.Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        self.emptyLabel = _ttk.Label(self.buttonFrame, relief="flat", width=8, text="", anchor="w")
        self.emptyLabel.pack(side="left")
        self.cancelBtn = _ttk.Button(self.buttonFrame, command=lambda: self.close_options_frame(), text="Cancel")
        self.resetBtn = _ttk.Button(
            self.buttonFrame, command=lambda: self.add_action(self.nameEntry.get(), self.seedEntry.get()), text="Add")
        self.cancelBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)  # , height=20)
        self.resetBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)  # , height=20)
        self.buttonFrame.pack(fill='x', side="bottom", expand=True)

        root.update()
        root.update_idletasks()
        self.optionsFrame.place(x=int(_reg.Registry.gameData["WindowWidth"] / 2) - 240 - 69, y=320, anchor="nw",
                                width=480)

        # self.textInput = ttk.Entry()
        self.oFrame.pack(fill="both", expand=True)

    def rename_save(self):
        if self.selectedCanvas is None:
            return
        else:
            src = self.names[self.selectedCanvas]

        root = _reg.Registry.get_window("default")

        self.oFrame.destroy()
        self.oFrame = _tk.Frame(self.frame, bg="#5c5c5c")
        self.titleCanvas = _tk.Canvas(self.oFrame, bg="#5c5c5c", highlightthickness=0, width=480, height=48)
        self.titleCanvas.create_text(0, 0, text=f"Rename save '{src}'", fill="cyan", anchor="nw", font=("Consolas", 24))
        self.titleCanvas.place(x=int(_reg.Registry.gameData["WindowWidth"] / 2) - 240, y=320 - 48, anchor="nw")
        self.optionsFrame = _tk.Frame(self.oFrame, bg="#5c5c5c", width=480)

        self.nameEntryFrame = _tk.Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        self.nameLabel = _ttk.Label(self.nameEntryFrame, relief="flat", width=8, text="Name:", anchor="w")
        self.nameLabel.pack(side="left")
        self.nameEntry = _ttk.Entry(self.nameEntryFrame)
        self.nameEntry.pack(side="left", fill="x", expand=True)
        self.nameEntryFrame.pack(fill="x", expand=True, padx=1, pady=1)

        self.buttonFrame = _tk.Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        self.emptyLabel = _ttk.Label(self.buttonFrame, relief="flat", width=8, text="", anchor="w")
        self.emptyLabel.pack(side="left")
        self.cancelBtn = _ttk.Button(self.buttonFrame, command=lambda: self.close_options_frame(), text="Cancel")
        self.renameBtn = _ttk.Button(self.buttonFrame, command=lambda: self.rename_action(src, self.nameEntry.get()),
                                     text="Add")
        self.cancelBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)  # , height=20)
        self.renameBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)  # , height=20)
        self.buttonFrame.pack(fill='x', side="bottom", expand=True)

        root.update()
        root.update_idletasks()
        self.optionsFrame.place(x=int(_reg.Registry.gameData["WindowWidth"] / 2) - 240 - 69, y=320, anchor="nw",
                                width=480)

        self.textInput = _ttk.Entry()
        self.oFrame.pack(fill="both", expand=True)

    def add_action(self, new, seed):
        """
        Adding a slot to your game.

        :param seed: Seed (integer) for the new save
        :param new: Name of the new save
        :return:
        """

        max_seed = 2 ** 32

        if seed == "":
            seed = random.randint(0, max_seed)

        print(max_seed)

        seed = int(seed)

        import os

        if (new in ("aux", "con", "num", "..")) or (len(new) < 3) or (
                new.lower() in [f.lower() for f in
                                os.listdir(f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/")]):
            return

        if self.self2.selectedCanvas is None:
            return
        game_map = self.gameMapCanv[self.self2.selectedCanvas]

        # Creating dir for the game.
        os.makedirs(f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/" + new, exist_ok=True)

        print(game_map.get_uname())

        game_map.create_savedata(f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/{new}", seed)
        self.close_options_frame()

    def reset_action(self, src):
        """
        Resets the game save

        :param src: Name of the save
        :return:
        """

        max_seed = 2 ** 32
        seed = random.randint(0, max_seed)

        try:
            _temp_0002 = _conf.Reader(
                f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/{src}/game.nzt").get_decoded()
            game_map = _reg.Registry.get_gamemap(_temp_0002["GameMap"]["id"])
            seed = _temp_0002["GameMap"]["seed"]

            game_map.create_savedata(f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/{src}", seed)
            self.close_options_frame()
        except KeyError or AttributeError or IndexError or NameError:
            game_map = _reg.Registry.get_gamemap("qbubbles:classic_map")

            game_map.create_savedata(f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/{src}", seed)
            self.close_options_frame()

    def open_direct(self, n_):
        """
        Open the game direct from the name

        :param n_: The name of the save
        :return:
        """

        self.open_action(n_)

    # noinspection PyTypeChecker
    def remove_action(self, src):
        """
        Deletes the save.

        :param src: The name of the save
        :return:
        """

        import os

        # Removing the files inside.
        for i in os.listdir(f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/" + src):
            os.remove(f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/" + src + "/" + i)

        # Remove the slot (dir)
        os.removedirs(f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/" + src)

        self.close_options_frame()

    def rename_action(self, src, new):
        """
        Renames a save.

        :param src: Source name of the save
        :param new: New name of the save
        :return:
        """

        import os

        # noinspection PyTypeChecker
        # Rename the dir for the slot.
        os.rename(f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/" + src,
                  f"{_reg.Registry.gameData['launcherConfig']['gameDir']}saves/" + new)

        self.close_options_frame()

    def open_save(self):
        if self.selectedCanvas is None:
            return
        else:
            src = self.names[self.selectedCanvas]

        self.open_action(src)

    def open_action(self, src):
        """
        Opens and run the game save.

        :param src: Name of the save
        :return:
        """

        # Runs the game
        self.scenemanager.change_scene("Game", src)

    def back_title(self):
        self.scenemanager.change_scene("TitleScreen")


class OptionsMenu(_scenemgr.Scene):
    def __init__(self):
        super(OptionsMenu, self).__init__(_reg.Registry.get_window("default"))

        # Initialize options menu variables
        self.lang_selected = _tk.StringVar(self.frame)

        # Create top frame
        self.frame3 = _tk.Frame(self.frame, height=700, width=1000, bg="#5c5c5c")
        self.frame3.pack()

        # Create bottom frame
        self.frame4 = _tk.Frame(self.frame, height=20, bg="#5c5c5c")
        self.frame4.pack(side="bottom", fill="x")

        # Create language option
        self.lang_lbl = _tk.Label(
            self.frame3, text=_reg.Registry.gameData["launguage"]["options.language"], bg="#5c5c5c")
        self.lang_lbl.grid(row=0, column=0)
        self.lang_btn = _tk.Menubutton(
            self.frame3, textvariable=_reg.Registry.gameData["config"]["selectedLanguage"], bg="#3c3c3c", fg="#9c9c9c")
        self.lang_btn.grid(row=0, column=1)

        # Create save button
        self.save = _tk.Button(
            self.frame4, text=_reg.Registry.gameData["language"]["options.save"], width=7, command=self.options_save,
            bg="#3c3c3c", fg="#9c9c9c")
        self.save.pack(side="right")

        a = os.listdir("lang/")
        b = []
        c = []
        self.lang_btn.menu = _tk.Menu(self.lang_btn, tearoff=0)
        self.lang_btn["menu"] = self.lang_btn.menu

        for i in a:
            file = open("lang/" + i, "r")
            b.append(_yml.safe_load(file)["options.name"])
            c.append(i)
            file.close()

        d = 0
        for i in range(len(b)):
            self.lang_btn.menu.add_checkbutton(label=b[i], command=lambda: self.lang_selected.set(c[i]))
            d += 1

    def options_save(self):

        with open("lang/" + self.lang_selected.get(), "r") as file:
            _reg.Registry.gameData["languages"] = _yml.safe_load(file.read())
            file.close()

        self.scenemanager.change_scene("TitleScreen")


class ErrorScene(_scenemgr.CanvasScene):
    def __init__(self):
        root = _reg.Registry.get_window("default")
        super(ErrorScene, self).__init__(root)

        mx = _reg.Registry.gameData["MiddleX"]
        my = _reg.Registry.gameData["MiddleY"]
        h = _reg.Registry.gameData["WindowHeight"]
        w = _reg.Registry.gameData["WindowWidth"]
        self.t0 = self.canvas.create_rectangle(0, 0, _reg.Registry.gameData["WindowWidth"],
                                               _reg.Registry.gameData["WindowHeight"], fill="#ff0000",
                                               outline="#ff0000")
        # self.t1 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] - 2,
        #                              text="Loading Mods", anchor="s",
        #                              font=("Helvetica", root.tkScale(40)), fill="#ffa7a7")
        # self.t2 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] + 2,
        #                              text="", anchor="n",
        #                              font=("Helvetica", root.tkScale(15)), fill="#ffa7a7")
        # self.canvas.update()

        # self.t0 = CPanel(self.canvas, 0, 0, width="extend", height="expand", fill="#ff0000", outline="#ff0000")
        font1 = _tk.font.Font(font=("Consolas", 50, "bold"))
        font2 = _tk.font.Font(font=("Consolas", 15))
        _tk.font.Font()
        self.t1 = _gui.CText(
            self.canvas, mx, my - 5, text="", anchor="s", fill="#ffa7a7", font=font1)
        self.t2 = _gui.CText(
            self.canvas, mx, my + 5, text="", anchor="n", fill="#ffa7a7", font=font2)
        self.t3 = _gui.CText(
            self.canvas, w - 15, h - 15, text="Press any key or mouse button to continue", anchor="se", fill="#ffa7a7",
            font=font2)

    def show_scene(self, t1: str, t2: str):
        super(ErrorScene, self).show_scene(t1, t2)
        # self.canvas.itemconfig(self.t0, fill="#ff0000")
        # self.canvas.itemconfig(self.t1, text=t1, fill="#ffa7a7")
        # self.canvas.itemconfig(self.t2, text=t2, fill="#ffa7a7")
        # self.canvas.create_text(Registry.gameData["WindowWidth"]-16, Registry.gameData["WindowHeight"]-16,
        #                         text="Press any key or mouse button to continue", anchor="se",
        #                         font=("Helvetica", Registry.get_window("default").tkScale(16), 'bold'), fill="#ffa7a7")
        # Registry.get_window("default").focus_set()
        # self.canvas.bind_all("<Key>", lambda evt: os.kill(os.getpid(), 1))
        # self.canvas.bind_all("<Button>", lambda evt: os.kill(os.getpid(), 1))
        # Registry.get_window("default").protocol("WM_DELETE_WINDOW", lambda: None)
        # self.canvas.update()
        # self.canvas.mainloop()
        self.t1.configure(text=t1)
        self.t2.configure(text=t2)
        _reg.Registry.get_window("default").focus_set()
        self.canvas.bind_all("<Key>", lambda evt: os.kill(os.getpid(), 1))
        self.canvas.bind_all("<Button>", lambda evt: os.kill(os.getpid(), 1))
        _reg.Registry.get_window("default").protocol("WM_DELETE_WINDOW", lambda: None)
        self.canvas.mainloop()


class CrashScene(_scenemgr.CanvasScene):
    def __init__(self):
        root = _reg.Registry.get_window("default")
        super(CrashScene, self).__init__(root)

        mx = _reg.Registry.gameData["MiddleX"]
        my = _reg.Registry.gameData["MiddleY"]
        h = _reg.Registry.gameData["WindowHeight"]
        w = _reg.Registry.gameData["WindowWidth"]
        self.t0 = self.canvas.create_rectangle(0, 0, _reg.Registry.gameData["WindowWidth"],
                                               _reg.Registry.gameData["WindowHeight"], fill="#ff0000",
                                               outline="#ff0000")
        # self.t1 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] - 2,
        #                              text="Loading Mods", anchor="s",
        #                              font=("Helvetica", root.tkScale(40)), fill="#ffa7a7")
        # self.t2 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] + 2,
        #                              text="", anchor="n",
        #                              font=("Helvetica", root.tkScale(15)), fill="#ffa7a7")
        # self.canvas.update()

        # self.t0 = CPanel(self.canvas, 0, 0, width="extend", height="expand", fill="#ff0000", outline="#ff0000")
        font1 = _tk.font.Font(font=("Consolas", root.tkScale(50), "bold"))
        font2 = _tk.font.Font(font=("Consolas", root.tkScale(15)))
        font3 = _tk.font.nametofont("TkFixedFont").configure(size=root.tkScale(10))
        # font.Font()
        self.t1 = _gui.CText(
            self.canvas, mx, my - root.tkScale(155), text="", anchor="s", fill="#ffa7a7", font=font1)
        self.t2 = _gui.CText(
            self.canvas, mx, my - root.tkScale(145), text="", anchor="n", fill="#ffa7a7", font=font2)
        self.t3 = _gui.CText(
            self.canvas, mx, my - root.tkScale(115), text="", anchor="n", fill="#ffa7a7", font=font2)
        self.t5 = _gui.CText(
            self.canvas, mx, my - root.tkScale(85),
            text="Click on the button on the top to go the the webpage (if you don't use mods)", anchor="n",
            fill="#ffa7a7",
            font=font2)
        self.t4 = _gui.CText(
            self.canvas, w - root.tkScale(15), h - root.tkScale(15), text="Press Alt+F4 to quit", anchor="se",
            fill="#ffa7a7",
            font=font2)
        self.frame2 = _tk.Frame(self.frame, bg="#a70000", height=root.tkScale(350), width=root.tkScale(1000))
        self.frame2.place(x=mx, y=my - root.tkScale(30), anchor="n", height=root.tkScale(350), width=root.tkScale(1000))
        self.t6 = _tk.Text(self.frame2, relief="flat", border=0, bd=root.tkScale(5), state="disabled", bg="#a70000",
                           foreground="#ffa7a7",
                           font=font3, selectforeground="#ffffff", selectbackground="#ff0000")
        self.t6.pack(side="left", fill="both", expand=True)
        self.scrollbar = _special.CustomVerticalScrollbar(self.frame2, width=root.tkScale(10), command=self.t6.yview,
                                                          bg="#a70000", fg="#ffa7a7", bd=0)
        self.scrollbar.pack(side="left", fill="y")
        self.t6.config(yscrollcommand=self.scrollbar.set)
        self.t7 = _tk.Button(self.frame, text="Open Issue Tracker (Not for Mods!)", bg="#ff7f7f", fg="#ffffff",
                             width=72, font=font2,
                             command=lambda: os.startfile("https://github.com/Qboi123/QplayBubbles-Releaes/issues"),
                             relief="flat", border=0)
        self.t7.place(x=mx, y=my - root.tkScale(250), anchor="s")
        self.exc = False
        # self.scrollbar.config(command=self.t4.yview)

    def hide_scene(self):
        return

    def show_scene(self, crashlog: str):
        super(CrashScene, self).show_scene()
        if self.exc is True:
            return
        self.exc = True
        # self.canvas.itemconfig(self.t0, fill="#ff0000")
        # self.canvas.itemconfig(self.t1, text=t1, fill="#ffa7a7")
        # self.canvas.itemconfig(self.t2, text=t2, fill="#ffa7a7")
        # self.canvas.create_text(Registry.gameData["WindowWidth"]-16, Registry.gameData["WindowHeight"]-16,
        #                         text="Press any key or mouse button to continue", anchor="se",
        #                         font=("Helvetica", Registry.get_window("default").tkScale(16), 'bold'), fill="#ffa7a7")
        # Registry.get_window("default").focus_set()
        # self.canvas.bind_all("<Key>", lambda evt: os.kill(os.getpid(), 1))
        # self.canvas.bind_all("<Button>", lambda evt: os.kill(os.getpid(), 1))
        # Registry.get_window("default").protocol("WM_DELETE_WINDOW", lambda: None)
        # self.canvas.update()
        # self.canvas.mainloop()
        self.t1.configure(text="Fatal Error occoured")
        self.t2.configure(text="If you use mods, report the log below to thier issue tracker.")
        self.t3.configure(text="If you don't use mods, report the log below on the issue tracker")
        self.t6.config(state="normal")
        self.t6.insert('end', crashlog)
        self.t6.config(state="disabled")
        _reg.Registry.get_window("default").focus_set()
        _reg.Registry.get_window("default").focus_get()
        # Registry.get_window("default").wm_iconify()
        # Registry.get_window("default").bind_all("<Control-Q>", lambda evt: os.kill(os.getpid(), 1))
        # self.canvas.bind_all("<Button>", lambda evt: os.kill(os.getpid(), 1) if evt.widget == self.canvas else None)
        _reg.Registry.get_window("default").protocol("WM_DELETE_WINDOW", lambda: None)
        _reg.Registry.get_window("default").bind_all("<Alt-F4>", lambda evt: os.kill(os.getpid(), 0))
        self.canvas.bind("<Alt-F4>", lambda evt: os.kill(os.getpid(), 0))
        self.t6.bind("<Alt-F4>", lambda evt: os.kill(os.getpid(), 0))
        self.scrollbar.bind("<Alt-F4>", lambda evt: os.kill(os.getpid(), 0))
        self.canvas.mainloop()


def custom_excepthook(exc_type, exc_val, exc_tb):
    # noinspection PyBroadException
    try:
        scenemanager: _t.Optional[_scenemgr.SceneManager] = _reg.Registry.get_scenemanager()
        if scenemanager is None:
            sys.__excepthook__(exc_type, exc_val, exc_tb)
    except Exception:
        scenemanager = None

    if exc_type == KeyboardInterrupt:
        os.kill(os.getpid(), 0)

    try:
        import traceback
        # crashlog = traceback.walk_tb(exc_tb)
        # print(list(crashlog))
        crashlog = traceback.format_exception(exc_type, exc_val, exc_tb)
        for line in crashlog:
            for line2 in line.splitlines(False):
                _gameIO.printerr(line2)
        # print(''.join(list(crashlog)))
        if scenemanager is not None:
            scenemanager.change_scene("qbubbles:CrashScene", "Fatal Error occoured", "See log below for info.",
                                      ''.join(list(crashlog))[:-1])
    except Exception as e:
        _gameIO.printerr(f"{e.__class__.__name__}: {e.__str__()}")
        sys.__excepthook__(e.__class__, e, e.__traceback__)


def report_callback_exception(exc, val, tb):
    """Report callback exception on sys.stderr.

    Applications may want to override this internal function, and
    should when sys.stderr is None."""
    # print("Exception in Tkinter callback", file=sys.stderr)

    exc, val, tb = sys.exc_info()
    # noinspection PyBroadException
    try:
        scenemanager: _t.Optional[_scenemgr.SceneManager] = _reg.Registry.get_scenemanager()
        if scenemanager is None:
            sys.__excepthook__(exc, val, tb)
    except Exception:
        scenemanager = None

    if exc == KeyboardInterrupt:
        os.kill(os.getpid(), 0)

    try:
        import traceback
        # crashlog = traceback.walk_tb(tb)
        # print(list(crashlog))
        exception_format = traceback.format_exception(exc, val, tb)
        if _reg.Registry.get_scene("qbubbles:CrashScene").exc:
            return
        crashlog = "Exception in Tkinter callback\n" + ''.join(list(exception_format))
        for line in exception_format:
            for line2 in line.splitlines(False):
                _gameIO.printerr(line2)
                # crashlog += line2
        # print(''.join(list(crashlog)))
        if scenemanager is not None:
            scenemanager.change_scene("qbubbles:CrashScene", crashlog[:-1])
    except Exception as e:
        _gameIO.printerr(f"{e.__class__.__name__}: {e.__str__()}")
        sys.__excepthook__(e.__class__, e, e.__traceback__)


def error2():
    raise Exception("Test Exception")


def error():
    error2()


if __name__ == '__main__':
    sys.excepthook = custom_excepthook

    error()

    # raise Exception("Test Exception")
