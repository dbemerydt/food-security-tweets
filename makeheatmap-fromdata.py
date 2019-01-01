import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.colors import LogNorm

df1 = pd.read_csv('waytoomuch.csv')
df1 = df1.dropna(subset=['logfollowers', 'logincrease'])

plt.rc('text', usetex=True)
plt.rc('font', family='sans-serif')

df1 = df1[df1['logincrease']<np.inf]

x1 = df1['logfollowers']
y1 = df1['logincrease']

df2 = pd.read_csv('nullheatmapdata.csv').sample(n=len(df1))

plt.rc('text', usetex=True)
plt.rc('font', family='sans-serif')

x = df2['logfollowers']
y = df2['logincrease']

f, axarr = plt.subplots(1, 2, sharey=True)
f.set_figheight(2.5)
f.set_figwidth(6)
axarr[0].hist2d(x1, y1, bins=40, norm=LogNorm(), cmap='Greys')
im = axarr[1].hist2d(x, y, bins=40, norm=LogNorm(), cmap='Greys')
# axarr[0].set(adjustable='box-forced')
# axarr[1].set(adjustable='box-forced')
axarr[1].set_xlim(0,6.5)
axarr[0].set_xlim(0,6.5)
axarr[0].set_ylim(-2.5,2.5)
axarr[1].set_ylim(-2.5,2.5)
axarr[0].set_title('a.', fontsize='x-small', loc='left')
axarr[1].set_title('b.', fontsize='x-small', loc='left')
# f.text(0.4, 0.04, r'$\log_{10}$(\# Followers)',fontsize='medium', ha='center', va='center', rotation='horizontal')
f.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
plt.grid(False)
plt.xlabel(r'$\log_{10}$(\# Followers)',fontsize='small')
bigax = plt.gca()
# bigax.yaxis.set_label_coords(0.4,0.04)
plt.ylabel(r'$\log_{10}$(Fractional Change in Tweet Rate)',fontsize='x-small')
f.subplots_adjust(right=0.85,bottom=0.15,top=0.9,wspace=0.1)
cbar_ax = f.add_axes([0.87, 0.15, 0.025, 0.75])
cb = f.colorbar(im[3],cax=cbar_ax, ticks=[])
cb.set_label(r'$\log_{10}$(density)')
cb.ax.set_yticklabels([])
print('saving figure')
plt.savefig('heatmap-sandy+null-horizontal.png',dpi=600)



# plt.hist2d(x1, y1, bins=40, norm=LogNorm(), cmap='Greys')
# plt.xlabel(r'$\log_{10}$(\# Followers)',fontsize='large')
# plt.ylabel(r'$\log_{10}$(Fractional Change in Tweet Rate)',fontsize='large')
# cb = plt.colorbar()
# cb.set_label('density')
# plt.xlim(0,6.5)
# plt.ylim(-2.5,2.5)
# plt.savefig('heatmap-remake.png',dpi=600)

# plt.hist2d(x, y, bins=40, norm=LogNorm(), cmap='Greys')
# plt.xlabel(r'$\log_{10}$(\# Followers)',fontsize='large')
# plt.ylabel(r'$\log_{10}$(Fractional Change in Tweet Rate)',fontsize='large')
# cb = plt.colorbar()
# cb.set_label('density')
# plt.xlim(0,6.5)
# plt.ylim(-2.5,2.5)
# plt.savefig('nullheatmap.png',dpi=600)


