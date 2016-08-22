import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import Graphics as artist
import seaborn as sns
from sklearn.decomposition import PCA
from matplotlib import rcParams
data = np.loadtxt('../data/drug-by-topic-matrix.tsv',delimiter = '\t')
feature_names = open('../data/lda_feature_names','rb').read().splitlines()
READ = 'rb'
drugs = open('../data/drugs-that-actually-occurr',READ).read().splitlines()

cutoff = 60

r = np.corrcoef(data)
df = pd.DataFrame(r,index=drugs,columns=drugs)
#df.to_csv('../data/lda_occurences.csv')
print df[df>0.9]
'''
sns.set(font_scale=0.8)
g = sns.clustermap(df,figsize=(19,19))
plt.setp(g.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
plt.setp(g.ax_heatmap.xaxis.get_majorticklabels(), rotation='vertical')

g.savefig('../imgs/cluster-drug-drug-correlation-by-topic.png')
'''
'''
fig = plt.figure()
ax = fig.add_subplot(111)

cax =ax.imshow(r[r[:,0].argsort()],interpolation='nearest',aspect='auto',cmap=plt.cm.seismic)
artist.adjust_spines(ax)
plt.colorbar(cax)
plt.tight_layout()
plt.savefig('../imgs/drug-drug-correlation-by-topic.png')

'''
'''
#PCA
pca = PCA(10)
x_r = pca.fit_transform(data)
print pca.explained_variance_ratio_
print x_r.shape
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x_r[:,0],x_r[:,1],'k.')
plt.show()
'''