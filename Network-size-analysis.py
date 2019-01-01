import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

df=pd.read_csv('food-climate-network-sizes-new-new.csv')
dfhs=df[df['event']=='hurricanesandy']
dflf=df[df['event']=='louisianaflooding']
dfhi=df[df['event']=='hurricaneirene']
dft1=df[df['event']=='tornadoes1']
dft2=df[df['event']=='tornadoes2']


freqhs=np.bincount(dfhs['followers'].tolist())
follhs=range(1,len(freqhs)+1)
freqlf=np.bincount(dflf['followers'].tolist())
folllf=range(1,len(freqlf)+1)
freqhi=np.bincount(dfhi['followers'].tolist())
follhi=range(1,len(freqhi)+1)
freqt1=np.bincount(dft1['followers'].tolist())
follt1=range(1,len(freqt1)+1)
freqt2=np.bincount(dft1['followers'].tolist())
follt2=range(1,len(freqt1)+1)


f, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, sharey=True,figsize=(15,4))
ax2.scatter(np.log10(follhs),np.log10(freqhs+1),color='black',s=3)
ax1.scatter(np.log10(follhi),np.log10(freqhi+1),color='black',s=3)
ax3.scatter(np.log10(folllf),np.log10(freqlf+1),color='black',s=3)
ax4.scatter(np.log10(follt1),np.log10(freqt1+1),color='black',s=3)
ax5.scatter(np.log10(follt2),np.log10(freqt2+1),color='black',s=3)
ax1.set_title('a.',fontsize='medium', loc='right',y=.91,x=.98)
ax2.set_title('b.',fontsize='medium', loc='right',y=.91,x=.98)
ax3.set_title('c.',fontsize='medium', loc='right',y=.91,x=.98)
ax4.set_title('d.',fontsize='medium', loc='right',y=.91,x=.98)
ax5.set_title('e.',fontsize='medium', loc='right',y=.91,x=.98)
#plt.suptitle('Follower Count Distribution of Active Disaster Tweeters During Several Disasters')
ax=f.add_subplot(111, frameon=False)
ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
ax.grid(False)
#txt = r'\textbf{Figure X}'
ax.set_xlabel(r'$\log_{10}$(\# followers)')
ax1.set_ylabel(r'$\log_{10}$(user count)')


plt.savefig('followers-dist-by-event-2.png',dpi=300)

