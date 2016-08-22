import json, os 
import matplotlib.pyplot as plt 
import Graphics as artist

from matplotlib import rcParams
rcParams['text.usetex'] = True

freqs = json.load(open(os.path.join('..','data','descriptions.json'),'rb'))

#Words unique to each

def plot(aList,ax, cutoff=20):
	tokens,frequencies = zip(*sorted(aList,key=lambda item:item[1],reverse=True))
	ax.plot(frequencies[:cutoff],'k--')
	artist.adjust_spines(ax)
	ax.set_xticks(xrange(cutoff))
	ax.set_xticklabels(map(artist.format,tokens[:cutoff]),rotation='vertical')

common_drugs,_ = zip(*freqs["both"].items())

fig,axs = plt.subplots(nrows=3,sharey=True)
for drug,ax in zip(["both","lsd","mdma"],axs):
	if drug == "both":
		plot(freqs["both"].iteritems(),ax)
	else:
		f = [(token,frequency) for token,frequency in freqs[drug].iteritems()
				if token not in common_drugs]
		plot(f,ax)

plt.tight_layout()
plt.show()