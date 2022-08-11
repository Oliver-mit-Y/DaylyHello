import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from einträge import *

target = sys.argv[1]
ent = Eintraege('./dmps/dumpfile.json')
entry = ent.dmp_by_id(target)

# {"title": "str", "txt": "text for entry", "api": True/False,
# "api_conf":["what to access"]["in the api data"], "api_lnk": "api options",
# "img": [True/False, Image(), True/False], "qr": "data for qr code (code will be made from it)"}

# api tasks


# set up entry


# finalize

#for x, t in enumerate(ent.dump):
#    for y, d in enumerate(t['entrys']):
#        if d['id'] == target:
#            ent.dump[x]['entrys'][y] = entry
#        else:
#            pass
#ent.savedump()
