import json, os

db = {}
WRITE = 'wb'

for filename in os.listdir(os.path.join(os.getcwd(),'forums'))[:2]:
	db['text'] = open(os.path.join(os.getcwd(),'forums',filename)).read()

json.dump(db,open('db.json',WRITE))
