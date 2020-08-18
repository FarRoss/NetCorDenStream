#!/usr/bin/python3
# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] January, 25th 2020.


import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
from utils import plotme

SHOW_PLOT_FLAG = False
plot_id = '13'
plot_name = 'oDenStream_ncDenStream'

# Loading the file
df = pd.read_csv('compare.csv')
print("File is loaded")

gs1 = gridspec.GridSpec(1, 1, wspace=0.35, hspace=0.23, top=.85, bottom=0.23, left=0.09, right=0.99)

# fig = plt.figure(figsize=(5, 2))
# ax = fig.add_subplot(111)

fig = plt.figure(figsize=(5, 1.6))
ax = plt.subplot(gs1[0])

ax.plot([i + 1 for i in df.index.to_list()], df['OutlierDenStream'], '-s', ms=4, linewidth=1, label='OutlierDenStream',
        c='orange', alpha=0.8)
ax.plot([i + 1 for i in df.index.to_list()], df['bravo'], '-s', ms=4, linewidth=1, label='NetCorDenStream', c='blue',
        alpha=0.5)

# ax.set_xlabel('K_Neighbors ', size=12, weight='bold')
# ax.set_ylabel('Alarms', size=12, weight='bold')


left, width = -0.058, .5
bottom, height = 0.27, .5
right = left + width
top = bottom + height
ax.text(left, 0.5 * (bottom + top), 'Alarms',
        horizontalalignment='right',
        verticalalignment='center',
        fontsize=11,
        rotation='vertical',
        transform=ax.transAxes)

left, width = 0.61, .5
bottom, height = -0.28, 0
right = left + width
top = bottom + height
ax.text(left, 0.5 * (bottom + top), 'K_Neighbors',
        horizontalalignment='right',
        verticalalignment='center',
        fontsize=11,
        rotation='horizontal',
        transform=ax.transAxes)

handles, labels = ax.get_legend_handles_labels()
plt.legend(handles, labels, ncol=2,
           loc='upper center', prop={'size': 10},
           bbox_to_anchor=(0.55, 1.02), borderpad=.12,
           bbox_transform=plt.gcf().transFigure)
plt.xticks(np.arange(1, 6, 1))
plt.yticks(np.arange(0, 41, 10))
# plt.yticks(np.arange(1, 450, 100))
# ax.plot(df.index.to_list(), np.log(df['Abnomalies']) - np.log(df['Bravo']), label='without', c='r')
# ax.plot(df.index.to_list(), np.log(df['Bravo']), label='Bravo', c='b')

plotme(plt, plot_id, plot_name, show_flag=SHOW_PLOT_FLAG, png_only=False)
# plt.show()
