import os
import sys
import tempfile
from random import randint
from time import time, sleep
from tkinter import Button, Frame, Canvas, Tk
from typing import Tuple, Callable, Any, Dict

import pyglet
from PIL import Image, ImageDraw
from overload import overload

from qbubbles.advBuiltins import *
from qbubbles.bubble import place_bubble
from qbubbles.components import Store
from qbubbles.extras import get_coords
from qbubbles.registry import Registry
from qbubbles.special import ScrolledWindow
from qbubbles.teleport import teleport, tp_mode


def randint_lookup(value_in, min_, max_):
    # value_in2 = (value_in / 2) + 0.5
    sys.stderr.write(str(value_in) + " ")
    value_in2 = value_in
    return int(round(value_in2 * (max_ - min_) + min_))


def version2name(version: Tuple[str, int, int, int]):  # releasetype: str, a: int, b: int, c: int=0):
    rt: str = version[0]
    rt = rt.title()
    a_: int = version[1]
    b_: int = version[2]
    c_: int = version[3]
    return "%s %s.%s.%s" % (rt, a_, b_, c_)


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


def createbubble_image(size, inner=None, *colors):
    im = _new('RGBA', size, '#ffffff00')
    # im.putalpha(0)
    if inner is not None:
        inner_im: Optional[Image.Image] = _open(inner)
    else:
        inner_im: Optional[Image.Image] = None
    # draw = ImageDraw.Draw(im, "RGBA")
    i = 2

    # Drawung ellipses for Bubble.
    width = 0.75
    ex_w = width / 2
    w = width
    if len(colors) == 1:
        draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=colors[0], width=w, antialias=4)
        i += width + ex_w
        # print("Single circle")
    else:
        for index in range(0, len(colors)):

            if len(colors) - 1 > index > 0:  # .OOO.
                draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=colors[index], width=w + ex_w,
                             antialias=4)
            elif index == len(colors) - 1:  # ....O
                draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=colors[index], width=w, antialias=4)
            else:  # First:  O....
                draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=colors[index], width=w + ex_w,
                             antialias=4)
            i += width + (ex_w * 2)

    i += 10

    if inner is not None:
        png2 = _new('RGBA', size, (0, 0, 0, 0))
        # noinspection PyUnboundLocalVariable
        if size[0] - int(i) < png2.width:
            inner_im = inner_im.resize((size[0] - int(i), size[1] - int(i)))
        png2.paste(inner_im, (int(i / 2), int(i / 2)))
        im = Image.alpha_composite(png2, im)

    return pillow2pyglet(im=im)


def pillow2pyglet(im: Image.Image):
    if not os.path.exists("assets/temp"):
        os.makedirs("assets/temp")

    # _imaging.

    temp_file = tempfile.TemporaryFile("w+", suffix=".png", dir=os.path.abspath("assets/temp"), delete=False)
    temp_file.close()

    pyglet.resource.reindex()
    im.save(temp_file.name)
    # temp_file.name

    # image: pyglet.image.ImageData = pyglet.image.ImageData(im.width, im.height, 'RGBA', raw_image, pitch=-im.width * 4)
    image = pyglet.resource.image(os.path.join("temp", os.path.split(temp_file.name)[-1]).replace("\\", "/"))
    # pyglet.image.TextureRegion()
    os.remove(temp_file.name)
    return image


def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return AdvFloat((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2).sqrt()


# fast math algorithms
class FastRandom(object):
    def __init__(self, seed):
        self.seed = seed

    def randint(self):
        self.seed = (214013 * self.seed + 2531011)
        return (self.seed >> 16) & 0x7FFF


# rand.randint()


class Seed(object):
    def __init__(self, seed):
        self._seed = seed

    def randint(self, x, y):
        h: int = self._seed + x * 374761393 + y * 668265263
        h = (h ** (h >> 16)) * 1274126177
        return h ** (h >> 16)


def control(input_modes: dict, config: dict, root: Tk, canvas: Canvas, stats: dict, bubbles: dict, back: object, texts: dict,
            commands: dict, temp: dict, panels: dict, fore: dict, ship: dict, tp: dict, lang: dict, return_main: Callable,
            icons: dict, bub: dict, font: tuple, event, c_ammo: Callable, laucher_cfg: dict, log,
            save_system: object):
    """
    Ship-motion event
    :param save_system:
    :param log:
    :param laucher_cfg:
    :param c_ammo:
    :param font:
    :param bub:
    :param icons:
    :param ship:
    :param tp:
    :param lang:
    :param return_main:
    :param commands:
    :param fore:
    :param panels:
    :param temp:
    :param input_modes:
    :param config:
    :param root:
    :param canvas:
    :param stats:
    :param bubbles:
    :param back:
    :param texts:
    :param event:
    """

    if input_modes["store"] and commands["store"] is not None:
        if event.keysym == "Up":
            commands["store"].set_selected(canvas, -1)
        if event.keysym == "Down":
            commands["store"].set_selected(canvas, 1)
        if event.keysym == "Left":
            commands["store"].set_selected(canvas, int(-((config["height"] - 215) / 140 + 1)))
        if event.keysym == "Right":
            commands["store"].set_selected(canvas, int((config["height"] - 215) / 140 + 1))
        if event.keysym == "space":
            commands["store"].buy_selected(config, input_modes, log, root, canvas, stats, bubbles, back,
                                           texts,
                                           commands, temp, panels)
        if event.keysym == "BackSpace":
            commands["store"].exit(canvas, log, input_modes, stats, temp, commands)
            commands["store"] = None
        if event.keysym == "Escape":
            sleep(1)
            commands["store"].exit(canvas, log, input_modes, stats, temp, commands)
            commands["store"] = None
    if input_modes["present"]:
        if event.keysym == "space":
            if False != commands["present"] != True:
                commands["present"].exit(canvas)
                input_modes["pause"] = False
                input_modes["present"] = False
                stats["Effects"]["scorestate_time"] = temp["scorestate-save"] + time()
                stats["Effects"]["secure_time"] = temp["secure-save"] + time()
                stats["Effects"]["timebreak_time"] = temp["timebreak-save"] + time()
                stats["Effects"]["confusion_time"] = temp["confusion-save"] + time()
                stats["Effects"]["slowmotion_time"] = temp["slowmotion-save"] + time()
                stats["Effects"]["paralyse_time"] = temp["paralyse-save"] + time()
                stats["Effects"]["shotspeed_time"] = temp["shotspeed-save"] + time()
                stats["Effects"]["notouch_time"] = temp["notouch-save"] + time()
    if input_modes["teleport"]:
        x, y = get_coords(canvas, tp["id1"])
        if event.keysym == 'Up':
            if y > 72 + 5:
                canvas.move(tp["id1"], 0, -5)
                canvas.move(tp["id2"], 0, -5)
                canvas.move(tp["id3"], 0, -5)
                canvas.move(tp["id4"], 0, -5)
        if event.keysym == "Down":
            if y < config["height"] - 105 - 5:
                canvas.move(tp["id1"], 0, 5)
                canvas.move(tp["id2"], 0, 5)
                canvas.move(tp["id3"], 0, 5)
                canvas.move(tp["id4"], 0, 5)
        if event.keysym == "Left":
            if x > 0 + 5:
                canvas.move(tp["id1"], -5, 0)
                canvas.move(tp["id2"], -5, 0)
                canvas.move(tp["id3"], -5, 0)
                canvas.move(tp["id4"], -5, 0)
        if event.keysym == "Right":
            if x < config["width"] - 5:
                canvas.move(tp["id1"], 5, 0)
                canvas.move(tp["id2"], 5, 0)
                canvas.move(tp["id3"], 5, 0)
                canvas.move(tp["id4"], 5, 0)
        if event.keysym == "BackSpace":
            input_modes["pause"] = False

            stats["Effects"]["scorestate_time"] = temp["scorestate-save"] + time()
            stats["Effects"]["secure_time"] = temp["secure-save"] + time()
            stats["Effects"]["timebreak_time"] = temp["timebreak-save"] + time()
            stats["Effects"]["confusion_time"] = temp["confusion-save"] + time()
            stats["Effects"]["slowmotion_time"] = temp["slowmotion-save"] + time()
            stats["Effects"]["paralyse_time"] = temp["paralyse-save"] + time()
            stats["Effects"]["shotspeed_time"] = temp["shotspeed-save"] + time()
            stats["Effects"]["notouch_time"] = temp["notouch-save"] + time()
        if event.keysym == "Escape":
            input_modes["pause"] = False

            stats["Effects"]["scorestate_time"] = temp["scorestate-save"] + time()
            stats["Effects"]["secure_time"] = temp["secure-save"] + time()
            stats["Effects"]["timebreak_time"] = temp["timebreak-save"] + time()
            stats["Effects"]["confusion_time"] = temp["confusion-save"] + time()
            stats["Effects"]["slowmotion_time"] = temp["slowmotion-save"] + time()
            stats["Effects"]["paralyse_time"] = temp["paralyse-save"] + time()
            stats["Effects"]["shotspeed_time"] = temp["shotspeed-save"] + time()
            stats["Effects"]["notouch_time"] = temp["notouch-save"] + time()
            sleep(1)
        if event.keysym == "Return":
            input_modes["pause"] = False

            stats["Effects"]["scorestate_time"] = temp["scorestate-save"] + time()
            stats["Effects"]["secure_time"] = temp["secure-save"] + time()
            stats["Effects"]["timebreak_time"] = temp["timebreak-save"] + time()
            stats["Effects"]["confusion_time"] = temp["confusion-save"] + time()
            stats["Effects"]["slowmotion_time"] = temp["slowmotion-save"] + time()
            stats["Effects"]["paralyse_time"] = temp["paralyse-save"] + time()
            stats["Effects"]["shotspeed_time"] = temp["shotspeed-save"] + time()
            stats["Effects"]["notouch_time"] = temp["notouch-save"] + time()

            stats["teleports"] -= 1
            teleport(canvas, root, stats, input_modes, ship, tp, tp["id1"])
        if event.keysym.lower() == "space":
            input_modes["pause"] = False

            stats["Effects"]["scorestate_time"] = temp["scorestate-save"] + time()
            stats["Effects"]["secure_time"] = temp["secure-save"] + time()
            stats["Effects"]["timebreak_time"] = temp["timebreak-save"] + time()
            stats["Effects"]["confusion_time"] = temp["confusion-save"] + time()
            stats["Effects"]["slowmotion_time"] = temp["slowmotion-save"] + time()
            stats["Effects"]["paralyse_time"] = temp["paralyse-save"] + time()
            stats["Effects"]["shotspeed_time"] = temp["shotspeed-save"] + time()
            stats["Effects"]["notouch_time"] = temp["notouch-save"] + time()

            stats["teleports"] -= 1
            teleport(canvas, root, stats, input_modes, ship, tp, tp["id1"])
    elif event.keysym.lower() == "space":
        ammo_object = c_ammo()
        ammo_object.create(None, None)
    if event.keysym == "Escape" and (not input_modes["pause"]) and (not input_modes["store"]) and (not input_modes["teleport"]) and \
            (not input_modes["window"]) and (not input_modes["present"]) and (not input_modes["cheater"]):
        input_modes["pause"] = True

        canvas.delete(icons["pause"])
        if stats["Effects"]["special-level"]:
            temp['pause/bg'] = canvas.create_rectangle(0, 69,
                                                       config["width"],
                                                       config[
                                                           "height"],
                                                       fill="#3f3f3f",
                                                       outline="#3f3f3f")
            temp['pause/toline'] = canvas.create_line(0, 69, config["width"], 69,
                                                      fill="#afafaf")
            # temp['pause/bottom.line'] = canvas.create_line(0, config["height"] - 102, config["width"],
            #                                                config["height"] - 102,
            #                                                fill="#afafaf")

            temp['pause/menu_frame'] = Frame(root, bg="#3f3f3f")
            temp['pause/menu'] = canvas.create_window(config["middle-x"], config["middle-y"] / 2 + 130,
                                                      window=temp['pause/menu_frame'], anchor='n',
                                                      height=20, width=300)

            temp["pause/back-to-menu"] = Button(temp["pause/menu_frame"], text=lang["pause.back-to-home"],
                                                command=lambda: return_main(),
                                                relief="flat", bg="#1f1f1f", fg="#afafaf", font=font)
            back = "#1f1f1f"
            fore = "yellow"
        else:
            temp['pause/bg'] = canvas.create_rectangle(0, 69,
                                                       config["width"],
                                                       config[
                                                           "height"],
                                                       fill="darkcyan",
                                                       outline="darkcyan")
            temp['pause/toline'] = canvas.create_line(0, 69, config["width"], 69,
                                                      fill="#7fffff")
            # temp['pause/bottom.line'] = canvas.create_line(0, config["height"] - 102, config["width"],
            #                                                config["height"] - 102,
            #                                                fill="#7fffff")

            temp['pause/menu_frame'] = Frame(root, bg="darkcyan")
            temp['pause/menu'] = canvas.create_window(config["middle-x"], config["middle-y"] / 2 + 130,
                                                      window=temp['pause/menu_frame'], anchor='n',
                                                      height=500, width=300)

            temp["pause/back-to-menu"] = Button(temp["pause/menu_frame"], text=lang["pause.back-to-home"],
                                                command=lambda: return_main(),
                                                relief="flat", bg="#005f5f", fg="#7fffff", font=[font])

            back = "#005f5f"
            fore = "#7fffff"

        temp["s_frame"] = Frame(root, bg=back)
        temp["s_frame"].place(x=config["middle-x"], y=config["middle-y"] / 2 + 250, anchor='n', width=1000)

        temp["sw"] = ScrolledWindow(temp["s_frame"], 1020, 321, height=321, width=1000)

        temp["canv"] = temp["sw"].canv
        temp["canv"].config(bg=back)
        temp["sw"].scrollwindow.config(bg=back)

        temp["frame"] = temp["sw"].scrollwindow

        class_names = ("Normal", "Double", "Kill", "Triple", "SpeedUp", "SpeedDown", "Up", "Ultimate", "DoubleState",
                       "Protect", "SlowMotion", "TimeBreak", "Confusion", "HyperMode", "Teleporter",
                       "Coin", "NoTouch", "Paralyse", "Diamond", "StoneBub", "Present", "SpecialKey", "LevelKey")

        id_names = (
            "bubble.normal", "bubble.double", "bubble.kill", "bubble.triple", "bubble.speedup", "bubble.speeddown",
            "bubble.up", "bubble.state.ultimate", "bubble.state.double", "bubble.state.protect",
            "bubble.state.slowmotion",
            "bubble.state.timebreak", "bubble.state.confusion", "bubble.state.hypermode", "bubble.teleporter",
            "bubble.coin", "bubble.state.notouch", "bubble.state.paralyse", "bubble.diamond", "bubble.stonebubble",
            "bubble.present", "bubble.state.specialkey", "bubble.levelkey"
        )

        canvass = Canvas(temp["frame"], bg=back, highlightthickness=0)
        x = 50
        y = 50
        temp["pause/bubble.iconss"] = []
        for i in range(len(class_names)):
            # print(class_names[i], b[i])
            place_bubble(canvass, bub, x, y, 25, class_names[i])
            canvass.create_text(x, y + 40, text=lang[id_names[i]], fill=fore, font=[font, 10])
            if x > 900:
                x = 50
                y += 100
            else:
                x += 100

        canvass.config(height=y + 70, width=1000)
        canvass.pack(fill="y")

        temp["pause/back-to-menu"].pack(fill="x")

        icons["pause"] = canvas.create_image(config["middle-x"], config["middle-y"] / 2,
                                             image=icons["pause-id"])

        canvas.itemconfig(texts["pause"], text="")
        root.update()

        temp["scorestate-save"] = stats["Effects"]["scorestate_time"] - time()
        temp["secure-save"] = stats["Effects"]["secure_time"] - time()
        temp["timebreak-save"] = stats["Effects"]["timebreak_time"] - time()
        temp["confusion-save"] = stats["Effects"]["confusion_time"] - time()
        temp["slowmotion-save"] = stats["Effects"]["slowmotion_time"] - time()
        temp["paralyse-save"] = stats["Effects"]["paralyse_time"] - time()
        temp["shotspeed-save"] = stats["Effects"]["shotspeed_time"] - time()
        temp["notouch-save"] = stats["Effects"]["notouch_time"] - time()
        temp["special-level-save"] = stats["Effects"]["special-level_time"] - time()
    elif event.keysym == "Escape" and input_modes["pause"] and (not input_modes["store"]) and (not input_modes["teleport"]) and \
            (not input_modes["window"]) and (not input_modes["present"]) and (not input_modes["cheater"]):
        input_modes["pause"] = False

        canvas.itemconfig(icons["pause"], state="hidden")
        canvas.itemconfig(texts["pause"], text="")

        temp["pause/back-to-menu"].destroy()
        temp['pause/menu_frame'].destroy()
        temp["s_frame"].destroy()

        canvas.delete(temp['pause/toline'])
        # canvas.delete(temp['pause/bottom.line'])
        canvas.delete(temp['pause/menu'])
        canvas.delete(temp['pause/bg'])

        root.update()

        stats["Effects"]["scorestate_time"] = temp["scorestate-save"] + time()
        stats["Effects"]["secure_time"] = temp["secure-save"] + time()
        stats["Effects"]["timebreak_time"] = temp["timebreak-save"] + time()
        stats["Effects"]["confusion_time"] = temp["confusion-save"] + time()
        stats["Effects"]["slowmotion_time"] = temp["slowmotion-save"] + time()
        stats["Effects"]["paralyse_time"] = temp["paralyse-save"] + time()
        stats["Effects"]["shotspeed_time"] = temp["shotspeed-save"] + time()
        stats["Effects"]["notouch_time"] = temp["notouch-save"] + time()
    if event.keysym == "t" and stats["teleports"] > 0 and (not input_modes["teleport"]):
        input_modes["pause"] = True

        temp["scorestate-save"] = stats["Effects"]["scorestate_time"] - time()
        temp["secure-save"] = stats["Effects"]["secure_time"] - time()
        temp["timebreak-save"] = stats["Effects"]["timebreak_time"] - time()
        temp["confusion-save"] = stats["Effects"]["confusion_time"] - time()
        temp["slowmotion-save"] = stats["Effects"]["slowmotion_time"] - time()
        temp["paralyse-save"] = stats["Effects"]["paralyse_time"] - time()
        temp["shotspeed-save"] = stats["Effects"]["shotspeed_time"] - time()
        temp["notouch-save"] = stats["Effects"]["notouch_time"] - time()
        temp["special-level-save"] = stats["Effects"]["special-level_time"] - time()

        input_modes["teleport"] = True

        tp_mode(canvas, config, stats, input_modes, tp)
    if event.keysym.lower() == "e" and (not input_modes["store"]):
        input_modes["pause"] = True
        temp["scorestate-save"] = stats["Effects"]["scorestate_time"] - time()
        temp["secure-save"] = stats["Effects"]["secure_time"] - time()
        temp["timebreak-save"] = stats["Effects"]["timebreak_time"] - time()
        temp["confusion-save"] = stats["Effects"]["confusion_time"] - time()
        temp["slowmotion-save"] = stats["Effects"]["slowmotion_time"] - time()
        temp["paralyse-save"] = stats["Effects"]["paralyse_time"] - time()
        temp["shotspeed-save"] = stats["Effects"]["shotspeed_time"] - time()
        temp["notouch-save"] = stats["Effects"]["notouch_time"] - time()
        temp["special-level-save"] = stats["Effects"]["special-level_time"] - time()
        input_modes["store"] = True
        log.debug("bub_move", "Creating Store() to input mode \"store\"")
        log.debug("bub_move", "storemode=" + str(input_modes["store"]))
        commands["store"] = Store(canvas, log, config, input_modes, stats, icons, fore, font, laucher_cfg)
    # if event.char == "/":
    #     CheatEngine().event_handler(canvas, input_modes, stats, config, temp, log, backgrounds, bubble, event, bub)
    # if input_modes["cheater"]:
    #     CheatEngine().input_event_handler(canvas, log, stats, backgrounds, bubble, event, config, bub, temp,
    #                                       input_modes)

    if event.keysym == "Escape":
        save_system.save()
    root.update()


def get_error_with_class_path(e: Exception, obj: Any) -> str:
    # if hasattr(obj, "__qualname__"):
    #     if hasattr(obj, "__module__"):
    #         text = f"{obj.__module__}.{obj.__qualname__}"
    #     else:
    #         text = f"{obj.__name__}"
    # elif hasattr(obj, "__module__"):
    #     text = f"{obj.__module__}.*"
    # elif hasattr(obj, "__class__"):
    #     if hasattr(obj.__class__, "__qualname__"):
    #         if hasattr(obj.__class__, "__module__"):
    #             text = f"{obj.__class__.__module__}.{obj.__class__.__qualname__}"
    #         else:
    #             text = f"{obj.__class__.__qualname__}"
    #     elif hasattr(obj.__class__, "__module__"):
    #         text = f"{obj.__class__.__module__}.*"
    #     else:
    #         text = f"<UNKNOWN-CLASS>"
    # else:
    #     text = f"<UNKNOWN-FUNCTION>"

    if hasattr(obj, "__qualname__"):
        text = f"{obj.__qualname__}"

    tb = e.__traceback__
    while tb:
        line = f" at line {tb.tb_lineno}"
        file = f"<{tb.tb_frame.f_code.co_filename}>"
        tb = tb.tb_next

    return f"({file}.{text}) {e.__class__.__name__}{line}: {str(e)}"


def get_adv_error(e: Exception, obj):
    tb = e.__traceback__

    text = f"{e.__class__.__name__}: {str(e)}"

    while tb:
        text += f"\n  {tb.tb_frame.f_code.co_filename} ({tb.tb_frame.f_code.co_name}:{tb.tb_frame.f_lineno})"
        tb = tb.tb_next

    return text


def print_adv_error(e: Exception, obj):
    print("\n"+get_adv_error(e, obj)+"\n", end="", file=sys.stderr)


def tkinter_adv_error(e: Exception, obj):
    # root = Tk()
    # root.wm_attributes("-alpha", 0)
    # root.maxsize(1, 1)
    # root.wm_withdraw()

    # mb.showerror("Python crash", get_adv_error(e, obj))
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.font

    root = tk.Tk()
    root.title("Python crash")
    icon = ttk.Label(root, image="::tk::icons::error")
    icon.pack(side=tk.LEFT, padx=10, pady=10)
    # text = ttk.Label(root, text=get_adv_error(e, obj), font=tkinter.font.nametofont("TkFixedFont"))
    # text.pack(side=tk.LEFT, expand=True, fill='both')
    text = tk.Text(root, height=8, borderwidth=0, font=tkinter.font.nametofont("TkFixedFont"))
    text.insert(1.0, get_adv_error(e, obj))
    text.pack(expand=True, fill="both")

    text.configure(state="disabled")

    # if tkinter is 8.5 or above you'll want the selection background
    # to appear like it does when the widget is activated
    # comment this out for older versions of Tkinter
    text.configure(inactiveselectbackground=text.cget("selectbackground"))

    button = ttk.Button(root, text="OK", command=lambda: root.destroy())
    button.pack(side=tk.BOTTOM)
    button.focus_set()
    root.mainloop()


def _adv_excepthook(exc_type, exc_value, exc_traceback):
    tb = exc_traceback

    text = f"{exc_type.__name__}: {str(exc_value)}"

    while tb:
        text += f"\n  {tb.tb_frame.f_code.co_filename} ({tb.tb_frame.f_code.co_name}:{tb.tb_frame.f_lineno})"
        tb = tb.tb_next

    return text


def adv_excepthook(exc_type, exc_value, exc_traceback):
    print("\n"+_adv_excepthook(exc_type, exc_value, exc_traceback)+"\n", end="", file=sys.stderr)


def tkinter_excepthook(exc_type, exc_value, exc_traceback):

    # root = Tk()
    # root.wm_attributes("-alpha", 0)
    # root.maxsize(1, 1)
    # root.wm_withdraw()

    # mb.showerror("Python crash", get_adv_error(e, obj))
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.font

    root = tk.Tk()
    root.title("Python crash")
    icon = ttk.Label(root, image="::tk::icons::error")
    icon.pack(side=tk.LEFT, padx=10, pady=10)
    # text = ttk.Label(root, text=get_adv_error(e, obj), font=tkinter.font.nametofont("TkFixedFont"))
    # text.pack(side=tk.LEFT, expand=True, fill='both')
    text = tk.Text(root, height=8, borderwidth=0, font=tkinter.font.nametofont("TkFixedFont"), bg=root.cget("bg"))
    text.insert(1.0, _adv_excepthook(exc_type, exc_value, exc_traceback))
    text.pack(expand=True, fill="both")

    text.configure(state="disabled")

    # if tkinter is 8.5 or above you'll want the selection background
    # to appear like it does when the widget is activated
    # comment this out for older versions of Tkinter
    text.configure(inactiveselectbackground=text.cget("selectbackground"))

    button = ttk.Button(root, text="OK", command=lambda: root.destroy())
    button.pack(side=tk.BOTTOM)
    button.focus_set()
    root.mainloop()


class Background:
    """
    Background for the title menu.
    This is a random animation.
    """

    def __init__(self, root: Tk):
        # Widgets
        self._root = root
        self._canvas = Canvas(root, bg="#00afaf", highlightthickness=0)
        self._canvas.pack(fill="both", expand="true")

        # Bubble-sprites config.
        self.__bubbles = []
        self.__speed = []

    def create_bubble(self):
        r = randint(9, 60)
        x = self._root.winfo_width() + 100
        y = randint(int(r), int(self._canvas.winfo_height() - r))

        spd = randint(7, 10)

        self.__bubbles.append(self._canvas.create_oval(x - r, y - r, x + r, y + r, outline="white"))
        self.__speed.append(spd)

    def cleanup_bubs(self):
        """
        Cleaning up bubbles.
        Deleting bubble if the x coord of the bubble is under -100
        :return:
        """
        from .bubble import get_coords

        for index in range(len(self.__bubbles) - 1, -1, -1):
            x, y, = get_coords(self._canvas, self.__bubbles[index])
            if x < -100:
                self._canvas.delete(self.__bubbles[index])
                del self.__bubbles[index]
                del self.__speed[index]

    def move_bubbles(self):
        """
        Move all bubble to the left with the self.__speed with index of the bubble
        :return:
        """
        for index in range(len(self.__bubbles) - 1, -1, -1):
            self._canvas.move(self.__bubbles[index], -self.__speed[index], 0)

    def destroy(self):
        """
        Destroys this custom widget.
        :return:
        """
        self._canvas.destroy()


class Font(object):
    def __init__(self, fam: str = None, siz: int = None, stl: str = None):
        self.family = "Helvetica"
        self.size = 10
        self.style = ""
        if fam:
            self.family = fam
        if siz:
            self.size = siz
        if stl:
            self.style = stl

    def get_tuple(self):
        return self.family, Registry.get_window("default").tkScale(self.size), self.style


class Color(object):
    @overload
    def __init__(self, r, g, b, a=None):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        if a is None:
            self.a = 255

    @__init__.add
    def __init__(self, hex_):
        self.r = eval(f"0x{hex_[1:3]}")
        self.g = eval(f"0x{hex_[3:5]}")
        self.b = eval(f"0x{hex_[5:7]}")

    # def __init__(self, *args, **kwargs):
    #     if len(args) == 1:
    #     elif len(args) == 3:
    #         self.r = args[0]
    #         self.g = args[1]
    #         self.b = args[2]
    #     elif len(kwargs.keys()) == 1:
    #         hex_ = kwargs.pop("hex_")
    #         self.r = eval(f"0x{hex_[1:3]}")
    #         self.g = eval(f"0x{hex_[3:5]}")
    #         self.b = eval(f"0x{hex_[5:7]}")
    #     elif len(kwargs.keys()) == 3:
    #         self.r = kwargs.pop("r", None)
    #         self.g = kwargs.pop("g", None)
    #         self.b = kwargs.pop("b", None)
    #         self.r = kwargs.pop("red") if self.r is None else self.r
    #         self.g = kwargs.pop("green") if self.g is None else self.g
    #         self.b = kwargs.pop("blue") if self.b is None else self.b
    #     else:
    #         raise NameError("Arguments doesn't match any overload")
    #     self.r = self.r % 256
    #     self.g = self.g % 256
    #     self.b = self.b % 256

    def get_tkcolor(self):
        r = hex(self.r)[2:]
        g = hex(self.g)[2:]
        b = hex(self.b)[2:]
        if len(r) == 1:
            r = "0"+r
        if len(g) == 1:
            g = "0"+g
        if len(b) == 1:
            b = "0"+b
        if len(r) > 2:
            raise OverflowError(f"red color is more than 255 (int) or FF (hex)")
        if len(g) > 2:
            raise OverflowError(f"green color is more than 255 (int) or FF (hex)")
        if len(b) > 2:
            raise OverflowError(f"blue color is more than 255 (int) or FF (hex)")
        return f"#{r+g+b}"


    def get_pilcolor(self):
        r = hex(self.r)[2:]
        g = hex(self.g)[2:]
        b = hex(self.b)[2:]
        a = hex(self.a)[2:]
        if len(r) == 1:
            r = "0"+r
        if len(g) == 1:
            g = "0"+g
        if len(b) == 1:
            b = "0"+b
        if len(a) == 1:
            a = "0"+a
        if len(r) > 2:
            raise OverflowError(f"red color is more than 255 (int) or FF (hex)")
        if len(g) > 2:
            raise OverflowError(f"green color is more than 255 (int) or FF (hex)")
        if len(b) > 2:
            raise OverflowError(f"blue color is more than 255 (int) or FF (hex)")
        if len(a) > 2:
            raise OverflowError(f"alpha color is more than 255 (int) or FF (hex)")
        return f"#{r+g+b+a}"


class Maintance:
    def __init__(self):
        pass

    @staticmethod
    def auto_save(save_name: str, game_stats: Dict[str, Any]):
        """
        Saves the game. (For Auto-Save)
        """
        from qbubbles import config as cfg

        import os

        print(os.curdir)

        try:
            cfg.Writer(f"{Registry.gameData['launcherConfig']['gameDir']}saves/" + save_name + "/game.nzt", game_stats.copy())
            # cfg.Writer(f"{Registry.gameData['launcherConfig']['gameDir']}saves/" + save_name + "/bubble.nzt", bubble.copy())
        except FileNotFoundError as e:
            print(e.args)
            print(e.filename)
            print(e.filename2)

    @staticmethod
    def auto_restore(save_name: str):
        """
        Restoring. (For Auto-Restore)
        """
        from qbubbles import config as cfg

        game_stats = cfg.Reader(f"{Registry.gameData['launcherConfig']['gameDir']}saves/" + save_name + "/game.nzt").get_decoded()

        return game_stats

    @staticmethod
    def reset(save_name: str):
        """
        Resets the game fully
        """
        from qbubbles import config as cfg

        stats = cfg.Reader("versions/" + Registry.gameData["launcherConfig"]["versionDir"] + "/config/reset.nzt").get_decoded()
        bubble = cfg.Reader("versions/" + Registry.gameData["launcherConfig"]["versionDir"] + "/config/reset-bubble.nzt").get_decoded()

        cfg.Writer(f"{Registry.gameData['launcherConfig']['gameDir']}saves/" + save_name + "/game.nzt", stats.copy())
        cfg.Writer(f"{Registry.gameData['launcherConfig']['gameDir']}saves/" + save_name + "/bubble.nzt", bubble.copy())


if __name__ == '__main__':
    c_ = Color(255, 255, 255)
    print()
    print(c_.get_tkcolor())
    print(c_.get_pilcolor())

    c_ = Color(15, 31, 63, 127)
    print()
    print(c_.get_tkcolor())
    print(c_.get_pilcolor())
