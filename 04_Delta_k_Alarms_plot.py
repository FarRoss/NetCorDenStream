#!/usr/bin/python3

# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] March 15, 2020
#

import matplotlib.pyplot as plt
import json
from utils import plotme
import numpy as np
import pandas as pd
import matplotlib.gridspec as gridspec

# load variables
config = json.load(open('config.json'))

path = 'TimeProximityResults/'
features = config['featureModel']

baseNodes = config['baseNodes']

kNeighbors_lst = config['KNeighbors']  # number of neighbors to consider
delta_lst = config['delta_lst']  # In seconds

SHOW_PLOT_FLAG = False
plot_id = '13'

gs1 = gridspec.GridSpec(1, 1, wspace=0.35, hspace=0.23, top=.87, bottom=0.2, left=0.09, right=0.99)

# df = pd.read_csv('./TimeProximityResults/spine1.csv')
for baseNode in baseNodes:
    for dataset in config['dataset']['availableDataset']:
        data = pd.read_csv(path + 'baseNode_' + baseNode + '/' + features + '/' + dataset + '.csv')
        for e in range(12):
            fig = plt.figure(figsize=(5, 1.8))
            ax = plt.subplot(gs1[0])
            ax.plot(delta_lst, data['1_Neighbor(s)'].values, '-o', marker='s', ms=4, linewidth=1, label='k=1', c='r',
                    alpha=0.5)
            ax.plot(delta_lst, data['2_Neighbor(s)'].values, '-o', marker='s', ms=4, linewidth=1, label='k=2', c='b',
                    alpha=0.5)
            ax.plot(delta_lst, data['3_Neighbor(s)'].values, '-o', marker='s', ms=4, linewidth=1, label='k=3', c='g',
                    alpha=0.5)
            ax.plot(delta_lst, data['4_Neighbor(s)'].values, '-o', marker='s', ms=4, linewidth=1, label='k=4',
                    c='orange', alpha=0.5)
            ax.plot(delta_lst, data['5_Neighbor(s)'].values, '-o', marker='s', ms=4, linewidth=1, label='k=5',
                    c='purple', alpha=0.5)
            # ax.set_xlabel('Delta (in seconds)', size=12) #, weight='bold')
            # ax.set_ylabel('Alarms Raised', size=12) #, weight='bold')
            left, width = -0.058, .5
            bottom, height = 0.27, .5
            right = left + width
            top = bottom + height
            ax.text(left, 0.5 * (bottom + top), 'Alarms Raised',
                    horizontalalignment='right',
                    verticalalignment='center',
                    fontsize=11,
                    rotation='vertical',
                    transform=ax.transAxes)

            left, width = 0.66, .5
            bottom, height = -0.25, 0
            right = left + width
            top = bottom + height
            ax.text(left, 0.5 * (bottom + top), 'Delta (in seconds)',
                    horizontalalignment='right',
                    verticalalignment='center',
                    fontsize=11,
                    rotation='horizontal',
                    transform=ax.transAxes)

            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles, labels, ncol=5,
                      loc='upper center', prop={'size': 10},
                      bbox_to_anchor=(0.54, 1.02), borderpad=.12,
                      bbox_transform=plt.gcf().transFigure)
            plt.xticks(np.arange(5, 61, 5))
            plot_name = 'timeProx_' + str(e)
            plot_name = features + '_' + baseNode + '_' + dataset
            plotme(plt, plot_id, plot_name, show_flag=SHOW_PLOT_FLAG, png_only=False)
            plt.close()
