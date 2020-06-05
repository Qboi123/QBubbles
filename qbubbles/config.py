import dill


class Reader(object):
    def __init__(self, config_file):
        self.configFile = config_file

        with open(config_file, "rb") as file:
            data = dill.load(file)

        # file = NZTFile(config_file, "r")
        # file.load()
        # file.close()
        self.data = data

    def get_decoded(self):
        data = self.data
        return data


class Writer(object):
    def __init__(self, config_file, obj):
        self.data = obj

        with open(config_file, "wb+") as file:
            dill.dump(config_file, file)

        # file = NZTFile(config_file, "w")
        # file.data = data
        # file.save()
        # file.close()
