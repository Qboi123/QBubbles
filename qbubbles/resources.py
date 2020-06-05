import io
import json
import os
import sys
import tkinter as tk
from typing import List, Union, Optional, Dict

import PIL
import yaml
from PIL import ImageTk, Image

from qbubbles.globals import GAME_VERSION
from qbubbles.lib import utils

from qbubbles.gameIO import printerr, Logging
from qbubbles.lib.utils import Translate
from qbubbles.registry import Registry


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


def languagereader(langid):
    with io.open(f"lang/{langid}.yaml", "r", encoding="utf-8") as file:
        lang = yaml.safe_load(file.read())
    return lang


def language_genrator(langid):
    languages = {"nl": "Dutch", "en": "English", "de": "Deutch", "es": "Spanish", "fr": "French", "it": "Italian",
                 "fy": "Frysk", "jp": "Japanese", "zh": "Chinese", "pt": "Portuguese", "pl": "Polish", "hi": "Hindi",
                 "ar": "Arabic", "af": "Afrikaans", "hu": "Hungarian", "ru": "Russian", "mt": "Maltese",
                 "sq": "Albanian", "am": "Amharic", "hy": "Armenian", "az": "Azerbaijani", "eu": "Basque",
                 "bn": "Bengali", "my": "Burmeese", "bs": "Bosnian", "bg": "Bulgarian", "ca": "Catalan",
                 "ceb": "Cebuanian", "ny": "Chichewese", "zh-TW": "Chinese (Traditional)",
                 "zh-CN": "Chinese (Simplified)", "co": "Corsican", "da": "Danish", "eo": "Esperanto", "et": "Estonian",
                 "fi": "Finnish", "gl": "Galician", "ka": "Georgian", "el": "Greek", "ig": "Igbo", "is": "Icelandic",
                 "id": "Indonesian", "jw": "Javanese", "yi": "Yiddish", "kn": "Kannada", "kk": "Kazakh", "km": "Khmer",
                 "rw": "Kinyarwanda", "ky": "Kyrgyz", "ku": "Kurdish", "ko": "Korean", "hr": "Croatian", "lo": "Lao",
                 "la": "Latin", "lv": "Latvian", "lt": "Lithuanian", "hmn": "Hmong", "iw": "Hebrew", "haw": "Hawaiian",
                 "ha": "Hausa", "ht": "Haitian Creole", "gu": "Gujarati", "lb": "Luxembourgish", "mk": "Macedonian",
                 "mg": "Malagasy", "ml": "Malayalam", "ms": "Malay", "mi": "Maori", "mr": "Marathi", "mn": "Mongolian",
                 "ne": "Nepalese", "no": "Norwegian", "or": "Odia", "ug": "Uyghurs", "uk": "Ukrainian", "uz": "Uzbek",
                 "ps": "Pashto", "fa": "Persian", "pa": "Punjabi", "ro": "Romanian", "sm": "Samoan",
                 "gd": "Scottish Celtic", "sr": "Serbian", "st": "Seshoto", "sn": "Shona", "sd": "Sindhi",
                 "si": "Sinhala", "sk": "Slovak", "sl": "Slovenian", "su": "Sundanese", "so": "Somali", "sw": "Swahili",
                 "tg": "Tajik", "tl": "Tagalog", "ta": "Tamil", "tt": "Tatar", "te": "Telugu", "th": "Thai",
                 "cs": "Czech", "tk": "Turkmen", "tr": "Turkish", "ur": "Urdu", "vi": "Vietnamese", "cy": "Welsh",
                 "be": "Belarusian", "xh": "Xhosa", "yo": "Yoruba", "zu": "Zulu", "sv": "Swedish"}

    if langid is not None:
        lang = languagereader("en")
        langout = {}

        trans = Translate("en", langid)
        for key, value in lang.items():
            langout[key] = trans.translate(value)
        langout["options.name"] = trans.translate(languages[langid]) + " " + languages[langid]

        return langout
    else:
        gtrans_path = os.path.join(Registry.gameData['launcherConfig']['gameDir'], "data", GAME_VERSION, "gtrans")
        if not os.path.exists(gtrans_path):
            os.makedirs(gtrans_path)
        for langid, name in languages.items():
            Logging.info("LanguageGenerator", f"Generate language id {langid}, name: {name}")

            lang = languagereader("en")
            langout = {}

            trans = Translate("en", langid)
            for key, value in lang.items():
                Logging.info("LanguageGenerator", f"Lang [{langid}]: Translating key: {key}")
                langout[key] = str(trans.translate(value))
            langout["options.name"] = trans.translate(name) + f" ({name})"

            path = os.path.join(gtrans_path, f"{langid}.yaml")

            with io.open(path, "w+", encoding="utf-8") as file:
                file.write(yaml.safe_dump(langout))
                file.close()


def languageloader_gtrans(langid):
    r"""
    Loads a Google Translated language file. From the gtrans folder.

    The ``gtrans`` folder is located at ``%DIR%\data\%VER%\gtrans\`` where ``%DIR%`` is the game directory, and
    ``%VER%`` is the game version.

    :param langid: The Google Translate language identifier.
    :returns: Tuple: A boolean indicating the gtrans folder was found, and the language data.
    """

    gtrans_path = os.path.join(Registry.gameData['launcherConfig']['gameDir'], "data", GAME_VERSION, "gtrans")
    path = os.path.join(gtrans_path, f"{langid}.yaml")

    if not os.path.exists(gtrans_path):
        return False, None
    if not os.path.exists(path):
        raise FileNotFoundError(f"Language data for {langid} not found! That's a local 404.")
    with open(path) as file:
        lang = yaml.safe_load(file.read())
        file.close()
    return True, lang


def languageloader(langid, gtrans=False):
    if gtrans is True:
        lang = languageloader_gtrans(langid)
    else:
        lang = languagereader(langid)

    Registry.gameData["language"] = lang


if __name__ == '__main__':
    def test_yamldata():
        import tempfile
        with tempfile.TemporaryFile("r+t", encoding="utf-8") as tmpfile:
            tmpfile.seek(0)
            tmpfile.write(yaml.safe_dump({"Key": "Value",
                                          "Integer": 300,
                                          "Boolean": True,
                                          "List": [300, 400, 500],
                                          "Set": {300, 400, 500},
                                          "Tuple": (300, 400, 500)}))
            tmpfile.seek(0)
            sys.stdout.write(repr(yaml.safe_load(tmpfile.read()))+"\n")
            tmpfile.seek(0)
            sys.stdout.write(tmpfile.read()+"\n")

    def generate_gtansfiles():
        Logging("..\\TestLogs\\")
        Registry.gameData['launcherConfig'] = {}
        Registry.gameData['launcherConfig']['gameDir'] = f"C:/Users/{os.getlogin()}/Desktop/QplayBubblesLanguages"
        if not os.path.exists(f"C:/Users/{os.getlogin()}/Desktop/QplayBubblesLanguages"):
            os.makedirs(f"C:/Users/{os.getlogin()}/Desktop/QplayBubblesLanguages")
        language_genrator(None)

    generate_gtansfiles()
