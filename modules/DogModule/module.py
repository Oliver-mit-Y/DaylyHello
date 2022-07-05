import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from einträge import *
import requests
from PIL import Image
from io import BytesIO

target = sys.argv[1]
target_clean = target.replace('#', '')

ent = Eintraege('./dmps/dumpfile.json')

# {"title": "str", "txt": "text for entry", "api": True/False,
# "api_conf":["what to access"]["in the api data"], "api_lnk": "link.to.api.org",
# "img": [True/False, Image()]], "qr": "data for qr code (code will be made from it)"}

# api works   

lnk = 'https://dog.ceo/api/breeds/image/random'
pic_lnk = requests.get(lnk).json()
true_link = pic_lnk['message']
pic = Image.open(BytesIO(requests.get(true_link).content))
ftype = pic.format.lower()
img_pth = f'dmps/{target_clean}.{ftype}'
pic.save(img_pth)

# set up entry
entry = ent.dmp_by_id(target)
iy, ip, ib = entry['img']
entry['img'] = (1, img_pth, ib)
entry['qr_data'] = true_link

for x, t in enumerate(ent.dump):
    for y, d in enumerate(t):
        if d['id'] == target:
            ent.dump[x][y] = entry
ent.savedump()
