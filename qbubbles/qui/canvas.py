import tkinter as _tk
import typing as _t

import PIL as _PIL
from overload import overload as _overload


class CRectangle(object):
    def __init__(self, canvas: _tk.Canvas, x1, y1, x2, y2, *, fill="", outline="", tags=tuple()):
        self._id = canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline, tags=tags)  # , anchor=anchor)
        self._canvas = canvas
        # print("CRectangle created")

    def delete(self):
        self._canvas.delete(self._id)

    def get_id(self):
        return self._id

    def move(self, x=None, y=None):
        return self._canvas.move(self._id, x, y)

    def coords(self, x1, y1, x2, y2) -> _t.Optional[_t.Tuple[float, float, float, float]]:
        return self._canvas.coords(self._id, x1, y1, x2, y2)

    def bind(self, sequence=None, func=None, add=None) -> _t.Union[str, int]:
        return self._canvas.tag_bind(self._id, sequence, func, add)

    def unbind(self, sequence, funcid=None):
        return self._canvas.tag_unbind(self._id, sequence, funcid)

    def configure(self, fill=None, outline=None, anchor=None, tags=None):
        return self._canvas.itemconfigure(self._id, fill=fill, outline=outline, anchor=anchor, tags=tags)

    def cget(self, option) -> _t.Union[str, int, float, bool, list, dict, _t.Callable]:
        return self._canvas.itemcget(self._id, option)

    def lower(self, *args):
        return self._canvas.tag_lower(self._id, *args)

    def raise_(self, *args):
        return self._canvas.tag_raise(self._id, *args)

    config = configure


class CImage(object):
    def __init__(self, canvas: _tk.Canvas, x, y, *, image, anchor="center", tags=tuple()):
        # noinspection PyProtectedMember
        self.root = canvas._root()
        self._id = canvas.create_image(x, y, image=image, anchor=anchor, tags=tags)  # , anchor=anchor)
        self._canvas: _tk.Canvas = canvas
        self._image: _t.Union[_PIL.ImageTk.PhotoImage, _tk.PhotoImage] = image
        self._anchor = anchor
        self._tags = tags

    def get_id(self):
        return self._id

    def delete(self):
        self._canvas.delete(self._id)

    def move(self, x=None, y=None):
        return self._canvas.move(self._id, x, y)

    @_overload
    def coords(self, x1, y1) -> None:
        self._canvas.coords(self._id, x1, y1)

    @coords.add
    def coords(self) -> _t.Optional[_t.Tuple[float, float]]:
        return self._canvas.coords(self._id)

    def bind(self, sequence=None, func=None, add=None) -> _t.Union[str, int]:
        return self._canvas.tag_bind(self._id, sequence, func, add)

    def unbind(self, sequence, funcid=None):
        return self._canvas.tag_unbind(self._id, sequence, funcid)

    def configure(self, *, image=None, anchor=None, tags=None):
        if image is None:
            image = self._image
        if anchor is None:
            anchor = self._anchor
        if tags is None:
            tags = self._tags
        return self._canvas.itemconfigure(self._id, image=image, anchor=anchor, tags=tags)

    def cget(self, option) -> _t.Union[str, int, float, bool, list, dict, _t.Callable]:
        return self._canvas.itemcget(self._id, option)

    def lower(self, *args):
        return self._canvas.tag_lower(self._id, *args)

    def raise_(self, *args):
        return self._canvas.tag_raise(self._id, *args)

    config = configure


class CText(object):
    def __init__(self, canvas: _tk.Canvas, x, y, *, text, anchor="center", fill="", tags=tuple(),
                 font=("Helvetica", 10)):
        # noinspection PyProtectedMember
        self.root = canvas._root()
        self._id = canvas.create_text(x, y, text=text, anchor=anchor, tags=tags, fill=fill, font=font)
        self._canvas: _tk.Canvas = canvas
        self._text: str = text
        self._anchor = anchor
        self._tags = tags
        self._fill = fill
        self._font = font

    def delete(self):
        self._canvas.delete(self._id)

    def get_id(self):
        return self._id

    def move(self, x=None, y=None):
        return self._canvas.move(self._id, x, y)

    @_overload
    def coords(self, x1, y1) -> None:
        self._canvas.coords(self._id, x1, y1)

    @coords.add
    def coords(self) -> _t.Optional[_t.Tuple[float, float]]:
        return self._canvas.coords(self._id)

    def bind(self, sequence=None, func=None, add=None) -> _t.Union[str, int]:
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

    def cget(self, option) -> _t.Union[str, int, float, bool, list, dict, _t.Callable]:
        return self._canvas.itemcget(self._id, option)

    def lower(self, *args):
        return self._canvas.tag_lower(self._id, *args)

    def raise_(self, *args):
        return self._canvas.tag_raise(self._id, *args)

    config = configure


class CPanel(CRectangle):
    def __init__(self, canvas: _tk.Canvas, x, y, width, height, fill="", outline=""):
        # noinspection PyProtectedMember
        self.root = canvas._root()
        self._width = width
        self._height = height
        if width == "extend":
            width = canvas.winfo_width()
        if height == "expand":
            height = canvas.winfo_height()
        self.x = x
        self.y = y
        self.root.bind("<Configure>", self._onresize)
        super(CPanel, self).__init__(canvas, x, y, width, height, fill=fill, outline=outline)

    def delete(self):
        self._canvas.delete(self._id)

    # noinspection PyUnusedLocal
    def _onresize(self, evt: _t.Any):
        # noinspection PyDeepBugsBinOperand
        if self._width == "extend":
            width = self._canvas.winfo_width() - self.x
        if self._height == "expand":
            height = self._canvas.winfo_height() - self.y
        self.coords(self.x, self.y, self._width, self._height)


class CTransparentButton(CImage):
    buttonimageNormalPil = _PIL.Image.new("RGBA", (1, 1), "#ffffff7f")
    buttonimageHoverPil = _PIL.Image.new("RGBA", (1, 1), "#ffffffaf")
    buttonimagePressedPil = _PIL.Image.new("RGBA", (1, 1), "#0000007f")

    # noinspection PyProtectedMember
    def __init__(self, canvas, x, y, height, width, text="", command=lambda: None, font=None):
        # noinspection PyProtectedMember
        self.root = canvas._root()

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x1, self.y1 = x - width / 2, y - height / 2
        self.x2, self.y2 = x + width / 2, y + height / 2

        if not hasattr(self, "buttonimageNormal"):
            a = CTransparentButton.buttonimageNormalPil.copy().resize((width, height))
            self.buttonimageNormal = _PIL.ImageTk.PhotoImage(a)
        if not hasattr(self, "buttonimageHover"):
            b = CTransparentButton.buttonimageHoverPil.copy().resize((width, height))
            self.buttonimageHover = _PIL.ImageTk.PhotoImage(b)
        if not hasattr(self, "buttonimagePressed"):
            c = CTransparentButton.buttonimagePressedPil.copy().resize((width, height))
            self.buttonimagePressed = _PIL.ImageTk.PhotoImage(c)

        canvas.update()
        self.root.update()

        super(CTransparentButton, self).__init__(canvas, x, y, image=self.buttonimageNormal)

        self._textid = CText(canvas, x, y, text=text, font=font, fill="#000000")
        self._command = command

        self._hovered = False
        self._pressed = False

        self._canvas.tag_bind(self._id, "<Enter>", self.on_enter)
        self._canvas.tag_bind(self._id, "<Leave>", self.on_leave)
        self._canvas.tag_bind(self._id, "<ButtonPress-1>", self.on_press)
        self._canvas.tag_bind(self._id, "<ButtonRelease-1>", self.on_release)
        self._canvas.tag_bind(self._textid._id, "<Enter>", self.on_enter)
        self._canvas.tag_bind(self._textid._id, "<Leave>", self.on_leave)
        self._canvas.tag_bind(self._textid._id, "<ButtonPress-1>", self.on_press)
        self._canvas.tag_bind(self._textid._id, "<ButtonRelease-1>", self.on_release)
        self._canvas.bind("<Leave>", self.on_leave)

    def delete(self):
        self._canvas.delete(self._id)
        self._textid.delete()

    def on_enter(self):
        self._canvas.itemconfig(self._id, image=self.buttonimageHover)
        self._textid.configure(fill="#000000")
        self._hovered = True

    def on_leave(self):
        # if self._pressed:
        #     self._canvas.itemconfig(self._id, image=self.buttonimagePressed)
        # else:
        self._canvas.itemconfig(self._id, image=self.buttonimageNormal)
        self._textid.configure(fill="#000000")
        self._hovered = False

    def on_press(self):
        self._canvas.itemconfig(self._id, image=self.buttonimagePressed)
        self._textid.configure(fill="#ffffff")
        self._pressed = True

    def on_release(self, event):
        if self._hovered:
            self._canvas.itemconfig(self._id, image=self.buttonimageHover)
            self._textid.configure(fill="#000000")
        else:
            self._canvas.itemconfig(self._id, image=self.buttonimageNormal)
            self._textid.configure(fill="#000000")
        self._pressed = False

        print(event.x, event.y)
        print(self.x1, self.y1, self.x2, self.y2)

        if (event.x > self.x1 and event.y > self.y1) and (event.x < self.x2 and event.y < self.y2):
            self._command()
