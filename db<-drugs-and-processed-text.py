import json, nltk, string, itertools, sys


from awesome_print import ap 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.util import ngrams

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

list_of_drugs = set(open('list_of_drugs').read().splitlines())
not_drug_names = set(open('not_drug_names').read().splitlines())

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
	string_of_text = string_of_text.decode('utf-8').encode('ascii','ignore')
	
	''' HAVE TO REDO THIS. MUST EXTRACT DRUG NAMES BEFORE REMOVING NUMBERS
			DON'T WANT TO MISS TYLENOL 3. (OR JUST SEARCH FOR THIS?)'''

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
	
	sys.std.out(string_of_text)
	'''
	#bag_of_words += ngrams(bag_of_words,2)

	ap(bag_of_words)

	#flatten after contraction expansion
	bag_of_words = list(flatten(bag_of_words))
	bag_of_words = [word for word in bag_of_words
					if not any([word in stopwords, not valid_word(word)])]

	bag_of_words = [lmtzr.lemmatize(word,pos=get_wordnet_pos(pos)) 
		for word,pos in nltk.pos_tag(bag_of_words)]
	'''
	return bag_of_words
	#Will pos tagging help?

def identify_drugs(list_of_tokens):
	tokens = set(list_of_tokens)
	drugs = (tokens & list_of_drugs) - not_drug_names
	return list(drugs) #Sets are not JSON serializable

#Here is the easiest place to correct misspellings

for text in sys.stdin:
	sys.stdout.write("\n")
	sys.stdout.write(process(text))
	sys.stdout.write("\n")