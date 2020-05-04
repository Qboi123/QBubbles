import inspect
from tkinter import Tk, PhotoImage, Toplevel
from typing import Callable, Type, List, Union, Dict

from PIL import ImageTk
from overload import overload

from qbubbles.exceptions import UnlocalizedNameError, DuplicateAddonError
from qbubbles.gameIO import printerr, printwrn


class Registry(object):
    saveConfig = {}
    saveData = {}
    gameConfig = {}
    gameData = {}

    _registryAbilities = {}
    _registryGameMaps = {}
    _registryEffects = {}
    _registryScenes = {}
    _registrySceneManager = None
    _registryModes = {}
    _registryModeManager = None
    _registryBubbles = {}
    _registrySprites = {}
    _registryKeyBinds = {}
    _registryXboxBinds = {}
    _registryImages = {}
    _registryForegrounds = {}
    _registryBackgrounds = {}
    _registryIcons = {}
    _registryStoreIcons = {}
    _registryBubResources = {}
    _registryDefaultTextures = {}
    _registryTextures = {}
    _registryMods = {}
    _registryRoot: Dict[str, Union[Tk, Toplevel]] = {}

    @classmethod
    def get_abilities(cls):
        return [ability for ability in cls._registryAbilities.values()]

    @classmethod
    def ability_exists(cls, uname):
        return uname in cls._registryAbilities.keys()

    @classmethod
    def register_ability(cls, uname, ability):
        if type(uname) != str:
            raise TypeError(f"Ability uname must be a str-object not "
                            f"{'an' if uname.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                            f"{uname.__class__.__name__}-object")
        cls._registryAbilities[uname] = ability

    @classmethod
    def get_sprites(cls):
        return [sprite for sprite in cls._registrySprites.values()]
    
    @classmethod
    def sprite_exists(cls, sname):
        return sname in cls._registrySprites.keys()
    
    @classmethod
    def register_sprite(cls, sname, sprite):
        if type(sname) != str:
            raise TypeError(f"Sprite sname must be a str-object not "
                            f"{'an' if sname.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                            f"{sname.__class__.__name__}-object")
        cls._registrySprites[sname] = sprite

    @classmethod
    def get_gamemap(cls, uname):
        return cls._registryGameMaps[uname]

    @classmethod
    def get_gamemaps(cls):
        return [uname for uname in cls._registryGameMaps.keys()]
    
    @classmethod
    def get_gamemap_objects(cls):
        return [gamemap for gamemap in cls._registryGameMaps.values()]
    
    @classmethod
    def gamemap_exists(cls, uname):
        return uname in cls._registryGameMaps.keys()

    @classmethod
    def register_gamemap(cls, uname, gamemap):
        if type(uname) != str:
            raise TypeError(f"GameMap uname must be a str-object not "
                            f"{'an' if uname.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                            f"{uname.__class__.__name__}-object")
        # printerr(f"{repr(gamemap)} is not a GameMap Representaion")
        if not (repr(gamemap).startswith("GameMap<") and repr(gamemap).endswith(">")):
            raise ValueError(f"Representation is not of a GameMap-object, or is this not a subclass of a GameMap-object?")
        cls._registryGameMaps[uname] = gamemap

    @classmethod
    def get_effect(cls, uname):
        return cls._registryEffects[uname]

    @classmethod
    def effect_exists(cls, uname):
        return uname in cls._registryEffects.keys()
    
    @classmethod
    def register_effect(cls, uname, effect):
        if type(uname) != str:
            raise TypeError(f"Effect uname must be a str-object not "
                             f"{'an' if uname.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                             f"{uname.__class__.__name__}-object")
        # printerr(f"{repr(effect)} is not a EffectObject Representaion")
        if not (repr(effect).startswith("EffectObject(<") and repr(effect).endswith(">)")):
            raise ValueError(f"Representation is not of a Effect-object, or is this not a subclass of a Effect-object?")
        cls._registryEffects[uname] = effect
        
    @classmethod
    def get_scene(cls, name):
        return cls._registryScenes[name]

    @classmethod
    def scene_exists(cls, name):
        return name in cls._registryScenes.keys()

    @classmethod
    def get_mode(cls, name):
        return cls._registryModes[name]

    @classmethod
    def mode_exists(cls, name):
        return name in cls._registryModes.keys()

    @classmethod
    def get_bubble(cls, id):
        return cls._registryBubbles[id]

    @classmethod
    def get_keybinding(cls, key):
        return cls._registryKeyBinds[key]

    @classmethod
    def get_xboxbinding(cls, key):
        return cls._registryXboxBinds[key]

    @classmethod
    def get_window(cls, name: str) -> Union[Tk, Toplevel]:
        return cls._registryRoot[name]

    @classmethod
    def get_id_bubble(cls, bubble) -> List[str]:
        return [key for key, value in cls._registryBubbles if value == bubble]

    @classmethod
    def register_scene(cls, name: str, scene: Type[Callable]):
        if type(name) != str:
            raise TypeError(f"Scene name must be a str-object not "
                             f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                             f"{name.__class__.__name__}-object")
        # printerr(f"{repr(scene)} is not a SceneObject Representaion")
        if not (repr(scene).startswith("SceneObject<") and repr(scene).endswith(">")):
            raise ValueError(f"Representation is not of a Scene-object, or is this not a subclass of a Scene-object?")
        cls._registryScenes[name] = scene

    @classmethod
    def register_mode(cls, name: str, mode: object):
        if type(name) != str:
            raise TypeError(f"Mode name must be a str-object not "
                            f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                            f"{name.__class__.__name__}-object")
        if not (repr(mode).startswith("ModeObject<") and repr(mode).endswith(">")):
            raise ValueError(f"Representation is not of a Mode-object, or is this not a subclass of a Mode-object?")
        cls._registryModes[name] = mode

    @classmethod
    def register_bubble(cls, id_: str, bubbleobj: object):
        if type(id_) != str:
            raise TypeError(f"Bubble ID must be a str-object not "
                             f"{'an' if id_.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                             f"{id_.__class__.__name__}-object")
        if not (repr(bubbleobj).startswith("Bubble(<") and repr(bubbleobj).endswith(">)")):
            raise ValueError(f"Representation is not of a Bubble-object, or is this not a subclass of a Bubble-object?")
        cls._registryBubbles[id_] = bubbleobj

    @classmethod
    def register_keybinding(cls, key: str, command: Callable):
        if type(key) != str:
            raise TypeError(f"Key-binding must be a str-object not "
                             f"{'an' if key.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                             f"{key.__class__.__name__}-object")

        if key in cls._registryXboxBinds:
            printerr(f"Key-binding with key '{key}' already exists!")
        cls._registryKeyBinds[key] = command

    @classmethod
    def register_xboxbinding(cls, key: str, command: Callable):
        if type(key) != str:
            raise TypeError(
                f"Xbox-binding must be a str-object not "
                f"{'an' if key.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{key.__class__.__name__}-object")

        if key in cls._registryXboxBinds:
            printerr(f"Xbox-binding with key '{key}' already exists!")
        cls._registryXboxBinds[key] = command

    @classmethod
    def register_window(cls, name, window):
        if not issubclass(type(window), Tk):
            if not issubclass(type(window), Toplevel):
                raise TypeError(
                    f"Window must be a subclass of Tk(...) or Toplevel(...) not "
                    f"{'an' if window.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{window.__class__.__name__}-object, wich is not subclass of it")

        if name in cls._registryRoot.keys():
            printerr(f"Window with name '{name}' already exists!")
        cls._registryRoot[name] = window

    @classmethod
    def register_image(cls, name, image: PhotoImage, **data):
        if type(name) != str:
            raise TypeError(
                f"Image name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{name.__class__.__name__}-object")
        if type(image) != PhotoImage:
            if type(image) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Image must be a PhotoImage-object not "
                    f"{'an' if image.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{image.__class__.__name__}-object")

        if name in cls._registryImages.keys():
            printerr(f"Image with name '{name}' already exists!")
        cls._registryImages[name] = {}
        cls._registryImages[name][tuple(data.items())] = image

    @classmethod
    def get_image(cls, name):
        if name not in cls._registryImages.keys():
            raise UnlocalizedNameError(f"image with name '{name}' is non-existent")
        icon = cls._registryImages[name]
        return icon

    @classmethod
    def register_foreground(cls, name, image: PhotoImage):
        if type(name) != str:
            raise TypeError(
                f"Foreground name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{name.__class__.__name__}-object")
        if type(image) != PhotoImage:
            if type(image) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Foreground image must be a PhotoImage-object not "
                    f"{'an' if image.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{image.__class__.__name__}-object")

        if name in cls._registryXboxBinds:
            printerr(f"Foreground with name '{name}' already exists!")
        cls._registryForegrounds[name] = image

    @classmethod
    def get_foreground(cls, name):
        if name not in cls._registryForegrounds.keys():
            raise UnlocalizedNameError(f"foreground with name '{name}' is non-existent")
        icon = cls._registryForegrounds[name]
        return icon

    @classmethod
    def register_background(cls, name, image: PhotoImage):
        if type(name) != str:
            raise TypeError(
                f"Background name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{name.__class__.__name__}-object")
        if type(image) != PhotoImage:
            if type(image) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Background image must be a PhotoImage-object not "
                    f"{'an' if image.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{image.__class__.__name__}-object")

        if name in cls._registryXboxBinds:
            printerr(f"Image with name '{name}' already exists!")
        cls._registryBackgrounds[name] = image

    @classmethod
    def get_background(cls, name):
        if name not in cls._registryBackgrounds.keys():
            raise UnlocalizedNameError(f"background with name '{name}' is non-existent")
        icon = cls._registryBackgrounds[name]
        return icon

    @classmethod
    def register_storeitem(cls, name, icon: PhotoImage, obj: Callable = None):
        if type(name) != str:
            raise TypeError(
                f"Store item name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{name.__class__.__name__}-object")
        if type(icon) != PhotoImage:
            if type(icon) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Store item icon must be a PhotoImage-object not "
                    f"{'an' if icon.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{icon.__class__.__name__}-object")

        # # TODO: Make store item objects compatible
        # # printerr(f"{repr(scene)} is not a SceneObject Representaion")
        # if not (repr(obj).startswith("StoreItem<") and repr(obj).endswith(">")):
        #     raise ValueError(f"Representation is not of a StoreItem-object, or is this not a subclass of a Scene-object?")
        if name in cls._registryXboxBinds:
            printerr(f"Store item icon with name '{name}' already exists!")
        cls._registryStoreIcons[name] = icon

    @classmethod
    def register_icon(cls, name, image: PhotoImage):
        if type(name) != str:
            raise TypeError(
                f"Icon name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{name.__class__.__name__}-object")
        if type(image) != PhotoImage:
            if type(image) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Icon image must be a PhotoImage-object not "
                    f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{image.__class__.__name__}-object")

        if name in cls._registryXboxBinds:
            printerr(f"Ìcon with name '{name}' already exists!")
        cls._registryIcons[name] = image

    @classmethod
    def get_icon(cls, name):
        if name not in cls._registryIcons.keys():
            raise NameError(f"icon with name '{name}' is non-existent")
        icon = cls._registryIcons[name]
        return icon

    @classmethod
    def get_bubresource(cls, uname, key):
        if uname not in cls._registryBubResources.keys():
            raise UnlocalizedNameError(f"bubble resource with uname '{uname}' is non-existent")
        bub_reslist = cls._registryBubResources[uname]
        if key not in bub_reslist.keys():
            raise KeyError(f"key '{key}' for bubble resource '{uname}' is non-existent")
        bub_res = bub_reslist[key]
        return bub_res


    @classmethod
    def bubresource_exists(cls, uname, key=None):
        if uname in cls._registryBubResources.keys():
            if key is not None:
                return key in cls._registryBubResources[uname].keys()
            return True
        return False

    @classmethod
    def register_bubresource(cls, uname, key, value):
        if type(uname) != str:
            raise TypeError(
                f"uname for bubble resource must be a str-object not "
                f"{'an' if uname.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{uname.__class__.__name__}-object")
        if type(key) != str:
            raise TypeError(
                f"key for bubble resource must be a str-object not "
                f"{'an' if key.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{key.__class__.__name__}-object")

        if uname in cls._registryBubResources.keys():
            if key in cls._registryBubResources[uname].keys():
                printwrn(f"bubble resource key '{key}' with uname '{uname}' is overridden, this can be a intended override, "
                         f"but usually a mistake")
            cls._registryBubResources[uname][key] = value
        else:
            cls._registryBubResources[uname] = {key: value}

    @classmethod
    def get_dtexture(cls, type_, id_) -> Union[PhotoImage, ImageTk.PhotoImage]:
        # if "qbubbles:default" not in cls._registryDefaultTextures.keys():
        #     raise RuntimeError("Missing type 'qbubbles:default'")
        if type_ not in cls._registryDefaultTextures.keys():
            # cls.get_scenemanager().change_scene("qbubbles:ErrorScene",
            #                                     f"Game Crashed",
            #                                     f"Missing default texture for type '{type_}'")
            raise RuntimeError(f"Missing default texture for type '{type_}'")
        if id_ not in cls._registryDefaultTextures[type_].keys():
            return cls._registryDefaultTextures[type_][None]
        return cls._registryDefaultTextures[type_][id_]

    @classmethod
    def register_default_texture(cls, type_: str, id_: str = None, *, texture):
        if id_ is None:
            if type_ not in cls._registryDefaultTextures.keys():
                cls._registryDefaultTextures[type_] = {}
            else:
                printwrn(f"Default texture of type '{type_}' has been overridden")
            cls._registryDefaultTextures[type_][None] = texture
        else:
            if type_ not in cls._registryDefaultTextures.keys():
                raise RuntimeError(f"There is no default texture registered for type '{type_}'")
            if id_ in cls._registryDefaultTextures[type_].keys():
                printwrn(f"Default texture for type '{type_}' with id '{id_}' has been overridden")
            cls._registryDefaultTextures[type_][id_] = texture

    @classmethod
    def get_texture(cls, type_, id_, **data) -> Union[PhotoImage, ImageTk.PhotoImage]:
        if type_ not in cls._registryTextures.keys():
            printerr(f"Type '{type_}' is not found in texture registry")
            return cls.get_dtexture(type_, id_)
        if id_ not in cls._registryTextures[type_].keys():
            printerr(f"ID '{id_}' with type '{type_}' is not found in texture registry")
            return cls.get_dtexture(type_, id_)
        if tuple(data.items()) not in cls._registryTextures[type_][id_]:
            printerr(f"ID '{id_}' with type '{type_}' and data '{dict(data)}' is not found in texture registry")
            return cls.get_dtexture(type_, id_)
        return cls._registryTextures[type_][id_][tuple(data.items())]

    @classmethod
    def get_current_scene(cls):
        return cls.get_scene("Game").scenemanager.currentScene

    @classmethod
    def get_scenemanager(cls):
        return cls.get_scene("Game").scenemanager

    @classmethod
    def register_scenemanager(cls, scenemanager):
        if cls._registrySceneManager is not None:
            raise RuntimeError("scenemanager already registered")
        cls._registrySceneManager = scenemanager
    
    @classmethod
    def register_texture(cls, type_, id_, texture, **data):
        if type(type_) != str:
            raise TypeError(
                f"Texture type must be a str-object not "
                f"{'an' if type_.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{type_.__class__.__name__}-object")
        if type(id_) != str:
            raise TypeError(
                f"Texture ID must be a str-object not "
                f"{'an' if id_.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{id_.__class__.__name__}-object")
        if type(texture) != PhotoImage:
            if type(texture) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Image must be a PhotoImage-object not "
                    f"{'an' if texture.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{texture.__class__.__name__}-object")

        if type_ in cls._registryTextures.keys():
            if id_ in cls._registryTextures[type_].keys():
                if tuple(data.items()) in cls._registryTextures[type_][id_]:
                    printwrn(f"texture with ID '{id_}' and type '{type_}' is overridden, this can be a intended override, "
                             f"but usually a mistake")
                cls._registryTextures[type_][id_][tuple(data.items())] = texture
            else:
                # cls._registryTextures[type_][id_] = texture
                cls._registryTextures[type_][id_] = {}
                cls._registryTextures[type_][id_][tuple(data.items())] = texture
        else:
            cls._registryTextures[type_] = {id_: {tuple(data.items()): texture}}

    @classmethod
    def get_bubbles(cls):
        return tuple(cls._registryBubbles.values())

    @classmethod
    def get_lname(cls, *args):
        l_id = ".".join([*args])
        if l_id in cls.gameData["language"].keys():
            return cls.gameData["language"][l_id]
        else:
            return l_id

    @classmethod
    def register_sprite_image(cls, name, image, **data):
        pass

    @classmethod
    def register_modobject(cls, modid: str, name: str, version: str, func: object):
        # print(modid, name, version, func)
        if modid in cls._registryMods.keys():
            path = inspect.getfile(func)
            raise DuplicateAddonError(modid, name, version, path, func)
        cls._registryMods[modid] = dict(name=name, version=version, addon=func)

    @classmethod
    def get_all_addons(cls):
        return [modid for modid in cls._registryMods.keys()]

    @classmethod
    def mod_exists(cls, modid, version=None):
        if version is not None:
            if modid in cls._registryMods.keys():
                if version.split(".") in cls._registryMods[modid]["version"].split("."):
                    return True
            return False
        return modid in cls._registryMods.keys()

    @classmethod
    def get_module(cls, modid):
        return cls._registryMods[modid]

    @classmethod
    def get_sprite(cls, uname):
        return cls._registrySprites[uname]
