import numpy as np 
import matplotlib.pyplot as plt 
import Graphics as artist

from matplotlib import rcParams
from sklearn.decomposition import PCA

rcParams['text.usetex'] = True

data = np.loadtxt('comention-matrix.tsv',delimiter='\t').astype(float)

#scale by columns
data /= data.sum(axis=0)
data = np.nan_to_num(data)
pca = PCA(n_components=10)
X = pca.fit_transform(data)
print pca.explained_variance_ratio_

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(X[:,0],X[:,1],c=X[:,2],cmap=plt.cm.seismic)
artist.adjust_spines(ax)
plt.tight_layout()
plt.show()