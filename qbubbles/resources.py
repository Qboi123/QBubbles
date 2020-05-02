import io
import json
import os
import tkinter as tk
from typing import List, Union, Optional, Dict

import PIL
import yaml
from PIL import ImageTk, Image
from qbubbles.lib import utils

from qbubbles.gameIO import printerr


class Resources(object):
    _assetsPath: Optional[str] = None
    supportedImages = [".png", ".gif"]
    _tkImgs = [".png", ".gif"]
    _files: List[str] = []
    _images: Dict[str, Union[tk.PhotoImage, ImageTk.PhotoImage]] = []

    def __init__(self, path: Union[str, List[str]] = "assets/"):
        Resources._assetsPath = path
        Resources._files = []
        Resources._images = []
        Resources.index()

    @classmethod
    def _recursion_index(cls, path, depth=10):
        items = os.listdir(path)
        ret = []
        for item in items:
            i_abspath = os.path.join(path, item).replace("\\", "/")
            if (os.path.isdir(i_abspath)) and (depth > 0):
                ret.extend(cls._recursion_index(i_abspath, depth - 1))
            elif os.path.isfile(i_abspath):
                ret.append(i_abspath)
            else:
                pass
        return ret

    @classmethod
    def index(cls):
        if type(cls._assetsPath) == str:
            cls._files = cls._recursion_index(cls._assetsPath)
        elif type(cls._assetsPath) == list:
            cls._files = []
            for path in cls._assetsPath:
                cls._files.extend(cls._recursion_index(path))
        for file in cls._files:
            f_ext = os.path.splitext(file)[-1]
            if f_ext in cls.supportedImages:
                if f_ext in cls._tkImgs:
                    cls._images[file] = tk.PhotoImage(file=file)

    @classmethod
    def get_resource(cls, path, mode="r"):
        path = path.replace("\\", "/")
        abspath = os.path.join("assets", path).replace("\\", "/")
        if "w" in mode:
            raise ValueError("write mode is not supported for resources")
        if mode == "r+":
            raise ValueError("write mode is not supported for resources")
        if mode == "r+b":
            raise ValueError("write mode is not supported for resources")
        if abspath in cls._files:
            with open(abspath, mode) as file:
                data = file.read()
            return data
        elif not os.path.exists(abspath):
            raise TypeError("the specified assets path don't exists")
        elif os.path.isdir(abspath):
            raise TypeError("the assets path is a directory, wich is not supported as resource")
        elif os.path.exists(abspath):
            raise TypeError("the specified assets path isn't indexed")
        else:
            raise RuntimeError("an unkown problem occourd when getting the resource")

    @classmethod
    def get_imagefrom_data(cls, data, filename):
        if filename is not None:
            if filename.lower().endswith(".jpg"):
                dataEnc = io.BytesIO(data)
                img = Image.open(dataEnc)
            elif filename.lower().endswith(".png"):
                dataEnc = io.BytesIO(data)
                img = Image.open(dataEnc)
            else:
                dataEnc = io.BytesIO(data)
                img = Image.open(dataEnc)
        else:
            img = Image.frombytes("RGBA", len(data), data, decoder_name="raw")
        return ImageTk.PhotoImage(img)

    @classmethod
    def get_image(cls, path):
        abspath = os.path.join("assets", path).replace("\\", "/")
        image: Optional[Union[tk.PhotoImage, ImageTk.PhotoImage]] = cls._images.get(abspath, None)

        if image is not None:
            return image
        elif not os.path.exists(abspath):
            raise TypeError("the specified assets path don't exists")
        elif os.path.isdir(abspath):
            raise TypeError("the assets path is a directory, wich is not supported as resource")
        elif os.path.exists(abspath):
            raise TypeError("the specified assets path isn't indexed")
        else:
            raise RuntimeError("an unkown problem occourd when getting the resource")


class ModelLoader(object):
    assetsPath = "assets/"

    def __init__(self):
        pass

    def generate_bubble_images(self, min_size, max_size, config):
        images = {}
        for radius in range(min_size, max_size+1):
            colors = config["Colors"]
            images[radius] = utils.createbubble_image((radius, radius), None, *colors)
        return images

    def load_models(self, model_type):
        models = {}
        
        path = f"{self.assetsPath}/textureconfig/{model_type}"

        if not os.path.exists(path):
            raise FileNotFoundError(f"Path '{path}' does not exist")

        for model in os.listdir(path):
            if model.count(".") > 1:
                raise NameError(f"Model name '{model}' contains multiple dots, but only one is allowed "
                                f"(for the file-extension)")
            modelpath = os.path.join(path, model)
            if model.endswith(".yml"):
                with open(os.path.join(path, model), 'r') as file:
                    models[os.path.splitext(model)[0]] = yaml.safe_load(file.read())
            elif model.endswith(".json"):
                with open(os.path.join(path, model), 'r') as file:
                    models[os.path.splitext(model)[0]] = json.loads(file.read())
            else:
                if model.count(".") == 0:
                    printerr(f"Skipping model file '{modelpath}' because it has no file extension")
                    continue
                printerr(f"Skipping model file '{modelpath}' because it has an unknown file extension: {os.path.splitext(model)[1]}")
        return models
