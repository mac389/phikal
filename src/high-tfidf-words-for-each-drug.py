import json, itertools, csv, os 

import matplotlib.pyplot as plt 
from gensim import corpora, models, similarities

db = json.load(open('../data/db.json','rb'))
drugs = open('../data/drugs-that-actually-occurr').read().splitlines()

text = {drug: list(itertools.chain.from_iterable(item['processed_text'] 
						for item in db.itervalues() if drug in item['drugs']))
						for drug in drugs}

texts = [text[drug] for drug in drugs]
if not os.path.isfile('../data/gensim_dictionary'):
    dictionary = corpora.Dictionary(texts)
    dictionary.save('../data/gensim_dictionary.dict')
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('../data/gensim_corpus.mm', corpus)
    tfidf = models.TfidfModel(corpus)
    tfidf.save('../data/gensim_tfidf')

else:

    corpus = corpora.MmCorpus('../data/gensim_corpus')
    tfidf = models.TfidfModel.load('../data/gensim_tfidf')

corpus_tfidf = tfidf[corpus]

d = {dictionary.get(id): value for doc in corpus_tfidf for id, value in doc}
print d.keys()
print type(text) 
print d[text['lsa'][0]]
drug_tfidf = {drug:[{word:d[word]} for word in text[drug]] for drug in drugs}
json.dump(drug_tfidf,open('drug_tfidf','wb'))
