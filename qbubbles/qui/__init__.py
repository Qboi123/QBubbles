import tkinter as _tk
import tkinter.ttk as _ttk
import typing as _t

from overload import overload as _overload


# noinspection PyAttributeOutsideInit,PyUnusedLocal
class CustomVerticalScrollbar(_tk.Canvas):
    def __init__(self, parent, **kwargs):
        """
        Custom scrollbar, using canvas. It can be configured with fg, bg and command

        :param parent:
        :param kwargs:
        """

        self.command = kwargs.pop("command", None)
        kw = kwargs.copy()
        bd = 0
        hlt = 0
        if "fg" in kw.keys():
            del kw["fg"]
        if "bd" in kw.keys():
            bd = kw.pop("bd")
        if "border" in kw.keys():
            bd = kw.pop("border")
        if "highlightthickness" in kw.keys():
            hlt = kw.pop("highlightthickness")
        _tk.Canvas.__init__(self, parent, **kw, highlightthickness=hlt, border=bd, bd=bd)
        if "fg" not in kwargs.keys():
            kwargs["fg"] = "darkgray"

        # coordinates are irrelevant; they will be recomputed
        # in the 'set' method\
        self.old_y = 0
        self._id = self.create_rectangle(0, 0, 1, 1, fill=kwargs["fg"], outline=kwargs["fg"], tags=("thumb",))
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def configure(self, cnf=None, **kwargs):
        command = kwargs.pop("command", None)
        self.command = command if command is not None else self.command
        kw = kwargs.copy()
        if "fg" in kw.keys():
            del kw["fg"]
        super().configure(**kw, highlightthickness=0, border=0, bd=0)
        if "fg" not in kwargs.keys():
            kwargs["fg"] = "darkgray"
        self.itemconfig(self._id, fill=kwargs["fg"], outline=kwargs["fg"])

    def config(self, cnf=None, **kwargs):
        self.configure(cnf, **kwargs)

    def redraw(self, event):
        # The command is presumably the `yview` method of a widget.
        # When called without any arguments it will return fractions
        # which we can pass to the `set` command.
        self.set(*self.command())

    def set(self, first, last):
        first = float(first)
        last = float(last)
        height = self.winfo_height()
        x0 = int(self.cget("bd"))
        x1 = self.winfo_width() - int(self.cget("bd"))
        y0 = max(int(height * first), 0)
        y1 = min(int(height * last), height)
        self._x0 = x0
        self._x1 = x1
        self._y0 = y0
        self._y1 = y1

        self.coords("thumb", x0, y0, x1, y1)

    def on_press(self, event):
        self.bind("<Motion>", self.on_click)
        self.pressed_y = event.y
        self.on_click(event)

    def on_release(self, event):
        self.unbind("<Motion>")

    def on_click(self, event):
        y = event.y / self.winfo_height()
        y0 = self._y0
        y1 = self._y1
        a = y + ((y1 - y0) / -(self.winfo_height() * 2))
        self.command("moveto", a)


# noinspection PyAttributeOutsideInit,PyUnusedLocal
class CustomHorizontalScrollbar(_tk.Canvas):
    def __init__(self, parent, **kwargs):
        """
        Custom scrollbar, using canvas. It can be configured with fg, bg and command

        :param parent:
        :param kwargs:
        """

        self.command = kwargs.pop("command", None)
        kw = kwargs.copy()
        bd = 0
        hlt = 0
        if "fg" in kw.keys():
            del kw["fg"]
        if "bd" in kw.keys():
            bd = kw.pop("bd")
        if "border" in kw.keys():
            bd = kw.pop("border")
        if "highlightthickness" in kw.keys():
            hlt = kw.pop("highlightthickness")
        _tk.Canvas.__init__(self, parent, **kw, highlightthickness=hlt, border=bd, bd=bd)
        if "fg" not in kwargs.keys():
            kwargs["fg"] = "darkgray"

        # coordinates are irrelevant; they will be recomputed
        # in the 'set' method\
        self.old_y = 0
        self._id = self.create_rectangle(0, 0, 1, 1, fill=kwargs["fg"], outline=kwargs["fg"], tags=("thumb",))
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def configure(self, cnf=None, **kwargs):
        command = kwargs.pop("command", None)
        self.command = command if command is not None else self.command
        kw = kwargs.copy()
        if "fg" in kw.keys():
            del kw["fg"]
        super().configure(**kw, highlightthickness=0, border=0, bd=0)
        if "fg" not in kwargs.keys():
            kwargs["fg"] = "darkgray"
        self.itemconfig(self._id, fill=kwargs["fg"], outline=kwargs["fg"])

    def config(self, cnf=None, **kwargs):
        self.configure(cnf, **kwargs)

    def redraw(self, event):
        # The command is presumably the `yview` method of a widget.
        # When called without any arguments it will return fractions
        # which we can pass to the `set` command.
        self.set(*self.command())

    def set(self, first, last):
        first = float(first)
        last = float(last)
        width = self.winfo_width()
        y0 = 1
        y1 = self.winfo_width() - 1
        x0 = max(int(width * first), 0)
        x1 = min(int(width * last), width)
        self._x0 = x0
        self._x1 = x1
        self._y0 = y0
        self._y1 = y1

        self.coords("thumb", x0, y0, x1, y1)

    def on_press(self, event):
        self.bind("<Motion>", self.on_click)
        self.pressed_x = event.x
        self.on_click(event)

    def on_release(self, event):
        self.unbind("<Motion>")

    def on_click(self, event):
        x = event.x / self.winfo_width()
        x0 = self._x0
        x1 = self._x1
        a = x + ((x1 - x0) / -(self.winfo_width() * 2))
        self.command("moveto", a)


class QAccentButton(_ttk.Widget):
    def __init__(self, master, **kw):
        """
        Accent Button, an button with an accent color.

        :param master:
        :param kw:
        """

        kw['style'] = 'QAccentButton'
        kw['class'] = 'QAccentButton'

        command = kw.pop("command", lambda: None)

        def on_enter(evt):
            if evt.widget == self:
                state = list(self.state())
                # state.append("active")
                self.state(("active",))

        def on_leave(evt):
            # print("Leave")
            if evt.widget == self:
                state = list(self.state())
                # state.append("!active")
                self.state(("!active",))

        def on_press(evt):
            if evt.widget == self:
                state = list(self.state())
                # state.append("pressed")
                self.state(("pressed",))

        def on_release(evt):
            if evt.widget == self:
                state = list(self.state())
                # state.remove("pressed")
                # state.append("!pressed")
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

        :param master: Master of the scrolled frame.
                       Must be a QScrollableFrame, any type of Frame or any type of Labelframe
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
        self.master: _t.Union[_ttk.Frame, _tk.Frame, _tk.LabelFrame, _ttk.Labelframe, _tk.Tk, QScrollableFrame] = master
        self.scrollCommand: _t.Callable[[], _t.Any] = scrollcommand

        self._width = width
        self._height = height

        self._contentwidth = contentwidth = contentwidth if contentwidth is not None else width
        self._contentheight = contentheight = contentheight if contentheight is not None else height

        # Defining scroll region.
        scrollregion = (
            0, 0, contentwidth if contentwidth is not None else width,
            contentheight if contentheight is not None else height)

        self._frame = QScrollableFrameInner(self.master, width=width, height=height)
        self._frame.columnconfigure(0, weight=1)
        self._frame.rowconfigure(0, weight=1)

        self._frame2 = QScrollableFrameInner(self._frame, width=width, height=height)

        # Create the canvas.
        self._canvas = _tk.Canvas(
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
        self._scroll_gap = _tk.Canvas(self._frame, width=10, height=10, bg=scrollbarbg, highlightthickness=0)
        self._canvas.configure(yscrollcommand=self._vertical_scrollbar.set if vscrollbar else None,
                               xscrollcommand=self._horizontal_scrollbar.set if hscrollbar else None)

        self._fakecontent = _ttk.Frame(self._frame2, width=contentwidth, height=contentheight)
        self._frameinner = _ttk.Frame(self._frame2, width=contentwidth, height=contentheight)

        # Super(...) call.
        super(QScrollableFrame, self).__init__(self._frameinner, "ttk::frame", kw=super_kw)
        self._fakeinner = QScrollableFrameInner(self._fakecontent, width=contentwidth, height=contentheight)
        self._fakeinner.pack(fill="both", expand=True)
        self.fillcontents = fillcontents

        self.master: _t.Union[_ttk.Frame, _tk.Frame, _tk.LabelFrame, _ttk.Labelframe, _tk.Tk, QScrollableFrame] = master

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
        )  # scrollregion=scrollregion)

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

    @staticmethod
    def _bind_to_mousewheel(event):
        """
        Bind mousewheel event to the canvas

        :param event:
        :return:
        """

        print("Enter Canvas")
        # self._frame.bind_all("<MouseWheel>", self._on_mousewheel)

    @staticmethod
    def _unbind_to_mousewheel(event):
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
        self._frame2.configure(width=width - 2, height=height)
        self._canvas.configure(width=width - 2, height=height,
                               scrollregion=" ".join([item.__str__() for item in scrollregion]))  # Canvas
        self._frameinner.configure(width=contentwidth, height=contentheight)  # Inner Frame
        self._canvas.itemconfig(self._c_window_id, width=contentwidth, height=contentheight)  # Canvas Window
        self._canvas.update()
        super(QScrollableFrame, self).configure(**kw)


class QCanvasList(_ttk.Widget):
    def __init__(self, master, rowheight=200, command: _t.Callable[[_tk.Canvas, int], _t.Any] = lambda c, i: None,
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

    def append(self, **canvas_options) -> _t.Tuple[_tk.Canvas, int]:
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

        self.scrollable.configure(contentheight=(len(self._canvass) + 1) * self._rowHeight)

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

    @_overload
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


class QSpacing(_ttk.Frame):
    def __init__(self):
        pass


class QButton(_ttk.Widget):
    def __init__(self, master, text="", command=lambda: None):
        super(QButton, self).__init__(master, "ttk::button", {"class": "QButton", "style": "QButton", "text": text})

        def on_enter(evt):
            self.state(["active"])

        def on_leave(evt):
            self.state(["!active"])

        def on_press(evt):
            self.state(["pressed"])

        def on_release(evt):
            self.state(["!pressed"])
            master: QFrame
            print(dir(evt))
            if evt.widget.master.winfo_containing(evt.x_root, evt.y_root) == self:
                command()

        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)
        self.bind("<ButtonPress-1>", on_press)
        self.bind("<ButtonRelease-1>", on_release)


class QEntry(_ttk.Widget):
    def __init__(self, master):
        super(QEntry, self).__init__(master, "ttk::entry", {"class": "TEntry", "style": "QEntry"})


class QFrame(_ttk.Widget):
    def __init__(self, master):
        super(QFrame, self).__init__(master, "ttk::frame", {"class": "TFrame", "style": "QFrame"})


class QSeparator(_ttk.Widget):
    def __init__(self, master):
        super(QSeparator, self).__init__(master, "ttk::separator", {"class": "TSeparator", "style": "QSeparator"})


class QNotebook(_ttk.Notebook):
    def __init__(self, master, height=None, width=None):
        super(QNotebook, self).__init__(master, style="QNotebook", width=width, height=height)


class QLabel(_ttk.Widget):
    def __init__(self, master, text=""):
        kw = {}
        if text:
            kw["text"] = text

        super(QLabel, self).__init__(master, "ttk::label", {"class": "TLabel", "style": "QLabel", **kw})


class QCombobox(_ttk.Combobox):
    # noinspection PyMissingConstructor
    def __init__(self, master, values=None):
        kw = {}
        if values is not None:
            kw["values"] = values

        print(values)

        super(QCombobox, self).__init__(master, values=values)

    # def current(self, newindex=None):
    #     """If newindex is supplied, sets the combobox value to the
    #     element at position newindex in the list of values. Otherwise,
    #     returns the index of the current value in the list of values
    #     or -1 if the current value does not appear in the list."""
    #     if newindex is None:
    #         return self.tk.getint(self.tk.call(self._w, "current"))
    #     return self.tk.call(self._w, "current", newindex)
    #
    # def set(self, value):
    #     """Sets the value of the combobox to value."""
    #     self.tk.call(self._w, "set", value)


def init(widget=None):
    flat = "flat"

    s = _ttk.Style()
    s.theme_create("QUI", "default")
    s.theme_use("QUI")

    print(s.layout("ComboboxPopdownFrame"))
    print(s.layout("TSeparator"))
    print(s.map("TSeparator"))
    print(s.element_options("ComboboxPopdownFrame"))
    s.layout(
        "ComboboxPopdownFrame", [(
            'ComboboxPopdownFrame.highlight', {
                'border': 0,
                'sticky': 'nswe',
                'children': [(
                    'ComboboxPopdownFrame.border', {
                        'border': 0,
                        'sticky': 'nswe',
                        'children': [(
                            'ComboboxPopdownFrame.padding', {
                                'border': 0,
                                'sticky': 'nswe'
                            }
                        )]
                    }), (
                    'ComboboxPopdownFrame.bd', {
                        'sticky': 'nswe',
                        'border': 0,
                        'children': [(
                            'ComboboxPopdownFrame.padding', {
                                'border': 0,
                                'sticky': 'nswe'
                            }
                        )]
                    }
                )]
            }
        ), (
            'ComboboxPopdownFrame.border', {
                'border': 0,
                'sticky': 'nswe',
                'children': [(
                    'ComboboxPopdownFrame.padding', {
                        'border': 0,
                        'sticky': 'nswe'
                    }
                )]
            }), (
            'ComboboxPopdownFrame.bd', {
                'sticky': 'nswe',
                'border': 0,
                'children': [(
                    'ComboboxPopdownFrame.padding', {
                        'border': 0,
                        'sticky': 'nswe'
                    }
                )]
            }
        )]
        #     'Entry.highlight', {
        #         'border': 0,
        #         'sticky': 'nswe',
        #         "children": [(
        #             'ComboboxPopdownFrame.border', {
        #                 "border": 0,
        #                 'sticky': 'nswe'
        #             }
        #         )]
        #     }
        # )]
    )
    print(s.layout("ComboboxPopdownFrame"))
    # s.layout(
    #     "ComboboxPopdownFrame", [(
    #         'Entry.highlight', {
    #             'border': 0,
    #             'sticky': 'nswe',
    #             "children": [(
    #                 'ComboboxPopdownFrame.border', {
    #                     "border": 0,
    #                     'sticky': 'nswe'
    #                 }
    #             )]
    #         }
    #     )]
    # )
    s.layout("QFrame", s.layout("TFrame"))
    s.theme_settings(
        "QUI", {
            "QFrame": {
                "configure": {"background": "#5f5f5f", "relief": flat}
            }
        }
    )
    s.layout("QSeparator", [('Separator.separator', {"border": 1, 'sticky': 'nswe'})])
    s.theme_settings(
        "QUI", {
            "QSeparator": {
                "configure": {"background": "#6f6f6f", "relief": flat}
            }
        }
    )
    s.configure("QSeparator", relief='flat', borderwidth=1, bd=1, border=1)
    s.configure("Separator", relief='flat', borderwidth=1, bd=1, border=1)
    s.layout(
        "QEntry", [(
            'Entry.highlight', {
                'border': 0,
                'sticky': 'nswe',
                'children': [(
                    'Entry.border', {
                        'border': 0,
                        'sticky': 'nswe',
                        'children': [(
                            'Entry.padding', {
                                'sticky': 'nswe',
                                'children': [(
                                    'Entry.textarea', {
                                        'sticky': 'nswe',
                                        'border': 0}
                                )]
                            }
                        )]
                    }), (
                    'Entry.bd', {
                        'sticky': 'nswe',
                        'border': 0,
                        'children': [(
                            'Entry.padding', {
                                'sticky': 'nswe',
                                'children': [(
                                    'Entry.textarea', {
                                        'sticky': 'nswe'
                                    }
                                )]
                            }
                        )]
                    }
                )]
            }
        )]
    )
    s.theme_settings(
        "QUI", {
            "QEntry": {
                "configure": {"padding": 4},
                "map": {
                    "relief": [("active", flat),
                               ("focus", flat),
                               ("!disabled", flat),
                               ("disabled", flat)],
                    "background": [("active", "#00afaf"),
                                   ("focus", "#00afaf"),
                                   ("!disabled", "#6f6f6f"),
                                   ("disabled", "#8f8f8f")],
                    "bordercolor": [("active", "#00afaf"),
                                    ("focus", "#00afaf"),
                                    ("!disabled", "#6f6f6f"),
                                    ("disabled", "#5f5f5f")],
                    "foreground": [("active", "#ffffff"),
                                   ("focus", "#ffffff"),
                                   ("!disabled", "#afafaf"),
                                   ("disabled", "#5f5f5f")],
                    "selectbackground": [("active", "#00c7c7"),
                                         ("focus", "#00c7c7"),
                                         ("!disabled", "#7f7f7f"),
                                         ("disabled", "#9f9f9f")],
                    "selectforeground": [("active", "#ffffff"),
                                         ("focus", "#ffffff"),
                                         ("!disabled", "#bfbfbf"),
                                         ("disabled", "#6f6f6f")],
                }
            }
        }
    )
    s.layout("QButton", s.layout("TButton"))
    s.theme_settings(
        "QUI", {
            "QButton": {
                "configure": {"padding": 4},
                "map": {
                    "relief": [('pressed', flat),
                               ("active", flat),
                               ("focus", flat),
                               ("!disabled", flat),
                               ("disabled", flat)],
                    "background": [('pressed', '#005f5f'),
                                   ("active", "#00afaf"),
                                   ("focus", "#6f6f6f"),
                                   ("!disabled", "#6f6f6f"),
                                   ("disabled", "#8f8f8f")],
                    "bordercolor": [('pressed', '#005f5f'),
                                    ("active", "#00afaf"),
                                    ("focus", "#00afaf"),
                                    ("!disabled", "#6f6f6f"),
                                    ("disabled", "#5f5f5f")],
                    "foreground": [('pressed', '#ffffff'),
                                   ("active", "#ffffff"),
                                   ("focus", "#ffffff"),
                                   ("!disabled", "#afafaf"),
                                   ("disabled", "#5f5f5f")],
                }
            }
        }
    )
    s.layout(
        "QAccentButton", s.layout("TButton")
    )
    s.theme_settings(
        "QUI", {
            "QAccentButton": {
                "configure": {"padding": 4},
                "map": {
                    "relief": [('pressed', flat),
                               ("active", flat),
                               ("focus", flat),
                               ("!disabled", flat),
                               ("disabled", flat)],
                    "background": [('pressed', '#005f5f'),
                                   ("active", "#00afaf"),
                                   ("focus", "#00afaf"),
                                   ("!disabled", "#007f7f"),
                                   ("disabled", "#8f8f8f")],
                    "bordercolor": [('pressed', '#005f5f'),
                                    ("active", "#00afaf"),
                                    ("focus", "#00afaf"),
                                    ("!disabled", "#007f7f"),
                                    ("disabled", "#5f5f5f")],
                    "foreground": [('pressed', '#ffffff'),
                                   ("active", "#ffffff"),
                                   ("focus", "#ffffff"),
                                   ("!disabled", "#ffffff"),
                                   ("disabled", "#5f5f5f")],
                }
            }
        }
    )
    # s.theme_settings(
    #     "QUI", {
    #         "QAccentButton": {
    #             'configure': {
    #                 'font':
    #                     ['Helvetica', 10],
    #                 'padding': 4
    #             },
    #             'map': {
    #                 'relief': [('pressed', 'flat'),
    #                            ('active', 'flat'),
    #                            ('focus', 'flat'),
    #                            ('disabled', 'flat'),
    #                            ('!disabled', 'flat')],
    #                 'background': [('pressed', '#005f5f'),
    #                                ('active', '#009f9f'),
    #                                ('focus', '#009f9f'),
    #                                ('disabled', '#7f7f7f'),
    #                                ('!disabled', '#007f7f')],
    #                 'bordercolor': [('pressed', '#005f5f'),
    #                                 ('active', '#009f9f'),
    #                                 ('focus', '#009f9f'),
    #                                 ('disabled', '#7f7f7f'),
    #                                 ('!disabled', '#007f7f')],
    #                 'foreground': [('pressed', 'white'),
    #                                ('active', 'white'),
    #                                ('focus', 'white'),
    #                                ('disabled', '#7f7f7f'),
    #                                ('!disabled', 'white')]
    #             }
    #         }
    #     }
    # )
    s.layout("QScrollableFrame", s.layout("TFrame"))
    s.theme_settings(
        "QUI", {
            "QScrollableFrame": {
                "configure": {
                    "relief": flat,
                    "background": "#2f2f2f"
                }
            }
        }
    )
    s.layout("QScrollableFrame.Inner", s.layout("TFrame"))
    s.theme_settings(
        "QUI", {
            "QScrollableFrame.Inner": {
                "configure": {
                    "relief": flat,
                    "background": "#2f2f2f"
                }
            }
        }
    )
    s.layout("QCanvasList", s.layout("TFrame"))
    s.theme_settings(
        "QUI", {
            "QCanvasList": {
                "configure": {
                    "relief": flat,
                    "background": "#2f2f2f"
                }
            }
        }
    )
    s.layout("QLabel", s.layout("TLabel"))
    s.theme_settings(
        "QUI", {
            "QLabel": {
                'configure': {
                    'font': ['Helvetica', 10],
                    'background': '#5f5f5f',
                    'foreground': '#dfdfdf'
                }
            }
        }
    )
    s.layout("TCombobox", s.layout("TCombobox"))
    # s.layout(
    #     'TCombobox', [(
    #         'Entry.highlight', {
    #             'border': 0,
    #             'sticky': 'nswe',
    #             'children': [(
    #                 'Entry.border', {
    #                     'border': 0,
    #                     'sticky': 'nswe',
    #                     'children': [(
    #                         'Combobox.rightdownarrow', {
    #                             # "border": 0,
    #                             'side': 'right',
    #                             'sticky': 'ns'
    #                         }), (
    #                         'Entry.padding', {
    #                             'sticky': 'nswe',
    #                             'children': [(
    #                                 'Entry.textarea', {
    #                                     'sticky': 'nswe',
    #                                     'border': 0}
    #                             )]
    #                         }
    #                     )]
    #                 }), (
    #                 'Entry.bd', {
    #                     'sticky': 'nswe',
    #                     'border': 0,
    #                     'children': [(
    #                         'Entry.padding', {
    #                             'sticky': 'nswe',
    #                             'children': [(
    #                                 'Entry.textarea', {
    #                                     'sticky': 'nswe'
    #                                 }
    #                             )]
    #                         }
    #                     )]
    #                 }
    #             )]
    #         }
    #     )]
    #     'Combobox.border', {
    #         "border": 0,
    #         'sticky': 'nswe',
    #         'children': [(
    #             'Combobox.rightdownarrow', {
    #                 "border": 0,
    #                 'side': 'right',
    #                 'sticky': 'ns'
    #             }), (
    #             'Combobox.padding', {
    #                 'expand': '1',
    #                 "border": 0,
    #                 'sticky': 'nswe',
    #                 'children': [(
    #                     'Combobox.background', {
    #                         'sticky': 'nswe',
    #                         "border": 0,
    #                         'children': [(
    #                             'Combobox.focus', {
    #                                 'expand': '1',
    #                                 "border": 0,
    #                                 'sticky': 'nswe',
    #                                 'children': [(
    #                                     'Combobox.textarea', {
    #                                         "border": 0,
    #                                         'sticky': 'nswe'
    #                                     }
    #                                 )]
    #                             }
    #                         )]
    #                     }
    #                 )]
    #             }
    #         )]
    #     }
    # )]
    # )
    s.theme_settings(
        "QUI", {
            "TCombobox": {
                'configure': {
                    'padding': 4,
                    'arrowsize': 15,
                    'postoffset': 0,
                    "focusfill": '#7f7f7f',
                    "relief": flat
                },
                'map': {
                    'arrowcolor': [('pressed', 'white'),
                                   ('active', 'white'),
                                   ('focus', 'white'),
                                   ('disabled', '#7f7f7f'),
                                   ('!disabled', 'white')],
                    'bordercolor': [('active', '#007f7f'),
                                    ('focus', '#007f7f'),
                                    ('disabled', '#007f7f'),
                                    ('!disabled', '#007f7f')],
                    'background': [('pressed', '#009f9f'),
                                   ('active', '#007f7f'),
                                   ('focus', '#007f7f'),
                                   ('disabled', '#7f7f7f'),
                                   ('!disabled', '#676767')],
                    'fieldbackground': [('pressed', '#007f7f'),
                                        ('active', '#005f5f'),
                                        ('focus', '#005f5f'),
                                        ('disabled', '#6f6f6f'),
                                        ('!disabled', '#4f4f4f')],
                    'foreground': [('active', 'white'),
                                   ('focus', 'white'),
                                   ('disabled', '#afafaf'),
                                   ('!disabled', 'white')],
                    'selectbackground': [('active', '#009f9f'),
                                         ('focus', '#009f9f'),
                                         ('disabled', '#7f7f7f'),
                                         ('!disabled', '#007f7f')]
                }
            }
        }
    )
    s.layout("QNotebook", s.layout("TNotebook"))
    s.configure("QNotebook", relief='flat', borderwidth=0, bd=0, border=0)
    s.configure("QNotebook.Tab", relief='flat', borderwidth=0, bd=0, border=0)
    s.theme_settings(
        "QUI", {
            "QNotebook": {
                "configure": {
                    "padding": 4,
                    "tabmargins": 0,
                    "tabposition": "top",
                },
                "map": {
                    "background": [("focus", "#676767"),
                                   ("active", "#00afaf"),
                                   ("disabled", "#9f9f9f"),
                                   ("!disabled", "#676767")],
                    "lightcolor": [("focus", "#00afaf"),
                                   ("active", "#00afaf"),
                                   ("disabled", "#005f5f"),
                                   ("!disabled", "#00afaf")],
                    "darkcolor": [("focus", "#00afaf"),
                                  ("active", "#00afaf"),
                                  ("disabled", "#005f5f"),
                                  ("!disabled", "#00afaf")],
                    "bordercolor": [("focus", "#00afaf"),
                                    ("active", "#00afaf"),
                                    ("disabled", "#005f5f"),
                                    ("!disabled", "#00afaf")],
                    "foreground": [("focus", "#afafaf"),
                                   ("active", "#00afaf"),
                                   ("disabled", "#5f5f5f"),
                                   ("!disabled", "#afafaf")]
                }
            }
        }
    )
    s.theme_settings(
        "QUI", {
            "QNotebook.Tab": {
                "configure": {
                    "padding": 4
                },
                "map": {
                    "background": [("focus", "#7f7f7f"),
                                   ("active", "#00afaf"),
                                   ("disabled", "#9f9f9f"),
                                   ("!disabled", "#6f6f6f")],
                    "bordercolor": [("focus", "#00afaf"),
                                    ("active", "#00ffff"),
                                    ("disabled", "#005f5f"),
                                    ("!disabled", "#00afaf")],
                    "foreground": [("focus", "#afafaf"),
                                   ("active", "#ffffff"),
                                   ("disabled", "#5f5f5f"),
                                   ("!disabled", "#bfbfbf")]
                }
            }
        }
    )

    s.configure('TCombobox', relief='flat', bd=0, borderwidth=0)
    # s.layout("QProgressbar", s.layout("TProgressbar"))
    s.theme_settings(
        "QUI", {
            "QProgressbar": {
                'configure': {
                    'background': '#007f7f',
                    'bordercolor': '#007f7f',
                    'troughcolor': '#4f4f4f'
                }
            }
        }
    )
    s.theme_settings(
        "QUI", {
            "QProgressbar": {
                'configure': {
                    'background': '#007f7f',
                    'bordercolor': '#007f7f',
                    'troughcolor': '#4f4f4f'
                }
            }
        }
    )
    s.theme_settings(
        "QUI", {
            "TComboboxPopdownFrame": {
                'configure': {'relief': 'flat', 'borderwidth': 0, "highlightthickness": 0, "padding": 0}}
        }
    )
    s.configure("ComboboxPopdownFrame", relief='flat', borderwidth=0, bd=0, border=0)
    s.configure("ComboboxPopdownWindow", relief='flat', borderwidth=0, bd=0, border=0)
    if widget is not None:
        widget.option_add('*TCombobox*Listbox*background', '#3f3f3f')
        widget.option_add('*TCombobox*Listbox*foreground', 'white')
        widget.option_add('*TCombobox*Listbox*selectBackground', '#007f7f')
        widget.option_add('*TCombobox*Listbox*selectForeground', 'white')
        widget.option_add('*TCombobox*Listbox*relief', 'flat')
        widget.option_add('*TCombobox*Listbox*borderWidth', '0')
        widget.option_add('*TCombobox*Listbox*bd', '0')
        widget.option_add('*TCombobox*Listbox*highlightThickness', '0')
        widget.option_add('*TCombobox*PopdownWindow*relief', 'flat')
        widget.option_add('*TCombobox*PopdownWindow*borderWidth', '0')
        widget.option_add('*TCombobox*PopdownWindow*bd', '0')
        widget.option_add('*TCombobox*PopdownWindow*highlightThickness', '0')
        widget.option_add('*TCombobox*PopdownWindow*highLightThickness', '0')
        widget.option_add('*TCombobox*Listbox*font', ['helvetica', 10])

        widget.option_add('*QCombobox*Listbox*background', '#3f3f3f')
        widget.option_add('*QCombobox*Listbox*foreground', 'white')
        widget.option_add('*QCombobox*Listbox*selectBackground', '#007f7f')
        widget.option_add('*QCombobox*Listbox*selectForeground', 'white')
        widget.option_add('*QCombobox*Listbox*font', ['helvetica', 10])
    print(s.layout("ComboboxPopdownFrame"))
    print(s.layout("TSeparator"))
    print(s.map("TSeparator"))
    print(s.element_options("ComboboxPopdownFrame"))
    s.layout(
        "ComboboxPopdownFrame", [(
            'ComboboxPopdownFrame.highlight', {
                'border': 0,
                'sticky': 'nswe',
                'children': [(
                    'ComboboxPopdownFrame.border', {
                        'border': 0,
                        'sticky': 'nswe',
                        'children': [(
                            'ComboboxPopdownFrame.padding', {
                                'border': 0,
                                'sticky': 'nswe'
                            }
                        )]
                    }), (
                    'ComboboxPopdownFrame.bd', {
                        'sticky': 'nswe',
                        'border': 0,
                        'children': [(
                            'ComboboxPopdownFrame.padding', {
                                'border': 0,
                                'sticky': 'nswe'
                            }
                        )]
                    }
                )]
            }
        ), (
            'ComboboxPopdownFrame.border', {
                'border': 0,
                'sticky': 'nswe',
                'children': [(
                    'ComboboxPopdownFrame.padding', {
                        'border': 0,
                        'sticky': 'nswe'
                    }
                )]
            }), (
            'ComboboxPopdownFrame.bd', {
                'sticky': 'nswe',
                'border': 0,
                'children': [(
                    'ComboboxPopdownFrame.padding', {
                        'border': 0,
                        'sticky': 'nswe'
                    }
                )]
            }
        )]
        #     'Entry.highlight', {
        #         'border': 0,
        #         'sticky': 'nswe',
        #         "children": [(
        #             'ComboboxPopdownFrame.border', {
        #                 "border": 0,
        #                 'sticky': 'nswe'
        #             }
        #         )]
        #     }
        # )]
    )
    print(s.layout("ComboboxPopdownFrame"))
    # s.layout(
    #     "ComboboxPopdownFrame", [(
    #         'Entry.highlight', {
    #             'border': 0,
    #             'sticky': 'nswe',
    #             "children": [(
    #                 'ComboboxPopdownFrame.border', {
    #                     "border": 0,
    #                     'sticky': 'nswe'
    #                 }
    #             )]
    #         }
    #     )]
    # )
    s.layout("TFrame", s.layout("TFrame"))
    s.theme_settings(
        "QUI", {
            "TFrame": {
                "configure": {"background": "#5f5f5f", "relief": flat}
            }
        }
    )
    s.layout("TSeparator", [('Separator.separator', {"border": 1, 'sticky': 'nswe'})])
    s.theme_settings(
        "QUI", {
            "TSeparator": {
                "configure": {"background": "#6f6f6f", "relief": flat}
            }
        }
    )
    s.configure("TSeparator", relief='flat', borderwidth=1, bd=1, border=1)
    s.configure("Separator", relief='flat', borderwidth=1, bd=1, border=1)
    s.layout(
        "TEntry", [(
            'Entry.highlight', {
                'border': 0,
                'sticky': 'nswe',
                'children': [(
                    'Entry.border', {
                        'border': 0,
                        'sticky': 'nswe',
                        'children': [(
                            'Entry.padding', {
                                'sticky': 'nswe',
                                'children': [(
                                    'Entry.textarea', {
                                        'sticky': 'nswe',
                                        'border': 0}
                                )]
                            }
                        )]
                    }), (
                    'Entry.bd', {
                        'sticky': 'nswe',
                        'border': 0,
                        'children': [(
                            'Entry.padding', {
                                'sticky': 'nswe',
                                'children': [(
                                    'Entry.textarea', {
                                        'sticky': 'nswe'
                                    }
                                )]
                            }
                        )]
                    }
                )]
            }
        )]
    )
    s.theme_settings(
        "QUI", {
            "TEntry": {
                "configure": {"padding": 4},
                "map": {
                    "relief": [("active", flat),
                               ("focus", flat),
                               ("!disabled", flat),
                               ("disabled", flat)],
                    "background": [("active", "#00afaf"),
                                   ("focus", "#00afaf"),
                                   ("!disabled", "#6f6f6f"),
                                   ("disabled", "#8f8f8f")],
                    "bordercolor": [("active", "#00afaf"),
                                    ("focus", "#00afaf"),
                                    ("!disabled", "#6f6f6f"),
                                    ("disabled", "#5f5f5f")],
                    "foreground": [("active", "#ffffff"),
                                   ("focus", "#ffffff"),
                                   ("!disabled", "#afafaf"),
                                   ("disabled", "#5f5f5f")],
                    "selectbackground": [("active", "#00c7c7"),
                                         ("focus", "#00c7c7"),
                                         ("!disabled", "#7f7f7f"),
                                         ("disabled", "#9f9f9f")],
                    "selectforeground": [("active", "#ffffff"),
                                         ("focus", "#ffffff"),
                                         ("!disabled", "#bfbfbf"),
                                         ("disabled", "#6f6f6f")],
                }
            }
        }
    )
    s.layout("TButton", s.layout("TButton"))
    s.theme_settings(
        "QUI", {
            "TButton": {
                "configure": {"padding": 4},
                "map": {
                    "relief": [('pressed', flat),
                               ("active", flat),
                               ("focus", flat),
                               ("!disabled", flat),
                               ("disabled", flat)],
                    "background": [('pressed', '#005f5f'),
                                   ("active", "#00afaf"),
                                   ("focus", "#6f6f6f"),
                                   ("!disabled", "#6f6f6f"),
                                   ("disabled", "#8f8f8f")],
                    "bordercolor": [('pressed', '#005f5f'),
                                    ("active", "#00afaf"),
                                    ("focus", "#00afaf"),
                                    ("!disabled", "#6f6f6f"),
                                    ("disabled", "#5f5f5f")],
                    "foreground": [('pressed', '#ffffff'),
                                   ("active", "#ffffff"),
                                   ("focus", "#ffffff"),
                                   ("!disabled", "#afafaf"),
                                   ("disabled", "#5f5f5f")],
                }
            }
        }
    )
    s.layout(
        "TAccentButton", s.layout("TButton")
    )
    s.theme_settings(
        "QUI", {
            "TAccentButton": {
                "configure": {"padding": 4},
                "map": {
                    "relief": [('pressed', flat),
                               ("active", flat),
                               ("focus", flat),
                               ("!disabled", flat),
                               ("disabled", flat)],
                    "background": [('pressed', '#005f5f'),
                                   ("active", "#00afaf"),
                                   ("focus", "#00afaf"),
                                   ("!disabled", "#007f7f"),
                                   ("disabled", "#8f8f8f")],
                    "bordercolor": [('pressed', '#005f5f'),
                                    ("active", "#00afaf"),
                                    ("focus", "#00afaf"),
                                    ("!disabled", "#007f7f"),
                                    ("disabled", "#5f5f5f")],
                    "foreground": [('pressed', '#ffffff'),
                                   ("active", "#ffffff"),
                                   ("focus", "#ffffff"),
                                   ("!disabled", "#ffffff"),
                                   ("disabled", "#5f5f5f")],
                }
            }
        }
    )
    # s.theme_settings(
    #     "QUI", {
    #         "TAccentButton": {
    #             'configure': {
    #                 'font':
    #                     ['Helvetica', 10],
    #                 'padding': 4
    #             },
    #             'map': {
    #                 'relief': [('pressed', 'flat'),
    #                            ('active', 'flat'),
    #                            ('focus', 'flat'),
    #                            ('disabled', 'flat'),
    #                            ('!disabled', 'flat')],
    #                 'background': [('pressed', '#005f5f'),
    #                                ('active', '#009f9f'),
    #                                ('focus', '#009f9f'),
    #                                ('disabled', '#7f7f7f'),
    #                                ('!disabled', '#007f7f')],
    #                 'bordercolor': [('pressed', '#005f5f'),
    #                                 ('active', '#009f9f'),
    #                                 ('focus', '#009f9f'),
    #                                 ('disabled', '#7f7f7f'),
    #                                 ('!disabled', '#007f7f')],
    #                 'foreground': [('pressed', 'white'),
    #                                ('active', 'white'),
    #                                ('focus', 'white'),
    #                                ('disabled', '#7f7f7f'),
    #                                ('!disabled', 'white')]
    #             }
    #         }
    #     }
    # )
    s.layout("TScrollableFrame", s.layout("TFrame"))
    s.theme_settings(
        "QUI", {
            "TScrollableFrame": {
                "configure": {
                    "relief": flat,
                    "background": "#2f2f2f"
                }
            }
        }
    )
    s.layout("TScrollableFrame.Inner", s.layout("TFrame"))
    s.theme_settings(
        "QUI", {
            "TScrollableFrame.Inner": {
                "configure": {
                    "relief": flat,
                    "background": "#2f2f2f"
                }
            }
        }
    )
    s.layout("TCanvasList", s.layout("TFrame"))
    s.theme_settings(
        "QUI", {
            "TCanvasList": {
                "configure": {
                    "relief": flat,
                    "background": "#2f2f2f"
                }
            }
        }
    )
    s.layout("TLabel", s.layout("TLabel"))
    s.theme_settings(
        "QUI", {
            "TLabel": {
                'configure': {
                    'font': ['Helvetica', 10],
                    'background': '#5f5f5f',
                    'foreground': '#dfdfdf'
                }
            }
        }
    )
    s.layout("TCombobox", s.layout("TCombobox"))
    # s.layout(
    #     'TCombobox', [(
    #         'Entry.highlight', {
    #             'border': 0,
    #             'sticky': 'nswe',
    #             'children': [(
    #                 'Entry.border', {
    #                     'border': 0,
    #                     'sticky': 'nswe',
    #                     'children': [(
    #                         'Combobox.rightdownarrow', {
    #                             # "border": 0,
    #                             'side': 'right',
    #                             'sticky': 'ns'
    #                         }), (
    #                         'Entry.padding', {
    #                             'sticky': 'nswe',
    #                             'children': [(
    #                                 'Entry.textarea', {
    #                                     'sticky': 'nswe',
    #                                     'border': 0}
    #                             )]
    #                         }
    #                     )]
    #                 }), (
    #                 'Entry.bd', {
    #                     'sticky': 'nswe',
    #                     'border': 0,
    #                     'children': [(
    #                         'Entry.padding', {
    #                             'sticky': 'nswe',
    #                             'children': [(
    #                                 'Entry.textarea', {
    #                                     'sticky': 'nswe'
    #                                 }
    #                             )]
    #                         }
    #                     )]
    #                 }
    #             )]
    #         }
    #     )]
    #     'Combobox.border', {
    #         "border": 0,
    #         'sticky': 'nswe',
    #         'children': [(
    #             'Combobox.rightdownarrow', {
    #                 "border": 0,
    #                 'side': 'right',
    #                 'sticky': 'ns'
    #             }), (
    #             'Combobox.padding', {
    #                 'expand': '1',
    #                 "border": 0,
    #                 'sticky': 'nswe',
    #                 'children': [(
    #                     'Combobox.background', {
    #                         'sticky': 'nswe',
    #                         "border": 0,
    #                         'children': [(
    #                             'Combobox.focus', {
    #                                 'expand': '1',
    #                                 "border": 0,
    #                                 'sticky': 'nswe',
    #                                 'children': [(
    #                                     'Combobox.textarea', {
    #                                         "border": 0,
    #                                         'sticky': 'nswe'
    #                                     }
    #                                 )]
    #                             }
    #                         )]
    #                     }
    #                 )]
    #             }
    #         )]
    #     }
    # )]
    # )
    s.theme_settings(
        "QUI", {
            "TCombobox": {
                'configure': {
                    'padding': 4,
                    'arrowsize': 15,
                    'postoffset': 0,
                    "focusfill": '#7f7f7f',
                    "relief": flat
                },
                'map': {
                    'arrowcolor': [('pressed', 'white'),
                                   ('active', 'white'),
                                   ('focus', 'white'),
                                   ('disabled', '#7f7f7f'),
                                   ('!disabled', 'white')],
                    'bordercolor': [('active', '#007f7f'),
                                    ('focus', '#007f7f'),
                                    ('disabled', '#007f7f'),
                                    ('!disabled', '#007f7f')],
                    'background': [('pressed', '#009f9f'),
                                   ('active', '#007f7f'),
                                   ('focus', '#007f7f'),
                                   ('disabled', '#7f7f7f'),
                                   ('!disabled', '#676767')],
                    'fieldbackground': [('pressed', '#007f7f'),
                                        ('active', '#005f5f'),
                                        ('focus', '#005f5f'),
                                        ('disabled', '#6f6f6f'),
                                        ('!disabled', '#4f4f4f')],
                    'foreground': [('active', 'white'),
                                   ('focus', 'white'),
                                   ('disabled', '#afafaf'),
                                   ('!disabled', 'white')],
                    'selectbackground': [('active', '#009f9f'),
                                         ('focus', '#009f9f'),
                                         ('disabled', '#7f7f7f'),
                                         ('!disabled', '#007f7f')]
                }
            }
        }
    )
    s.layout("TNotebook", s.layout("TNotebook"))
    s.configure("TNotebook", relief='flat', borderwidth=0, bd=0, border=0)
    s.configure("TNotebook.Tab", relief='flat', borderwidth=0, bd=0, border=0)
    s.theme_settings(
        "QUI", {
            "TNotebook": {
                "configure": {
                    "padding": 4,
                    "tabmargins": 0,
                    "tabposition": "top",
                },
                "map": {
                    "background": [("focus", "#676767"),
                                   ("active", "#00afaf"),
                                   ("disabled", "#9f9f9f"),
                                   ("!disabled", "#676767")],
                    "lightcolor": [("focus", "#00afaf"),
                                   ("active", "#00afaf"),
                                   ("disabled", "#005f5f"),
                                   ("!disabled", "#00afaf")],
                    "darkcolor": [("focus", "#00afaf"),
                                  ("active", "#00afaf"),
                                  ("disabled", "#005f5f"),
                                  ("!disabled", "#00afaf")],
                    "bordercolor": [("focus", "#00afaf"),
                                    ("active", "#00afaf"),
                                    ("disabled", "#005f5f"),
                                    ("!disabled", "#00afaf")],
                    "foreground": [("focus", "#afafaf"),
                                   ("active", "#00afaf"),
                                   ("disabled", "#5f5f5f"),
                                   ("!disabled", "#afafaf")]
                }
            }
        }
    )
    s.theme_settings(
        "QUI", {
            "TNotebook.Tab": {
                "configure": {
                    "padding": 4
                },
                "map": {
                    "background": [("focus", "#7f7f7f"),
                                   ("active", "#00afaf"),
                                   ("disabled", "#9f9f9f"),
                                   ("!disabled", "#6f6f6f")],
                    "bordercolor": [("focus", "#00afaf"),
                                    ("active", "#00ffff"),
                                    ("disabled", "#005f5f"),
                                    ("!disabled", "#00afaf")],
                    "foreground": [("focus", "#afafaf"),
                                   ("active", "#ffffff"),
                                   ("disabled", "#5f5f5f"),
                                   ("!disabled", "#bfbfbf")]
                }
            }
        }
    )

    s.configure('TCombobox', relief='flat', bd=0, borderwidth=0)
    # s.layout("TProgressbar", s.layout("TProgressbar"))
    s.theme_settings(
        "QUI", {
            "TProgressbar": {
                'configure': {
                    'background': '#007f7f',
                    'bordercolor': '#007f7f',
                    'troughcolor': '#4f4f4f'
                }
            }
        }
    )
    s.configure(
        'TProgressbar', troughrelief='flat', borderwidth=0, thickness=16
    )
    s.theme_settings(
        "QUI", {
            "TComboboxPopdownFrame": {
                'configure': {'relief': 'flat', 'borderwidth': 0, "highlightthickness": 0, "padding": 0}}
        }
    )
    s.configure("ComboboxPopdownFrame", relief='flat', borderwidth=0, bd=0, border=0)
    s.configure("ComboboxPopdownWindow", relief='flat', borderwidth=0, bd=0, border=0)


if __name__ == '__main__':
    root = _tk.Tk()
    root.wm_minsize(200, 150)
    init(root)

    frame = QFrame(root)
    button = QButton(frame, text="QButton", command=lambda: print("Hoi"))
    button.pack(pady=1, padx=2, fill="x")
    button = QAccentButton(frame, text="QAccentButton")
    button.pack(pady=1, padx=2, fill="x")
    button = QLabel(frame, text="QAccentButton")
    button.pack(pady=1, padx=2, fill="x")
    button = QEntry(frame)
    button.pack(pady=1, padx=2, fill="x")
    button = QSeparator(frame)
    button.pack(pady=1, padx=0, fill="x")
    button = QNotebook(frame, height=200)
    button.add(QFrame(frame), text="Tab 1")
    button.pack(pady=1, padx=2, fill="x")
    button = QCombobox(frame, values=["Value 1", "Value 2"])
    button.pack(pady=1, padx=2, fill="x")
    button.set("Hallo")
    frame.pack(fill="both", expand=True)

    root.mainloop()
