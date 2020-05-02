from typing import overload


class StoreItemCompiler(object):
    @overload
    def __init__(self, json):
        pass

    @overload
    def __init__(self, data):
        pass

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            if type(args[0]) == str:
                _json = args[0]
                self.type = str

                import json
                data = {"StoreItems": json.JSONDecoder().decode(_json)}

                from qbubbles import nzt
                import os
                os.remove("assets/store_data.nzt")
                file = nzt.NZTFile("assets/store_data.nzt", "w")
                file.data = data
                file.save()
                file.close()
                self.data = data
                self.file = "assets/store_data.nzt"
                self.mode = "w"
            elif type(args[0]) == dict:
                data = args[0]
                self.type = dict

                from qbubbles import nzt
                import os
                os.remove("assets/store_data.nzt")
                file = nzt.NZTFile("assets/store_data.nzt", "w")
                file.data = data
                file.save()
                file.close()
                self.data = data
                self.file = "assets/store_data.nzt"
                self.mode = "w"
        elif len(kwargs.keys()) == 1:
            if "json" in kwargs.keys():
                _json = kwargs["json"]
                self.type = str

                import json
                data = {"StoreItems": json.JSONDecoder().decode(_json)}

                from qbubbles import nzt
                import os
                os.remove("assets/store_data.nzt")
                file = nzt.NZTFile("assets/store_data.nzt", "w")
                file.data = data
                file.save()
                file.close()
                self.data = data
                self.file = "assets/store_data.nzt"
                self.mode = "w"
            elif "assets" in kwargs.keys():
                data = kwargs["assets"]
                self.type = dict

                from qbubbles import nzt
                import os
                os.remove("assets/store_data.nzt")
                file = nzt.NZTFile("assets/store_data.nzt", "w")
                file.data = data
                file.save()
                file.close()
                self.data = data
                self.file = "assets/store_data.nzt"
                self.mode = "w"


if __name__ == '__main__':\
    StoreItemCompiler(json="""[
  {"coins": 5, "diamonds": 4, "name": "Level-up", "icon": "assets/Key.png"},
  {"coins": 0, "diamonds": 5, "name": "Teleport", "icon": ""},
  {"coins": 0, "diamonds": 2, "name": "Protection", "icon": "assets/Protect.png"},
  {"coins": 20, "diamonds": 0, "name": "Diamond", "icon": "assets/DiamondBuy.png"},
  {"coins": 7, "diamonds": 0, "name": "Koop een Taart", "icon": ""},
  {"coins": 5, "diamonds": 1, "name": "Pop 3 Bubbles", "icon": "assets/Pop_3_bubs.png"},
  {"coins": 2, "diamonds": 1, "name": "+2 Lifes", "icon": ""},
  {"coins": 5, "diamonds": 0, "name": "Speed Boost", "icon": "assets/Images/StoreItems/SpeedBoost.png"},
  {"coins": 5, "diamonds": 12, "name": "Ultra Mode!", "icon": "assets/Images/StoreItems/SpecialMode.png"},
  {"coins": 5, "diamonds": 0, "name": "Double Score", "icon": ""},
  {"coins": 1, "diamonds": 0, "name": "+10 Points", "icon": ""},
  {"coins": 10, "diamonds": 0, "name": "+100 Points", "icon": ""},
  {"coins": 19, "diamonds": 0, "name": "+200 Points", "icon": ""},
  {"coins": 5, "diamonds": 2, "name": "+500 Points", "icon": ""}
]""")
