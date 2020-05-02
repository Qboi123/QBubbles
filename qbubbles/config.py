from qbubbles.nzt import NZTFile


class Reader(object):
    def __init__(self, config_file):
        self.configFile = config_file

        file = NZTFile(config_file, "r")
        file.load()
        file.close()
        self.data = file.data

    def get_decoded(self):
        data = self.data
        return data


class Writer(object):
    def __init__(self, config_file, obj):
        self.data = data = obj

        file = NZTFile(config_file, "w")
        file.data = data
        file.save()
        file.close()
