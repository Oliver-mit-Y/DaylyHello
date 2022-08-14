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


def remove_slice(lis, slic):
    new_lis = []
    for n, x in enumerate(lis):
        if n != slic:
            new_lis.append(x)

    return new_lis


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

            # dumpfile consists of diffrent cards {}
            # cards consist of "name" and "entrys"
            # "name" is a string of the name of the card 'Kartei 1'
            # "entrys" is a list with the entrys of the card []

            # Basic Entry Structure
            # {"title": "str", "txt": "text for entry", "api": 0/1,
            # "api_conf":["what to access"]["in the api data"], "api_lnk": "api options",
            # "img": [0/1, Image(), 0/1], "qr": 0/1 ,"qr_data": "data for qr code (code will be made from it)"}
            card_id = self.generate_id()
            card_id2 = self.generate_id()
            dump_dummy = [{"name": "Kartei 1", "entrys": 
                                                [{"title": "title", 
                                                  "txt": "placeholder", 
                                                  "api": 0, 
                                                  "api_conf": ["empty"], 
                                                  "api_lnk": "", 
                                                  "img": [0, "path/to/image", 0], 
                                                  "qr": 0, 
                                                  "qr_data": "", 
                                                  "id": "#inhsiwwfjcrlxmqwsvcn"}],
                            'icon': [0, 'noicon'], 'id': card_id}, 
                            {"name": "Kartei 2", "entrys": [], 'icon': [0, 'noicon'], 'id': card_id2}]
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
        self.dump[typ]['entrys'].append(ent)

    def new_card(self, name='neue_kartei'):
        card_id = self.generate_id()
        self.dump.append({'name': name, 'icon': [0, 'noicon'], 'entrys': [], 'id': card_id})

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
            for n, d in enumerate(t['entrys']):
                if d['id'] == dmp_id:
                    return self.dump[i]['entrys'][n]

    def move_card_up(self, typ):
        if typ != 0:
            new_order = []
            old_without_changed = remove_slice(self.dump, typ)
            for n, x in enumerate(self.dump):
                if n<(typ-1):
                    new_order.append(self.dump[n])
                if n == (typ-1):
                    new_order.append(self.dump[typ])
                if n>(typ-1):
                    new_order.append(old_without_changed[(n-1)])
            self.dump = new_order

    def move_card_down(self, typ):
        if typ != len(self.dump)-1:
            self.dump = self.dump[::-1]
            typ = len(self.dump)-typ-1
            new_order = []
            old_without_changed = remove_slice(self.dump, typ)
            for n, x in enumerate(self.dump):
                if n<(typ-1):
                    new_order.append(self.dump[n])
                if n == (typ-1):
                    new_order.append(self.dump[typ])
                if n>(typ-1):
                    new_order.append(old_without_changed[(n-1)])
            self.dump = new_order
            self.dump = self.dump[::-1]

    def move_ent_down(self, id):
        tt = 0
        ee = 0
        s = 'entrys'
        for n, ty in enumerate(self.dump):
            for m, en in enumerate(ty['entrys']):
                if en['id'] == id:
                    tt = n
                    ee = m
                    break

        if ee != len(self.dump[tt][s])-1:
            self.dump[tt][s] = self.dump[tt][s][::-1]
            ee = len(self.dump[tt][s])-ee-1
            new_order = []
            old_without_changed = remove_slice(self.dump[tt][s], ee)

            for n, x in enumerate(self.dump[tt][s]):
                if n<(ee-1):
                    new_order.append(self.dump[tt][s][n])
                if n == (ee-1):
                    new_order.append(self.dump[tt][s][ee])
                if n>(ee-1):
                    new_order.append(old_without_changed[(n-1)])

            new_order = new_order[::-1]

            self.dump[tt][s] = new_order

    def move_ent_up(self, id):
        tt = 0
        ee = 0
        s = 'entrys'
        for n, ty in enumerate(self.dump):
            for m, en in enumerate(ty['entrys']):
                if en['id'] == id:
                    tt = n
                    ee = m
                    break
       
        if ee != 0:
            new_order = []
            old_without_changed = remove_slice(self.dump[tt][s], ee)

            for n, x in enumerate(self.dump[tt][s]):
                if n<(ee-1):
                    new_order.append(self.dump[tt][s][n])
                if n == (ee-1):
                    new_order.append(self.dump[tt][s][ee])
                if n>(ee-1):
                    new_order.append(old_without_changed[(n-1)])
            self.dump[tt][s] = new_order


    def printdump(self):
        print(self.dump)
