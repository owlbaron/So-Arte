import json


class Recents:
    def __init__(self):
        pass

    @staticmethod
    def read():
        with open('recents.json') as json_file:
            recents = json.load(json_file)

        return recents

    @staticmethod
    def add_new(recent):
        recents = Recents.read()

        recents.insert(0, recent)

        data = recents[0:10]

        with open('recents.json', 'w') as outfile:
            json.dump(data, outfile)


Recents.read = staticmethod(Recents.read)
Recents.add_new = staticmethod(Recents.add_new)
