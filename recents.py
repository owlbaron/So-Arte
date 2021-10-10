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
        recents = list(filter(lambda r: (
                r["type"] != recent["type"] or
                r["name"] != recent["name"] or
                r["param"] != recent["param"]
        ), recents))

        recents.insert(0, recent)

        data = recents[0:9]

        with open('recents.json', 'w') as outfile:
            json.dump(data, outfile)
