import numpy as np 

from scipy.stats import pearsonr, betai
from statsmodels.sandbox.stats.multicomp import multipletests
READ = 'rb'
data = np.loadtxt('../data/drug-by-topic-matrix.tsv',delimiter = '\t')
drugs = open('../data/drugs-that-actually-occurr',READ).read().splitlines()

def corrcoef(matrix):
    r = np.corrcoef(matrix)
    rf = r[np.triu_indices(r.shape[0], 1)]
    df = matrix.shape[1] - 2
    ts = rf * rf * (df / (1 - rf * rf))
    pf = betai(0.5 * df, 0.5, df / (df + ts))
    p = np.zeros(shape=r.shape)
    p[np.triu_indices(p.shape[0], 1)] = pf
    p[np.tril_indices(p.shape[0], -1)] = pf
    p[np.diag_indices(p.shape[0])] = np.ones(p.shape[0])
    return r, p

r,p = corrcoef(data)

uncorrected_p = p[np.tril_indices_from(p,k=-1)]
to_reject, corrected_p,_,b = multipletests(uncorrected_p,method='bonferroni')

print b
with open('../data/significant-occurrences-bon','wb') as f:
	for k,(i,j) in enumerate(zip(*np.tril_indices_from(r,k=-1))):
		if not to_reject[k]:
			print>>f, '%s : %s | r = %.04f, p = %.04f, p (corrected) = %.04f'%(drugs[i],drugs[j],r[i,j],p[i,j],corrected_p[k])

'''
correction_factor  =  r.shape[0] * (r.shape[0]-1)/2
significance = 0.05

significance /= correction_factor
print significance

with open('../data/significant-occurrences','wb') as f:
	for i,j in zip(*np.where(p>(1-significance))):
		print>>f, '%s : %s | r = %.04f, p = %.04f'%(drugs[i],drugs[j],r[i,j],p[i,j])
'''