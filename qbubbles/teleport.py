from qbubbles.extras import get_coords


def tp_mode(canvas, config, stats, modes, tp):
    """
    Teleport mode.
    Activated if you pressed F12, and have 1 or more TP's
    :rtype: object
    """
    stats["timebreak"] = True
    modes["tpmode"] = True

    # Creates Teleport-ID's
    tp["id1"] = canvas.create_oval(0, 0, 20, 20, outline="black")
    tp["id2"] = canvas.create_line(0, 10, 20, 10, fill="black")
    tp["id3"] = canvas.create_line(10, 0, 10, 20, fill="black")
    tp["id4"] = canvas.create_oval(7, 7, 13, 13, outline="black")

    # Moves teleport-ID's to mid.
    canvas.move(tp["id1"], config["middle-x"] - 10, config["middle-y"] - 10)
    canvas.move(tp["id2"], config["middle-x"] - 10, config["middle-y"] - 10)
    canvas.move(tp["id3"], config["middle-x"] - 10, config["middle-y"] - 10)
    canvas.move(tp["id4"], config["middle-x"] - 10, config["middle-y"] - 10)


def teleport(canvas, root, stats, modes, ship, tp, teleport_id):
    """
    Teleporting.
    Activating by TP_mode, if pressed on Spacebar.
    :param modes:
    :param stats:
    :param tp:
    :param ship:
    :param root:
    :param canvas:
    :param teleport_id:
    :rtype: object
    """

    # Globals
    stats["timebreak"] = False
    modes["teleport"] = False

    # Setting up variables for teleporting.
    s_x, s_y = get_coords(canvas, ship["id"])
    t_x, t_y = get_coords(canvas, teleport_id)
    x_move = t_x - s_x
    y_move = t_y - s_y

    # Teleporting.
    canvas.move(ship["id"], x_move, y_move)

    # Deletes Teleport ID's
    canvas.delete(tp["id1"])
    canvas.delete(tp["id2"])
    canvas.delete(tp["id3"])
    canvas.delete(tp["id4"])

    # Updates the screen
    root.update()
