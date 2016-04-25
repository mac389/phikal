import json, nltk, string, itertools

import utils as tech

from awesome_print import ap 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from progress.bar import Bar 
'''
Consider using TextBlob 
from textblob import TextBlob as tb
from textblob_aptagger import PerceptronTagger
'''
READ = 'rb'
WRITE = 'wb'
stopwords = set(open('stopwords',READ)) | set(nltk.corpus.stopwords.words('english'))
punctuation = string.punctuation + "`'"
contraction_expansion = json.load(open('contraction-expansion.json',READ))
lmtzr = WordNetLemmatizer()
db = json.load(open('db.json',READ))
drugs = json.load(open('drug_misnaming.json',READ))
not_drugs = set(open('not_drug_names',READ).read().splitlines())

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def flatten(foo):
    for x in foo:
        if hasattr(x, '__iter__'):
            for y in flatten(x):
                yield y
        else:
            yield x

def valid_word(token):
	return all([ch.isalpha() for ch in token])

def process(string_of_text):
	string_of_text = string_of_text.encode('utf-8').decode('ascii','ignore')
	
	'''For now ignoring bigrams, will investigate later if needed.'''

	'''	
		Uses NLTK word_tokenize.
		Converts to lowercase. 
		Removes all stopwords from Simpsons and NLTK's list. 
		Removes all punctuation. 
		Removes all purely numeric entries. 
		Lemmatizes using avereged perceptron for pos tagging
	'''

	bag_of_words =  [contraction_expansion[token].split() if token in contraction_expansion else token
				for token in nltk.word_tokenize(string_of_text.lower())]
	
	#flatten after contraction expansion
	bag_of_words = list(flatten(bag_of_words))
	bag_of_words = [word for word in bag_of_words
					if not any([word in stopwords, not valid_word(word)])]

	bag_of_words = [lmtzr.lemmatize(word,pos=get_wordnet_pos(pos)) 
		for word,pos in nltk.pos_tag(bag_of_words)]
	
	bag_of_words = [drugs[word] if word in drugs else word 
						for word in bag_of_words]

	return list(flatten(bag_of_words))
	
def identify_drugs(list_of_tokens):
	tokens = set(flatten(list_of_tokens))
	ans = (tokens & set(flatten(drugs.values()))) - not_drugs
	return list(ans) #Sets are not JSON serializable

#Here is the easiest place to correct misspellings

bar = Bar('Tokenizing Text, Identifying Drugs',max = len(db.items()))
for title,entry in db.items():
	processed_text = process(entry['text'])
	db[title] = {"processed_text":processed_text,
				"drugs":identify_drugs(processed_text),
				"text":entry['text']}
	bar.next()
bar.finish()

json.dump(db,open('db.json','wb'))
	