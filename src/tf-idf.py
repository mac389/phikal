import lda 
import numpy as np 
import matplotlib.pyplot as plt 
import Graphics as artist
import seaborn as sns 

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from matplotlib import rcParams
from progress.bar import Bar 

READ = 'rb'
drugs = open('../data/drugs-that-actually-occurr',READ).read().splitlines()
corpus = open('../data/corpus','rb').read().splitlines()
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join(['%s, %.04f'%(feature_names[i],model.components_[topic_idx,i])
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

#Create term matrix for LDA 
'''
all_words = list(set(' '.join(corpus).split()))

bar = Bar("Filling occurence matrix",max =len(all_words)*len(corpus))

def process(doc,word):
	bar.next()
	return doc.count(word)

X = np.array([[process(document,word) for word in all_words] 
											for document in corpus])
bar.finish()
'''
print("Extracting tf features for LDA...")
n_features = 1000
n_topics = 50 
n_top_words = 20 
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                                stop_words='english')

tf = tf_vectorizer.fit_transform(corpus)
lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                learning_method='online', learning_offset=50.,
                                random_state=0)
lda.fit(tf)
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)

'''
rcParams['text.usetex'] = True
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(lda.components_[:,:n_top_words],interpolation='nearest',aspect='auto',cmap=plt.cm.bone_r)
artist.adjust_spines(ax)
ax.set_xticks(xrange(n_top_words))
ax.set_xticklabels(map(artist.format,tf_feature_names[:n_top_words]),rotation='vertical')
ax.set_ylabel(artist.format('Topic'))
plt.tight_layout()
plt.show()
'''
import pandas as pd 
'''
df = pd.DataFrame(lda.components_, columns=tf_feature_names)

g = sns.clustermap(lda.components_)
plt.setp(g.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
g.savefig('../imgs/clustermap.png')
'''
#create drug-by-topic-matrix

def project(topic_idx,drug_idx):
	comments = corpus[drug_idx]
	topic = dict(zip(tf_feature_names,lda.components_[topic_idx,:]/np.linalg.norm(lda.components_[topic_idx,:])))
	bar.next()
	return sum([topic[word] for word in comments.split() if word in topic])

with open('../data/lda_feature_names','wb') as fid:
	for feature_name in tf_feature_names:
		print>>fid,feature_name
'''
bar = Bar("Filling occurence matrix",max =n_topics*len(drugs))
drug_by_topic = np.array([[project(topic,k) for topic in xrange(n_topics)] 
										for k,drug in enumerate(drugs)])
bar.finish()
np.savetxt('../data/drug-by-topic-matrix.tsv',drug_by_topic,fmt='%.04f',delimiter = '\t')
df_drugs = pd.DataFrame(drug_by_topic,index=drugs)
g = sns.clustermap(df_drugs)
plt.setp(g.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
g.savefig('../imgs/clustermap-drugs.png')
'''