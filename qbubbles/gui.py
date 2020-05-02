from tkinter import Canvas, PhotoImage
from typing import Optional, Tuple, Union, Callable, Any
from zipimport import zipimporter
import tkinter as _tk
import tkinter.ttk as _ttk
import typing as _t

from PIL import ImageTk, Image
from overload import overload
from qbubbles.registry import Registry

from qbubbles.resources import Resources

from qbubbles.events import ResizeEvent
from qbubbles.special import CustomVerticalScrollbar, CustomHorizontalScrollbar


class CRectangle(object):
    def __init__(self, canvas: Canvas, x1, y1, x2, y2, *, fill="", outline="", anchor="center", tags=tuple()):
        self._id = canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline)  # , anchor=anchor)
        self._canvas = canvas
        # print("CRectangle created")

    def get_id(self):
        return self._id

    def move(self, x=None, y=None):
        return self._canvas.move(self._id, x, y)

    def coords(self, x1, y1, x2, y2) -> Optional[Tuple[float, float, float, float]]:
        return self._canvas.coords(self._id, x1, y1, x2, y2)

    def bind(self, sequence=None, func=None, add=None) -> Union[str, int]:
        return self._canvas.tag_bind(self._id, sequence, func, add)

    def unbind(self, sequence, funcid=None):
        return self._canvas.tag_unbind(self._id, sequence, funcid)

    def configure(self, fill=None, outline=None, anchor=None, tags=None):
        return self._canvas.itemconfigure(self._id, fill=fill, outline=outline, anchor=anchor, tags=tags)

    def cget(self, option) -> Union[str, int, float, bool, list, dict, Callable]:
        return self._canvas.itemcget(self._id, option)

    def lower(self, *args):
        return self._canvas.tag_lower(self._id, *args)

    def raise_(self, *args):
        return self._canvas.tag_raise(self._id, *args)

    config = configure


class CImage(object):
    def __init__(self, canvas: Canvas, x, y, *, image, anchor="center", tags=tuple()):
        self._id = canvas.create_image(x, y, image=image, anchor=anchor, tags=tags)  # , anchor=anchor)
        self._canvas: Canvas = canvas
        self._image: Union[ImageTk.PhotoImage, PhotoImage] = image
        self._anchor = anchor
        self._tags = tags

    def get_id(self):
        return self._id

    def move(self, x=None, y=None):
        return self._canvas.move(self._id, x, y)

    @overload
    def coords(self, x1, y1) -> None:
        self._canvas.coords(self._id, x1, y1)

    @coords.add
    def coords(self) -> Optional[Tuple[float, float]]:
        return self._canvas.coords(self._id)

    def bind(self, sequence=None, func=None, add=None) -> Union[str, int]:
        return self._canvas.tag_bind(self._id, sequence, func, add)

    def unbind(self, sequence, funcid=None):
        return self._canvas.tag_unbind(self._id, sequence, funcid)

    def configure(self, *, image=None, anchor=None, tags=None):
        if image is None:
            image=self._image
        if anchor is None:
            anchor=self._anchor
        if tags is None:
            tags=self._tags
        return self._canvas.itemconfigure(self._id, image=image, anchor=anchor, tags=tags)

    def cget(self, option) -> Union[str, int, float, bool, list, dict, Callable]:
        return self._canvas.itemcget(self._id, option)

    def lower(self, *args):
        return self._canvas.tag_lower(self._id, *args)

    def raise_(self, *args):
        return self._canvas.tag_raise(self._id, *args)

    config = configure


class CText(object):
    def __init__(self, canvas: Canvas, x, y, *, text, anchor="center", fill="", tags=tuple(), font=("Helvetica", 10)):
        self._id = canvas.create_text(x, y, text=text, anchor=anchor, tags=tags, fill=fill, font=font)
        self._canvas: Canvas = canvas
        self._text: str = text
        self._anchor = anchor
        self._tags = tags
        self._fill = fill
        self._font = font

    def get_id(self):
        return self._id

    def move(self, x=None, y=None):
        return self._canvas.move(self._id, x, y)

    @overload
    def coords(self, x1, y1) -> None:
        self._canvas.coords(self._id, x1, y1)

    @coords.add
    def coords(self) -> Optional[Tuple[float, float]]:
        return self._canvas.coords(self._id)

    def bind(self, sequence=None, func=None, add=None) -> Union[str, int]:
        return self._canvas.tag_bind(self._id, sequence, func, add)

    def unbind(self, sequence, funcid=None):
        return self._canvas.tag_unbind(self._id, sequence, funcid)

    def configure(self, *, text=None, anchor=None, tags=None, fill=None, font=None):
        if text is None:
            text = self._text
        if anchor is None:
            anchor = self._anchor
        if tags is None:
            tags = self._tags
        if fill is None:
            fill = self._fill
        if font is None:
            font = self._font
        return self._canvas.itemconfigure(self._id, text=text, anchor=anchor, tags=tags, fill=fill, font=font)

    def cget(self, option) -> Union[str, int, float, bool, list, dict, Callable]:
        return self._canvas.itemcget(self._id, option)

    def lower(self, *args):
        return self._canvas.tag_lower(self._id, *args)

    def raise_(self, *args):
        return self._canvas.tag_raise(self._id, *args)

    config = configure


class CPanel(CRectangle):
    def __init__(self, canvas: Canvas, x, y, width, height, fill="", outline=""):
        self._width = width
        self._height = height
        if width == "extend":
            width = canvas.winfo_width()
        if height == "expand":
            height = canvas.winfo_height()
        self.x = x
        self.y = y
        super(CPanel, self).__init__(canvas, x, y, width, height, fill=fill, outline=outline, anchor="nw")

    def on_resize(self, event: ResizeEvent):
        # noinspection PyDeepBugsBinOperand
        if self._width == "extend":
            width = self._canvas.winfo_width() - self.x
        if self._height == "expand":
            height = self._canvas.winfo_height() - self.y
        self.coords(self.x, self.y, self._width, self._height)


class CEffectBarArea(object):
    def __init__(self, canvas, *, gamemap):
        self.effectbars = CEffectBar

    def add_effect(self, applied_effect):
        pass


class CEffectBar(object):
    def __init__(self, canvas, x, y, *, gamemap, effect):
        barimage = Registry.get_texture("qbubbles:gui", "qbubbles:effect_bar", gamemap=gamemap)
        effectimage = Registry.get_texture("qbubbles:effect", effect.get_uname(), gamemap=gamemap)

        self.cBarimage = CImage(canvas, x, y, image=barimage, anchor="nw")
        self.cEffectimage = CImage(canvas, x+2, y+2, image=effectimage, anchor="nw")
        self._effect = effect

    def get_effect(self):
        return self._effect


class QAccentButton(_ttk.Widget):
    def __init__(self, master, **kw):
        kw['style'] = 'QAccentButton'
        kw['class'] = 'QAccentButton'

        command = kw.pop("command", lambda: None)

        def on_enter(evt):
            if evt.widget == self:
                state = list(self.state())
                state.append("active")
                self.state(("active",))

        def on_leave(evt):
            # print("Leave")
            if evt.widget == self:
                state = list(self.state())
                state.append("!active")
                self.state(("!active",))

        def on_press(evt):
            if evt.widget == self:
                state = list(self.state())
                state.append("pressed")
                self.state(("pressed",))

        def on_release(evt):
            if evt.widget == self:
                state = list(self.state())
                state.remove("pressed")
                state.append("!pressed")
                self.state(("!pressed",))
                self.command()

        super(QAccentButton, self).__init__(master, "ttk::button", kw)
        self.command = command
        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)
        self.bind("<ButtonPress-1>", on_press)
        self.bind("<ButtonRelease-1>", on_release)


class QScrollableFrameInner(_ttk.Widget):
    def __init__(self, master, **kw):
        """
        Inner Frame for QScrollableFrame, don't use it directly.

        :param master: The master widget, must be a container widget like a Frame.
        :param kw: Frame parameters
        """

        # Initialize super().__init__() **kw parameters
        kw["class"] = "QScrollableFrame"
        kw["style"] = "QScrollableFrame.Inner"

        # Super(...) call.
        super(QScrollableFrameInner, self).__init__(master, "ttk::frame", kw=kw)


class QInnerLabel(_ttk.Widget):
    def __init__(self, master, **kw):
        """
        Tkinter Label for using in QScrollableFrame, for theme purposes.

        :param master: The master widget, must be a container widget like a Frame.
        :param kw: Label parameters.
        """

        # Initialize super().__init__() **kw parameters
        kw["class"] = "QInnerLabel"
        kw["style"] = "QInnerLabel"

        # Super(...) call.
        super(QInnerLabel, self).__init__(master, "ttk::label", kw=kw)


# noinspection PyUnusedLocal
class QScrollableFrame(_ttk.Widget):
    def __init__(self, master, width=400, height=400, fillcontents=True, contentheight=None, contentwidth=None,
                 vscrollbar=True, hscrollbar=True, *args, scrollcommand=lambda: None, scrollbarbg=None,
                 scrollbarfg="darkgray", **kwargs):
        """
        1. Master widget gets scrollbars and a canvas. Scrollbars are connected
        to canvas scrollregion.

        2. self.scrollwindow is created and inserted into canvas

        Usage Guideline:
        ----------------
        Assign any widgets as children of <ScrolledWindow instance>.scrollwindow
        to get them inserted into canvas

        Example:
        ---------
        >>> from tkinter import Tk, Label
        >>> root = Tk()
        >>> scrollframe = QScrollableFrame(root, contentheight=1000, background="#3f3f3f", scrollbarbg="#3f3f3f",
        ...     scrollbarfg="#000fff")
        >>> labels = []
        >>> for index in range(0, 100):
        ...     label = Label(scrollframe, text=f"Label number: {index}")
        ...     label.pack()
        ...     labels.append(label)
        >>> scrollframe.pack()
        >>> root.mainloop()

        :param master: Master of the scrolled frame. Must be a QScrollableFrame, any type of Frame or any type of Labelframe
        :param width: Width of the scrolled frame.
        :param height: Height of the scrolled frame.
        :param expand: Whether to expand the scrolled frame.
        :param fill: Whether to fill the scrolled frame.
        :param contentheight: The content height of the scrolled frame.
        :param contentwidth: The content width of the scrolled frame.
        :param *args: Any additional arguments for default frame. (ttk.Frame)

        :param scrollcommand: The callable to call when scrolling.
        :param scrollbarbg: The background color of the scrollbar.
        :param scrollbarfg: The foreground color of the scrollbar.
        :param **kwargs: Any additional keyword arguments for default frame. (ttk.Frame)
        """

        # Initialize super().__init__() **kw parameters
        super_kw = {"class": "QScrollableFrame",
                    "style": "QScrollableFrame",
                    # "height": contentheight,
                    # "width": contentwidth}
                    }

        width -= 10

        if "width" in kwargs.keys():
            raise ValueError("Keyword argument width is defined multiple times.")
        if "height" in kwargs.keys():
            raise ValueError("Keyword argument height is defined multiple times.")

        # Defining the needed attributes.
        self.master: Union[_ttk.Frame, _tk.Frame, _tk.LabelFrame, _ttk.Labelframe, _tk.Tk, QScrollableFrame] = master
        self.scrollCommand: Callable[[], Any] = scrollcommand

        self._width = width
        self._height = height

        self._contentwidth = contentwidth = contentwidth if contentwidth is not None else width
        self._contentheight = contentheight = contentheight if contentheight is not None else height

        # Defining scroll region.
        scrollregion = (
            0, 0, contentwidth if contentwidth is not None else width, contentheight if contentheight is not None else height)

        self._frame = QScrollableFrameInner(self.master, width=width, height=height)
        self._frame.columnconfigure(0, weight=1)
        self._frame.rowconfigure(0, weight=1)

        self._frame2 = QScrollableFrameInner(self._frame, width=width, height=height)

        # Create the canvas.
        self._canvas = Canvas(
            self._frame2, bg='#FFFFFF', width=width, height=height, scrollregion=scrollregion, highlightthickness=0)

        # scrollbg = s.map("QScrollableFrame")["scrollbackground"]
        # scrollfg = s.map("QScrollableFrame")["scrollforeground"]

        # Create the vertical scrollbar.
        if vscrollbar:
            self._vertical_scrollbar = CustomVerticalScrollbar(
                self._frame, width=10, command=self._canvas.yview, bg=scrollbarbg, fg=scrollbarfg, bd=0)
        else:
            pass
            # self._vertical_blank = Canvas(self._frame, width=10, bg=scrollbarbg, highlightthickness=0)
        if hscrollbar:
            self._horizontal_scrollbar = CustomHorizontalScrollbar(
                self._frame, height=10, command=self._canvas.xview, bg=scrollbarbg, fg=scrollbarfg, bd=0)
        else:
            pass
            # self._horizontal_blank = Canvas(self._frame, height=10, bg=scrollbarbg, highlightthickness=0)

        self._vscrollbar = vscrollbar
        self._hscrollbar = hscrollbar
        self._scroll_gap = Canvas(self._frame, width=10, height=10, bg=scrollbarbg, highlightthickness=0)
        self._canvas.configure(yscrollcommand=self._vertical_scrollbar.set if vscrollbar else None,
                               xscrollcommand=self._horizontal_scrollbar.set if hscrollbar else None)

        self._fakecontent = _ttk.Frame(self._frame2, width=contentwidth, height=contentheight)
        self._frameinner = _ttk.Frame(self._frame2, width=contentwidth, height=contentheight)

        # Super(...) call.
        super(QScrollableFrame, self).__init__(self._frameinner, "ttk::frame", kw=super_kw)
        self._fakeinner = QScrollableFrameInner(self._fakecontent, width=contentwidth, height=contentheight)
        self._fakeinner.pack(fill="both", expand=True)
        self.fillcontents = fillcontents

        self.master: Union[_ttk.Frame, _tk.Frame, _tk.LabelFrame, _ttk.Labelframe, _tk.Tk, QScrollableFrame] = master

        # Create the frame into the canvas using canvas.create_window(...)
        self._c_fakewindow_id = self._canvas.create_window(
            0, 0, window=self._fakecontent, anchor='nw', height=contentheight, width=1)
        self._c_window_id = self._canvas.create_window(
            0, 0, window=self._frameinner, anchor='nw', height=contentheight, width=contentwidth)
        # self._canvas.tag_lower(self._c_fakewindow_id)
        self._canvas.tag_lower(self._c_fakewindow_id)
        self._canvas.tag_raise(self._c_window_id)

        super(QScrollableFrame, self).pack(fill="both", expand=True)

        # Pack the scrollbar and canvas.
        self._canvas.pack(side="left", fill="both", expand=True)
        if vscrollbar:
            self._vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        else:
            pass
            # self._vertical_blank.grid(row=0, column=1, sticky="ns")
        if hscrollbar:
            self._horizontal_scrollbar.grid(row=1, column=0, sticky="ew")
        else:
            pass
            # self._horizontal_blank.grid(row=1, column=0, sticky="ew")
        if (not vscrollbar) and (not hscrollbar):
            self._scroll_gap.grid(row=1, column=1, sticky="")
        self._frame2.grid(row=0, column=0, sticky="nswe")

        # Configure the canvas
        self._canvas.config(  # xscrollcommand=self.hbar.set,
            yscrollcommand=self._vertical_scrollbar.set if vscrollbar else None,
            xscrollcommand=self._horizontal_scrollbar.set if hscrollbar else None
        )    # scrollregion=scrollregion)

        self._canvas.tag_raise(self._c_window_id)
        # Bind default events
        self._frame.bind('<Configure>', self._configure_window)
        self._frame.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self._frameinner.bind_all("<MouseWheel>", self._on_mousewheel)
        # self._canvas.bind('<Enter>', self._bind_to_mousewheel)
        # self._canvas.bind('<Leave>', self._unbind_to_mousewheel)
        # self.bind("<Enter>", lambda evt: print("Enter QScrollableFrame"))

    def pack_configure(self, cnf: dict = None, **kw):
        if cnf is None:
            cnf = {}
        return self._frame.pack_configure(cnf, **kw)

    pack = pack_configure

    def pack_forget(self):
        return self._frame.pack_forget()

    def pack_info(self):
        return self._frame.pack_info()

    def pack_propagate(self, flag: _t.List[str] = None):
        return self._frame.pack_propagate(flag=flag)

    def pack_slaves(self):
        return self._frame.pack_slaves()

    def place_configure(self, cnf: dict = None, **kw):
        if cnf is None:
            cnf = {}
        return self._frame.place_configure(cnf, **kw)

    place = place_configure

    def place_forget(self):
        return self._frame.place_forget()

    def place_info(self):
        return self._frame.place_info()

    def place_slaves(self):
        return self._frame.place_slaves()

    def grid_anchor(self, anchor=None):
        return self._frame.grid_anchor(anchor)

    def grid_location(self, x, y):
        return self._frame.grid_location(x, y)

    def grid_bbox(self, column=None, row=None, col2=None, row2=None):
        return self._frame.grid_bbox(column, row, col2, row2)

    def grid_columnconfigure(self, index, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        return self._frame.grid_columnconfigure(index, cnf, **kw)

    def grid_configure(self, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        return self._frame.grid_configure(cnf, **kw)

    grid = grid_configure

    def grid_forget(self):
        return self._frame.grid_forget()

    def grid_info(self):
        return self._frame.grid_info()

    def grid_propagate(self, flag=None):
        return self._frame.grid_propagate(flag)

    def grid_remove(self):
        return self._frame.grid_remove()

    def grid_rowconfigure(self, index, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        return self._frame.grid_rowconfigure(index, cnf, **kw)

    def grid_size(self):
        return self._frame.grid_size()

    def grid_slaves(self, row=None, column=None):
        return self._frame.grid_slaves(row, column)

    def _grid_configure(self, command, index, cnf, kw):
        return self._frame._grid_configure(command, index, cnf, kw)

    def _gridconvvalue(self, value):
        return self._frame._gridconvvalue(value)

    def _bind_to_mousewheel(self, event):
        """
        Bind mousewheel event to the canvas

        :param event:
        :return:
        """

        print("Enter Canvas")
        # self._frame.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_to_mousewheel(self, event):
        """
        Unbind mousewheel event from the canvas

        :param event:
        :return:
        """

        print("Leave Canvas")
        # self._frame.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """
        Mousewheel event handler for the canvas

        :param event:
        :return:
        """

        if event.widget in [self._frame, self._canvas, self._frameinner, self]:
            self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _configure_window(self, event):
        """
        Update the scrollbars to match the size of the inner frame

        :param event:
        :return:
        """
        # print("Configure")

        # size = (self._frame.winfo_reqwidth(), self._frame.winfo_reqheight() + 1)
        # print(self._frame.pack_info())
        # self._canvas.config(scrollregion='0 0 %s %s' % size, width=event.width - 10, height=event.height - 10)

        fill_width = False
        fill_height = False
        if self._frame.pack_info()["fill"] == "x":
            fill_width = True
        elif self._frame.pack_info()["fill"] == "y":
            fill_height = True
        elif self._frame.pack_info()["fill"] == "both":
            fill_height = True
            fill_width = True

        # print(event.width, event.height)

        # Change the width:
        if 1:
            # Configuring subwidgets.
            self._frame2.configure(width=event.width - 10, height=event.height - 10)
            self._canvas.configure(width=event.width - 10, height=event.height - 10)  # Canvas
            # print(self._canvas.winfo_width(), self._canvas.winfo_height())

            if self.fillcontents:
                contentwidth_ = event.width - (10 if self._vscrollbar else 0)
                contentheight_ = event.height - (10 if self._hscrollbar else 0)
                if contentwidth_ > self._contentwidth:
                    contentwidth = contentwidth_
                else:
                    contentwidth = None
                if contentheight_ > self._contentheight:
                    contentheight = contentheight_
                else:
                    contentheight = None

                scrollregion = (0, 0, contentwidth_, contentheight_)
                # print(contentwidth, contentheight)
                # print(contentwidth_, contentheight_)
                # print(self._contentwidth, self._contentheight)

                if contentwidth is not None:
                    scrollregion = (0, 0, contentwidth_, self._contentheight)
                    self._canvas.configure(scrollregion=" ".join([item.__str__() for item in scrollregion]))
                    self._fakecontent.configure(width=contentwidth_)
                    self._fakeinner.configure(width=contentwidth_)
                    self._canvas.itemconfig(self._c_fakewindow_id, width=contentwidth_)
                if contentheight is not None:
                    scrollregion = (0, 0, self._contentwidth, contentheight_)
                    self._canvas.configure(scrollregion=" ".join([item.__str__() for item in scrollregion]))
                    self._fakecontent.configure(height=contentheight_)
                    self._fakeinner.configure(height=contentheight_)
                    self._canvas.itemconfig(self._c_fakewindow_id, height=contentheight_)
                self._frameinner.configure(width=contentwidth, height=contentheight)  # Inner Frame
                self._canvas.itemconfig(self._c_window_id, width=contentwidth, height=contentheight)  # Canvas Window
                self._canvas.update()
            else:
                contentwidth = event.width - (10 if self._vscrollbar else 0)
                contentheight = event.height - (10 if self._hscrollbar else 0)
                # contentwidth -= self._contentwidth
                # contentheight = contentheight  #  - (self._contentheight) + contentheight
                if contentwidth < 1:
                    contentwidth = 1
                if contentheight < 1:
                    contentheight = 1
                if contentwidth < self._contentwidth:
                    contentwidth = self._contentwidth
                if contentheight < self._contentheight:
                    contentheight = self._contentheight
                print(contentwidth, contentheight)
                self._fakecontent.configure(width=contentwidth, height=contentheight)
                self._fakeinner.configure(width=contentwidth, height=contentheight)
                self._canvas.itemconfig(self._c_fakewindow_id, width=contentwidth, height=contentheight)

                # contentwidth = (event.width - 10)
                # contentheight = (event.height - 10)
                # contentwidth = contentwidth
                # contentheight -= self._contentheight  #  - (self._contentheight) + contentheight
                # if contentwidth < 1:
                #     contentwidth = 1
                # if contentheight < 1:
                #     contentheight = 1
                # print(contentwidth, contentheight)
                # self._fakecontent2.configure(width=contentwidth, height=contentheight)
                # self._fakeinner2.configure(width=contentwidth, height=contentheight)
                # self._canvas.itemconfig(self._c_fakewindow_id2, width=contentwidth, height=contentheight)

        # self._frame.config(width=self._frame.winfo_reqwidth(), height=self._frame.winfo_reqheight())
        # if self.scrollwindow.winfo_reqwidth() != self.canv.winfo_width():
        #     # update the canvas's width to fit the inner frame
        #     # self.canv.config(width=self.scrollwindow.winfo_reqwidth())
        # if self.scrollwindow.winfo_reqheight() != self.canv.winfo_height():
        #     # update the canvas's width to fit the inner frame
        #     # self.canv.config(height=self.scrollwindow.winfo_reqheight())

    def configure(self, cnf=None, **kw):
        # Redefining width and height
        width = kw.pop('width', self._width)
        height = kw.pop('height', self._height)
        self._width = width
        self._height = height

        # Redefining and recaluculating the content size.
        contentwidth = kw.pop('contentwidth', self._contentwidth)
        contentheight = kw.pop('contentheight', self._contentheight)
        self._contentwidth = contentwidth = contentwidth
        self._contentheight = contentheight = contentheight

        # Defining scroll region.
        scrollregion = (0, 0, contentwidth, contentheight)

        # print(" ".join([item.__str__() for item in scrollregion]))
        print(scrollregion)

        # Configuring subwidgets.
        self._frame.configure(width=width, height=height)  # Default Frame
        self._frame2.configure(width=width-2, height=height)
        self._canvas.configure(width=width-2, height=height, scrollregion=" ".join([item.__str__() for item in scrollregion]))  # Canvas
        self._frameinner.configure(width=contentwidth, height=contentheight)  # Inner Frame
        self._canvas.itemconfig(self._c_window_id, width=contentwidth, height=contentheight)  # Canvas Window
        self._canvas.update()
        super(QScrollableFrame, self).configure(**kw)


class QCanvasList(_ttk.Widget):
    def __init__(self, master, rowheight=200, command: Callable[[_tk.Canvas, int], Any] = lambda c, i: None,
                 canvbg="#373737", canvbg_hover="#3f3f3f", canvbg_pressed="#272727"):
        """
        An list of canvases, what do you expect? Internally used in QBubbles for the slots-menu.

        :param master: The master widget, must be a container widget like a Frame.
        :param rowheight: The row height for each canvas, must be an integer.
        :param command: Command when clicking on a canvas.
        :param canvbg: The standard canvas background color.
        :param canvbg_hover: The hover canvas background color.
        :param canvbg_pressed: The pressed canvas background color.
        """

        kw = {"class": "QCanvasList",
              "style": "QCanvasList"}
        super(QCanvasList, self).__init__(master, "ttk::frame", kw)

        self._command = command

        self._rowHeight = rowheight
        self._canvasBG = canvbg
        self._canvasBGHover = canvbg_hover
        self._canvasBGPressed = canvbg_pressed

        self._canvass = []

        self.scrollable = QScrollableFrame(
            self, 400, 400, fillcontents=True, hscrollbar=False, scollbarbg="#2f2f2f", scrollbarfg="#3f3f3f")
        self.scrollable.pack(fill="both", expand=True)

    def append(self, **canvas_options) -> Tuple[_tk.Canvas, int]:
        """
        Adds a new canvas to the list of canvas'.

        :returns: The created canvas.
        """

        index = len(self._canvass)

        c = _tk.Canvas(self.scrollable, height=self._rowHeight, bg=self._canvasBG, **canvas_options)
        c.pack(fill="x")
        c.bind("<Enter>", self._on_canv_enter)
        c.bind("<Leave>", self._on_canv_leave)
        c.bind("<ButtonPress-1>", self._on_canv_press)
        c.bind("<ButtonRelease-1>", lambda evt: self._on_canv_release(evt, index))

        self.scrollable.configure(contentheight=(len(self._canvass)+1) * self._rowHeight)

        self._canvass.append(c)

        return c, index

    def canvasconfigure(self, canvas, **canvas_options):
        if canvas not in self._canvass:
            raise ValueError(f"Canvas not found")

        canvas.configure(**canvas_options)

    def itemconfigure(self, index: int, **canvas_options):
        if index >= len(self._canvass):
            raise IndexError("Canvas index out of range")
        elif index < 0:
            raise IndexError("Canvas index out of range")

        canvas = self._canvass[index]
        canvas.configure(**canvas_options)

    @overload
    def remove(self, canvas: _tk.Canvas):
        """
        Removes the canvas from the canvas' list.

        :param canvas: The Canvas to remove.
        :return:
        """

        if canvas not in self._canvass:
            raise ValueError(f"Canvas not found")

        canvas.pack_forget()
        canvas.destroy()

        self.scrollable.configure(contentheight=(len(self._canvass) - 1) * self._rowHeight)
        self._canvass.remove(canvas)

    @remove.add
    def remove(self, index: int):
        """
        Removes the canvas from the canvas' list.

        :param index: The index of the canvas to remove.
        :return:
        """

        if index >= len(self._canvass):
            raise IndexError("Canvas index out of range")
        elif index < 0:
            raise IndexError("Canvas index out of range")

        c: _tk.Canvas = self._canvass[index]
        c.pack_forget()
        c.destroy()

        self.scrollable.configure(contentheight=(len(self._canvass)) * self._rowHeight)
        del self._canvass[index]

    def _on_canv_enter(self, evt):
        """
        Internal event handler for entering the mouse cursor over a canvas.

        :param evt:
        :return:
        """

        c: _tk.Canvas = evt.widget
        c.configure(bg=self._canvasBGHover)

    def _on_canv_leave(self, evt):
        """
        Internal event handler for leaving the mouse cursor from a canvas.

        :param evt:
        :return:
        """

        c: _tk.Canvas = evt.widget
        c.configure(bg=self._canvasBG)

    def _on_canv_press(self, evt):
        """
        Internal event handler for pressing on a canvas.

        :param evt:
        :return:
        """

        c: _tk.Canvas = evt.widget
        c.configure(bg=self._canvasBGPressed)

    def _on_canv_release(self, evt, i):
        """
        Internal event handler for stop pressing on a canvas.

        :param evt:
        :return:
        """

        c: _tk.Canvas = evt.widget
        c.configure(bg=self._canvasBG)

        if c.winfo_rootx() < evt.x_root < (c.winfo_rootx() + c.winfo_width()):
            if c.winfo_rooty() < evt.y_root < (c.winfo_rooty() + c.winfo_height()):
                self._command(c, i)
