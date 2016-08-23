import json, os 
import matplotlib.pyplot as plt 
import Graphics as artist

from matplotlib import rcParams
rcParams['text.usetex'] = True

freqs = json.load(open(os.path.join('..','data','descriptions.json'),'rb'))

#Words unique to each

def plot(aList,ax, cutoff=20):
	tokens,frequencies = zip(*sorted(aList,key=lambda item:item[1],reverse=True))

	tokens = tokens[:cutoff][::-1]
	frequencies = frequencies[:cutoff][::-1]

	ax.plot(frequencies,xrange(cutoff),'k--', linewidth=2)
	artist.adjust_spines(ax)
	ax.set_yticks(xrange(cutoff))
	ax.set_yticklabels(map(artist.format,tokens),rotation='horizontal')

common_drugs,_ = zip(*freqs["both"].items())

for drug in ["both","lsd","mdma"]:
	fig = plt.figure()
	ax = fig.add_subplot(111)
	if drug == "both":
		plot(freqs["both"].iteritems(),ax)
	else:
		f = [(token,frequency) for token,frequency in freqs[drug].iteritems()
				if token not in common_drugs]
		with open(os.path.join('..','data','exclusive-mentions-%s'%drug),'wb') as fid:
			for token,frequency in sorted(f,key = lambda item:item[1], reverse=True):
				print>>fid, '%s (%d)'%(token,frequency)
		plot(f,ax)
	plt.tight_layout()
	plt.savefig(os.path.join('..','imgs',"%s.png"%drug))

	del fig, ax