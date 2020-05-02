import tkinter as tk
import tkinter.tix as tix
import zipfile
from PIL import Image, ImageTk, ImageDraw2, ImageDraw, ImageFont


def extract_zipfile(path2zip: str, extract_path: str):
    zip_ref = zipfile.ZipFile(path2zip, 'r')
    zip_ref.extractall(extract_path)
    zip_ref.close()


def replace_dir2ver(string: str):
    return string.replace("_pre", "-pre").replace("_", ".")


def replace_ver2dir(string: str):
    return string.replace("-pre", "_pre").replace(".", "_")


def replace_name2dir(string: str):
    return replace_ver2dir(replace_name2ver(string))


def replace_name2ver(string: str):
    return string.replace(" - Pre Release ", "-pre")


def replace_any2name(ver: str):
    ver = replace_dir2ver(ver)
    return ver.replace("-pre", " - Pre Release ")


def yamldict2class(obj: dict):
    """
    DON'T USE THIS. THIS DOESN'T WORKING
    :param obj:
    :return:
    """
    keys = list(obj.keys())
    values = list(obj.values())
    length = len(keys)

    class DictClass:
        def __init__(self):
            pass

    obj2 = dict()

    for index in range(length):
        key = keys[index]
        value = values[index]
        print("Key: %s | Find Dot: %s" % (key, key.find(".")))

        keys2, values2 = dotkeyvalue(key, value)
        # length2 =

        # for index2 in range(length2):


        dictClass.__dict__[key] = value



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


def draw_ellipse(image, bounds, width=1.0, outline='white', antialias=4):
    """Improved ellipse drawing function, based on PIL.ImageDraw."""

    # Use a single channel image (mode='L') as mask.
    # The size of the mask can be increased relative to the imput image
    # to get smoother looking results.
    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='L', color='black')
    draw = ImageDraw.Draw(mask)

    # draw outer shape in white (color) and inner shape in black (transparent)
    for offset, fill in (width / -1.5, '#ffffffff'), (width / 1.5, '#000000ff'):  # Note: Was first white, black
        left, top = [(value + offset) * antialias for value in bounds[:2]]
        right, bottom = [(value - offset) * antialias for value in bounds[2:]]
        draw.ellipse([left, top, right, bottom], fill=fill)

    # downsample the mask using PIL.Image.LANCZOS
    # (a high-quality downsampling filter).
    mask = mask.resize(image.size, Image.LANCZOS)
    # paste outline color to input image through the mask
    image.paste(outline, mask=mask)


def openbackground(fp, size: tuple):
    im = Image.open(fp)
    im = im.resize(size)
    return ImageTk.PhotoImage(im)


def openresized(fp, size: tuple):
    im = Image.open(fp)
    im = im.resize(size)
    return ImageTk.PhotoImage(im)


def openimage(fp):
    im = Image.open(fp)
    return ImageTk.PhotoImage(im)


def maketextimage(text: str, color=None):
    font = ImageFont.truetype("font/Superfats.ttf", 15)
    a = font.getsize_multiline(text)
    # a = list(a)
    # a[0] *= 2
    # a[1] *= 2
    # a = tuple(a)

    im = Image.new('RGBA', a, (0, 0, 0, 0))
    # fonts = ImageDraw2.ImageFont.load_path("font/")
    drawing = ImageDraw2.ImageDraw.Draw(im)

    drawing.text((0, 0), text, font=font)
    return ImageTk.PhotoImage(im)


def _new(mode, size, color):
    return Image.new(mode, size, color)


def _open(fp, mode: str = "r"):
    return Image.open(fp, mode)


def createbackground(size, color):
    return _new("RGBA", size, color)


def createcolorfield(size, color):
    return createbackground(size, color)


def createellipse(size, bg, fill=None, outline=None, width: int = 0):
    im = _new('RGBA', size, bg)
    draw = ImageDraw.Draw(im, 'RGBA')
    draw.ellipse((0, 0, *size), fill, outline, width)


def createbubble_image(size, inner_image: Image.Image = None, *colors):
    """
    Create bubble image from colors, and optionally create inner image (transparency allowed)
    Using Pillow it's easy to create antialized images for tkinter.
    Use in mods:
        # imports
        from qbubbles.resources import ModelLoader

        # pre initialize method of Addon
        ...  # Here is code
        for bubble in bubbles:
            pre_data = self.zipimport.get_data(f"assets/models/bubble/{bubble.get_uname()}.json")
            data = json.loads(pre_data)
            images = ModelLoader.generate_bubble_images(bubble.minSize, bubble.maxSize, data)
        ...  # Here is code (do something with the images, such as using them for the mod-bubbles)

    :param size: Size of the bubble type: Tuple[int, int].
    :param inner_image: The inner image in the middle of the bubble.
    :param colors: The colors of the bubble.
    :return: ImageTk.PhotoImage instance. Has support for tkinter.
    """
    # Create base image for bubble (transparent)
    im = _new('RGBA', size, '#ffffff00')
    i = 2

    # Drawing ellipses for Bubble.
    width = 1
    w = width
    for circ_color in colors:
        if circ_color != colors[0]:
            draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=circ_color, width=w, antialias=8)
        elif circ_color != colors[-1]:
            draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=circ_color, width=w, antialias=8)
        else:
            draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=circ_color, width=w, antialias=8)
        i += 1.5

    i += 10

    # if inner_image is specified then draw the inner image in the middle of the bubble (transparency allowed)
    if inner_image is not None:
        png2 = _new('RGBA', size, (0, 0, 0, 0))
        inner_image = inner_image.resize((size[0] - int(i), size[1] - int(i)))
        png2.paste(inner_image, (int(i / 2), int(i / 2)))

        im = Image.alpha_composite(png2, im)

    return ImageTk.PhotoImage(im)


def makebuttonimage(fp: str, text: str, font: str, size: tuple):
    pass


class ScrolledWindow(tk.Frame):
    """
    1. Master widget gets scrollbars and a canvas. Scrollbars are connected
    to canvas scrollregion.

    2. self.scrollwindow is created and inserted into canvas

    Usage Guideline:
    Assign any widgets as children of <ScrolledWindow instance>.scrollwindow
    to get them inserted into canvas

    __init__(self, parent, canv_w = 400, canv_h = 400, *args, **kwargs)
    docstring:
    Parent = master of scrolled window
    canv_w - width of canvas
    canv_h - height of canvas

    """

    def __init__(self, parent, canv_w=400, canv_h=400, expand=False, fill=None, height=None, width=None, *args, scrollcommand=lambda: None, **kwargs):
        """Parent = master of scrolled window
        canv_w - width of canvas
        canv_h - height of canvas

       """
        from .theme import CustomScrollbar
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.scrollCommand = scrollcommand

        # creating a scrollbars

        if width is None:
            __width = 0
        else:
            __width = width

        if height is None:
            __height = 0
        else:
            __height = width

        self.canv = tk.Canvas(self.parent, bg='#FFFFFF', width=canv_w, height=canv_h,
                           scrollregion=(0, 0, __width, __height), highlightthickness=0)
        # self.hbar = Scrollbar(self.parent, orient=HORIZONTAL)
        # self.hbar.pack(side=BOTTOM, fill="x")
        # self.hbar.config(command=self.canv.xview)

        self.vbar = CustomScrollbar(self.parent, width=5, command=self.canv.yview)
        self.canv.configure(yscrollcommand=self.vbar.set)

        self.vbar.pack(side="right", fill="y")
        #
        # with open(__file__, "r") as f:
        #     text.insert("end", f.read())
        # self.vbar = tix.Scrollbar(self.parent, orient=tk.VERTICAL, background="#3f3f3f", activebackground="#FFD800")
        # self.vbar.pack(side=tk.RIGHT, fill=tk."y")
        # self.vbar.config(command=self.canv.yview)
        # self.canv.config(  # xscrollcommand=self.hbar.set,
        #                  yscrollcommand=self.vbar.set)
        self.canv.pack(side=tk.LEFT, fill=fill, expand=expand)
        # creating a canvas
        # self.canv = tk.Canvas(self.parent, width=canv_w, height=canv_h)
        # self.canv.config(relief='flat',
        #                  width=canv_w,
        #                  heigh=canv_h, bd=2)
        # placing a canvas into frame
        # self.canv.grid(column=0, row=0, sticky='nsew')
        # accociating scrollbar comands to canvas scroling
        # self.hbar.config(command=self.canv.xview)
        # self.vbar.config(command=self.canv.yview)

        # creating a frame to inserto to canvas
        self.scrollwindow = tk.Frame(self.parent, height=height, width=width)

        self.scrollwindow2 = self.canv.create_window(0, 0, window=self.scrollwindow, anchor='nw', height=height, width=width)

        self.canv.config(  # xscrollcommand=self.hbar.set,
                         yscrollcommand=self.vbar.set,
                         scrollregion=(0, 0, canv_h, canv_w))

        # self.vbar.lift(self.scrollwindow)
        # self.hbar.lift(self.scrollwindow)
        self.scrollwindow.bind('<Configure>', self._configure_window)
        self.scrollwindow.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollwindow.bind('<Leave>', self._unbound_to_mousewheel)

        return

    def _bound_to_mousewheel(self, event):
        self.canv.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canv.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canv.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # self.scrollCommand(int(-1 * (event.delta / 120)), self.scrollwindow.winfo_reqheight(), self.vbar.get(), self.vbar)

    def _configure_window(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight()+1)
        self.canv.config(scrollregion='0 0 %s %s' % size)
        # if self.scrollwindow.winfo_reqwidth() != self.canv.winfo_width():
        #     # update the canvas's width to fit the inner frame
        #     # self.canv.config(width=self.scrollwindow.winfo_reqwidth())
        # if self.scrollwindow.winfo_reqheight() != self.canv.winfo_height():
        #     # update the canvas's width to fit the inner frame
        #     # self.canv.config(height=self.scrollwindow.winfo_reqheight())


if __name__ == '__main__':
    from tkinter import *
    from PIL import Image
    root = Tk()
    root.wm_attributes("-fullscreen", True)
    c = Canvas(root, highlightthickness=0)

    size = 60
    i = size

    ddd = createbubble_image((i, i), None, "black", "orange", "yellow")

    c.create_rectangle(5, 5, size/2+10, size/2+10, fill="darkcyan")
    c.create_image(size/2+10, size/2+10, image=ddd)
    c.pack(fill="both", expand=True)
    root.mainloop()
