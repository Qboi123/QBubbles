from time import time
from tkinter import Tk, Canvas
from typing import *

from qbubbles.extras import get_coords


def create_shot(canvas: Canvas, ammo, config: Dict[str, Union[str, int, dict]], ship: dict, stats):
    """
    Creates Shooting ammo
    :param stats:
    :param ship:
    :param config:
    :param ammo:
    :type canvas: Canvas
    """
    if ammo["retime"] < time():
        x, y = get_coords(canvas, ship["id"])
        ammo["ammo-id"].append(canvas.create_line(10 + x + config["Game"]["ship-radius"] / 2, y,
                                                  15 + x + config["Game"]["ship-radius"] / 2,
                                                  y, fill="yellow"))
        ammo["ammo-speed"].append(stats["shotspeed"])
        ammo["ammo-damage"].append(0)
        ammo["retime"] = time() + 0.5


def move_ammo(canvas: Canvas, log, root: Tk, ammo: dict):
    """
    Motion for ammo.
    """
    for i in range(len(ammo["ammo-id"])-1, -1, -1):
        try:
            canvas.move(ammo["ammo-id"][i], ammo["ammo-speed"][i], 0)
        except IndexError:
            log.warning("move_ammo", "Can't move ammo index '" + str(i) + "'.")
        root.update()


def del_ammo(canvas: Canvas, id: int, ammo: dict):
    """
    Deletes ammo by request.
    :param canvas:
    :param ammo:
    :param id:
    :return:
    """
    canvas.delete(ammo["ammo-id"][id])
    del ammo["ammo-id"][id]
    del ammo["ammo-speed"][id]
    del ammo["ammo-damage"][id]


def clean_up_shots(canvas: Canvas, ammo: dict, config: Dict[str, Union[str, int]]):
    """
    Removes ammo if it's off screen.
    :return:
    """
    for i in range(len(ammo["ammo-id"]) - 1, -1, -1):
        x, y = get_coords(canvas, ammo["ammo-id"][i])
        if x > config["width"] + config["screen-gap"]:
            del_ammo(canvas, i, ammo)
