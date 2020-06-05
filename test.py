import os
from tkinter import Tk, Frame, Button

import win32gui
import win32ui
from ctypes import windll
from PIL import Image


def get_image(widget):
    if isinstance(widget, Tk):
        hwnd = win32gui.GetParent(widget.winfo_id())
        left, top, right, bot = win32gui.GetClientRect(hwnd)
    else:
        hwnd = win32gui.GetParent(win32gui.GetParent(widget.winfo_id()))
        left, top, right, bot = win32gui.GetClientRect(hwnd)
        # left += int(widget.winfo_rootx())
        # top += int(widget.winfo_rooty())
        # left = widget.winfo_rooty()
        # top = widget.winfo_rootx()
        # right = left + widget.winfo_height()
        # bot = top + widget.winfo_width()

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    save_bit_map = win32ui.CreateBitmap()
    save_bit_map.CreateCompatibleBitmap(mfc_dc, w, h)

    save_dc.SelectObject(save_bit_map)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 1)
    # result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0)
    print(result)

    bmpinfo = save_bit_map.GetInfo()
    bmpstr = save_bit_map.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(save_bit_map.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    if result == 1:
        # PrintWindow Succeeded
        # im.save("test.png")
        return im

    save_dc.DeleteDC()
    hwnd_dc.DeleteDC()

    # root.wm_protocol("WM_DELETE_WINDOW", lambda: os.kill(os.getpid(), 0))


if __name__ == '__main__':
    root = Tk()

    frame = Frame(root, bg="#ff0000")
    button = Button(frame, bg="#7c7c7c")
    button.pack(pady=10, padx=10)
    frame.pack(fill="both", expand=True)

    root.update()

    get_image(button).save("test.png")
    root.mainloop()
