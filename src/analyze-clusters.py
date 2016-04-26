import json

from sys import argv
from awesome_print import ap 

filename = argv[1]

drugs = open('../data/master-drug-list','rb').read().splitlines()
labels = json.load(open('../data/%s-matrix-kmeans-cluster-labels.json'%filename,'rb'))["3"]["labels"]


clusters = {label:[drug for i,drug in enumerate(drugs)
			if labels[i]==label] for label in set(labels)}

#json.dump(clusters, open("../data/drugs-in-each-cluster-%s.json"%filename,'wb'))

ap(clusters)
