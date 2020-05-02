from tkinter import Frame, Canvas

from typing import Optional

from qbubbles.exceptions import SceneNotFoundError
from qbubbles.registry import Registry


class SceneManager(object):
    def __init__(self):
        self._scenes = {}
        self.currentScene: Optional[Scene] = None
        self.currentSceneName: Optional[str] = None

    def change_scene(self, name, *args, **kwargs):
        if not Registry.scene_exists(name):
            raise SceneNotFoundError(f"scene '{name}' not existent")

        # Hide old scene first
        if self.currentScene is not None:
            self.currentScene.hide_scene()

        # Get new scene and show it
        new_scene = Registry.get_scene(name)
        self.currentSceneName = name
        self.currentScene: Scene = new_scene
        self.currentScene.show_scene(*args, **kwargs)


class Scene(object):
    scenemanager = SceneManager()

    def __init__(self, root):
        self.frame = Frame(root)

    def hide_scene(self):
        self.frame.pack_forget()

    def show_scene(self, *args, **kwargs):
        self.frame.pack(fill="both", expand=True)

    def start_scene(self):
        pass

    def update(self):
        pass

    def tick_update(self):
        pass

    def __repr__(self):
        return f"SceneObject<{self.__class__.__name__}>"


class CanvasScene(Scene):
    def __init__(self, root):
        super(CanvasScene, self).__init__(root)
        self.canvas = Canvas(self.frame, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

    def __repr__(self):
        return super(CanvasScene, self).__repr__()
