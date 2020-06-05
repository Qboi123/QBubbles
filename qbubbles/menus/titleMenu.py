# Python Modules
import os as _os
import sys as _sys
import tkinter as _tk

# QBubbles Modules
import qbubbles.background as _back
import qbubbles.registry as _reg
import qbubbles.scenemanager as _scenemgr
import qbubbles.utils as _utils
import qbubbles.gameIO as _gameIO
from qbubbles.events import LanguageChangeEvent
from qbubbles.scenes import get_lname


class TitleMenu(_scenemgr.Scene):
    def __init__(self):
        """
        Title-menu scene of the game.
        """

        super(TitleMenu, self).__init__(_reg.Registry.get_window("default"))

        self.lang = _reg.Registry.gameData["language"]
        self.config = _reg.Registry.gameData["config"]
        self.btnFont: _utils.Font = _reg.Registry.gameData["fonts"]["titleButtonFont"]

        # Items
        self.items = list()

        # Create background
        self.background = _back.Background(self.frame)

        # Create buttons
        self.start_btn = _tk.Button(
            self.frame, bg="#007f7f", fg="#7fffff", bd=15, command=lambda: self.play_event(),
            text=get_lname("home.start"), relief="flat", font=self.btnFont.get_tuple())
        self.quit_btn = _tk.Button(
            self.frame, bg="#007f7f", fg="#7fffff", bd=15, command=lambda: _os.kill(_os.getpid(), 0),
            text=get_lname("home.quit"), relief="flat", font=self.btnFont.get_tuple())
        self.options_btn = _tk.Button(
            self.frame, bg="#007f7f", fg="#7fffff", bd=15, command=lambda: self.options_event(),
            text=get_lname("home.options"), relief="flat", font=self.btnFont.get_tuple())

        # Place buttons on screen
        self.start_btn.place(
            x=_reg.Registry.gameData["WindowWidth"] / 2, y=_reg.Registry.gameData["WindowHeight"] / 2 - 40, width=310,
            anchor="center")
        self.quit_btn.place(
            x=_reg.Registry.gameData["WindowWidth"] / 2 + 80, y=_reg.Registry.gameData["WindowHeight"] / 2 + 40, width=150,
            anchor=_tk.CENTER)
        self.options_btn.place(
            x=_reg.Registry.gameData["WindowWidth"] / 2 - 80, y=_reg.Registry.gameData["WindowHeight"] / 2 + 40, width=150,
            anchor="center")

        # Refresh game.
        self.frame.update()

        self.loop_active = True

        LanguageChangeEvent.bind(self.on_language_change)

    def on_language_change(self, evt: LanguageChangeEvent):
        self.lang = _reg.Registry.gameData["language"]

        self.start_btn.configure(text=self.lang["home.start"])
        self.quit_btn.configure(text=self.lang["home.quit"])
        self.options_btn.configure(text=self.lang["home.options"])

    def mainloop(self):
        """
        Background mainloop method, used for animate the background.

        :return:
        """

        import time
        # Titlemenu mainloop
        self.background.canvas.update()
        end_time = time.time() + 10
        while self.loop_active:
            try:
                # Update background
                self.background.create_bubble()
                self.background.move_bubbles()
                self.background.cleanup_bubs()

                # Update window
                self.frame.update()
                self.frame.update_idletasks()

                if "--travis" in _sys.argv:
                    if time.time() > end_time:
                        _reg.Registry.get_window("default").destroy()
                        break
                        # pass
            except _tk.TclError:
                break

    def show_scene(self, *args, **kwargs):
        """
        Shows the scene.

        :param args:
        :param kwargs:
        :return:
        """

        super(TitleMenu, self).show_scene()

        _gameIO.Logging.info("TitleMenu", "Showing TitleMenu()-scene")

        self.loop_active = True
        self.mainloop()

    def hide_scene(self):
        """
        Hides the scene.

        :return:
        """

        self.loop_active = False
        super(TitleMenu, self).hide_scene()

    def play_event(self):
        """
        Play button event handler.

        :return:
        """

        self.scenemanager.change_scene("qbubbles:saves")

    def destroy(self):
        """
        Destroys the scene.

        :return:
        """

        self.options_btn.destroy()
        self.background.destroy()
        self.start_btn.destroy()
        self.quit_btn.destroy()

    def options_event(self):
        self.scenemanager.change_scene("qbubbles:options")
