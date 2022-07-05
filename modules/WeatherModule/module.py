import sys, os
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from einträge import *
from PIL import Image
from io import BytesIO

target = sys.argv[1]
city = sys.argv[2]
target_clean = target.replace('#', '')
ent = Eintraege('./dmps/dumpfile.json')
entry = ent.dmp_by_id(target)


# {"title": "str", "txt": "text for entry", "api": True/False,
# "api_conf":'module file' , "api_lnk": "link.to.api.org",
# "img": (0, path/to/image, 0), "qr": 0
# "qr_data":"data for qr code", "id":"#rndid"}

# api tasks

here_path = os.path.dirname(__file__)
keyfile = open(f'{here_path}//api-key.txt', 'r')
lines = keyfile.readlines()
key = lines[0].replace('\n', '')
citykey = lines[1].replace('\n', '')
keyfile.close()

try: 
    cityy = int(city)
    url = f"https://api.openweathermap.org/data/2.5/forecast?id={cityy}&units=metric&lang=de&appid={key}"
except Exception:
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&lang=de&appid={key}"
fdata = requests.get(url).json()
data = fdata['list'][0]


lnk = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
pic = Image.open(BytesIO(requests.get(lnk).content))
ftype = pic.format.lower()
img_pth = f'dmps/{target_clean}.{ftype}'
pic.save(img_pth)

# set up entry

iy, ip, ib = entry['img']
citycity = fdata['city']['name']
text = f"{data['weather'][0]['description']}\nTemperatur: {data['main']['temp']}°C (Gefühlt: {data['main']['feels_like']}°C)\nRegenwahrscheinlichkeit: {data['pop']}%"
entry['txt'] = text
entry['title'] = citycity.title()
entry['img'] = (1, img_pth, ib)

# finalize
backup = ent.dump
try: 
    for x, t in enumerate(ent.dump):
        for y, d in enumerate(t):
            if d['id'] == target:
                ent.dump[x][y] = entry
except Exception:
    ent.dump = backup
    print('ein Fehler ist passiert')

ent.savedump()
