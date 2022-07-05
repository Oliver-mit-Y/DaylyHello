import json
import os.path
import string
import random
from PIL import Image

placeholders = ["new daylytea entry", "new notes entry", "new upcoming entry", "new weather entry", "new space entry",
                "new crypto entry", "new mails entry"]


def ent_to_str(ent):
    ausgabe = f"{str(ent['title'])} \n\n{str(ent['txt'])}"
    return ausgabe


class Eintraege:
    daylytea = 0
    notes = 1
    upcoming = 2
    weather = 3
    space = 4
    crypto = 5
    mails = 6

    def __init__(self, dump_location):
        self.dumpsterpath = str(dump_location)
        if os.path.isfile(self.dumpsterpath):
            with open(self.dumpsterpath, 'r') as file:
                self.dump = json.load(file)
                file.close()
        else:
            # Basic dumb structure
            # meaning of diffrent lists in dumblist
            # 0 = "DaylyTea" entrys -- Random Sachen einfach
            # 1 = "Notes" entrys
            # 2 = "Upcoming" entrys -- Termine aufschreiben
            # 3 = "Weather" entrys -- basically ein Platz, um die Wetter-API Einträge reinzumachen
            # 4 = "Space" entrys -- Später kommen so Module mit support für Zeugs wie Nasas 'APOD'
            # 5 = "Crypto" entrys -- Platz für Einträge die mit dem Crypto Modul zusammenarbeite, dass später noch kommt
            # 6 = "Mails" entrys
            # Basic Entry Structure
            # {"title": "str", "txt": "text for entry", "api": True/False,
            # "api_conf":["what to access"]["in the api data"], "api_lnk": "link.to.api.org",
            # "img": [True/False, Image()]], "qr": "data for qr code (code will be made from it)"}
            dump_dummy = [[], [], [], [], [], [], []]
            with open(self.dumpsterpath, 'w') as file:
                json.dump(dump_dummy, file)
                file.close()
            with open(self.dumpsterpath, 'r') as file:
                self.dump = json.load(file)
                file.close()

    @staticmethod
    def generate_id():
        chars = string.ascii_lowercase
        rnd_id = '#' + ''.join(random.choice(chars) for i in range(20))
        return rnd_id

    def new_entry(self, typ, title="title", txt="placeholder",
                  api=0, api_conf=None, api_lnk="", img=None, qr=0, qrd=""):
        if img is None:
            img = (0, "path/to/image", 0)
        if api_conf is None:
            api_conf = ["empty"]
        dmp_id = self.generate_id()
        ent = {"title": title, "txt": txt, "api": api, "api_conf": api_conf, "api_lnk": api_lnk, "img": img, "qr": qr,
               "qr_data": qrd, "id": dmp_id}
        self.dump[typ].append(ent)

    def savedump(self):
        with open(self.dumpsterpath, 'w') as file:
            json.dump(self.dump, file)
            file.close()

    def reloaddump(self):
        if os.path.isfile(self.dumpsterpath):
            with open(self.dumpsterpath, 'r') as file:
                self.dump = json.load(file)
                file.close()

    def dmp_by_id(self, dmp_id):
        for i, t in enumerate(self.dump):
            for n, d in enumerate(t):
                if d['id'] == dmp_id:
                    return self.dump[i][n]

    def printdump(self):
        print(self.dump)
