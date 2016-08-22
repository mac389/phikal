import json, os

terms = ["lsd","mdma"]
db = json.load(open(os.path.join('..','data','db.json'),'rb'))

words = {term:open('../data/processed-%s'%term,'wb') for term in terms}
words["both"] = open('../data/processed-both','wb')

for entry in db.itervalues(): 
	if all([term in entry["drugs"] for term in terms]):
		for token in entry["processed_text"]:
			print>>words["both"],token
	else: #We know only one term is in the database entry
		for term in terms:
			if term in entry["drugs"]:
				for token in entry["processed_text"]:
					print>>words[term],token

for value in words.itervalues():
	value.close()

#Calculate frequency of each
from collections import Counter

descriptions = {term:dict(Counter(open('../data/processed-%s'%term,'rb').read().splitlines())) 
					for term in words.iterkeys()}

json.dump(descriptions,open('../data/descriptions.json','wb'))
