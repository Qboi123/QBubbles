from tkinter import Canvas


class BasePopup:
    def __init__(self, mainCanvas: Canvas):
        from PIL import Image, ImageTk
        img = Image.open("lib/theme/popup.background")

        ImageTk.PhotoImage(img)
        self._id = mainCanvas.create_image()
