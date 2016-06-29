import json
from awesome_print import ap 

READ = 'rb'
drugs = open('../data/drugs-that-actually-occurr',READ).read().splitlines()
db =  json.load(open('../data/db.json',READ))

corpus = []
for drug in drugs:
	entry = []
	for document in db.itervalues():
		if drug in document['drugs']:
			entry.extend(document['processed_text'])
	corpus.append(' '.join(entry))

with open('../data/corpus','wb') as fid:
	for document in corpus:
		print>>fid,document