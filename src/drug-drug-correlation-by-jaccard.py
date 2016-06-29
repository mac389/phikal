import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import Graphics as artist
import seaborn as sns
from sklearn.decomposition import PCA
from matplotlib import rcParams


data = np.loadtxt('../data/drug-jaccard-similarity-actually-occurred.tsv',delimiter='\t').astype(float)
feature_names = open('../data/lda_feature_names','rb').read().splitlines()
READ = 'rb'
drugs = open('../data/drugs-that-actually-occurr',READ).read().splitlines()

cutoff = 60

r = np.corrcoef(data)
df = pd.DataFrame(r,index=drugs,columns=drugs)
sns.set(font_scale=0.8)
g = sns.clustermap(df,figsize=(19,19))
plt.setp(g.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
plt.setp(g.ax_heatmap.xaxis.get_majorticklabels(), rotation='vertical')

g.savefig('../imgs/cluster-drug-drug-correlation-by-occurrence.png')
