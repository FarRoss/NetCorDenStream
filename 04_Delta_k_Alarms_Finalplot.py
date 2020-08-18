#!/usr/bin/python3

# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] March 15, 2020
#

import matplotlib.pyplot as plt
import json
from utils import plotme
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

# gs1 = gridspec.GridSpec(1, 1, wspace=0.35, hspace=0.23, top=.87, bottom=0.2, left=0.09, right=0.99)
gs1 = gridspec.GridSpec(2, 1, wspace=0.0, hspace=0.15, top=.88, bottom=0.16, left=0.09, right=0.99)

fig = plt.figure(figsize=(5, 2.5))


def plotFunction(x, y, color, k, flag):
    ax = plt.subplot(gs1[flag])
    ax.plot(x, y, '-o', marker='s', ms=3, linewidth=1, label='k=' + str(k), c=color, alpha=0.5)

    if flag == 0:
        ax.set_xticklabels(labels='')
        # ax.plot(x, y, '-o', marker='s', ms=3, linewidth=1, label='k=' + str(k), c=color, alpha=0.5)
        ax.set_xlim((4, 61))
        ax.legend(bbox_to_anchor=(0.5, 1.4), ncol=5, loc=9, prop={'size': 9.7},
                  bbox_transform=ax.transAxes, facecolor='lime', framealpha=0.2)
        ax.annotate('ControlPlane',
                    xy=(50, 35), xycoords='data',
                    xytext=(50, 35), textcoords='data',
                    size=8, va="center", ha="center",
                    bbox=dict(boxstyle="round", fc="lime", alpha=0.04))

    if flag == 1:
        ax.set_xticks([i for i in range(5, 61, 5)])
        ax.set_ylabel('Number of alarms raised')
        ax.yaxis.set_label_coords(-0.06, 1)

        ax.set_xlabel('delta (in seconds)')

        ax.xaxis.set_label_coords(0.5, -0.3)
        ax.set_xlim((4, 61))
        ax.annotate('DataPlane',
                    xy=(45, 35), xycoords='data',
                    xytext=(50, 38), textcoords='data',
                    size=8, va="center", ha="center",
                    bbox=dict(boxstyle="round", fc="lime", alpha=0.04))
    return


color_list = ['r', 'b', 'g', 'orange', 'purple']

baseNodes = ['spine4', 'spine4_1']
for baseNode in baseNodes:
    dataset = "bgpclear_apptraffic_2hourRun"

    if baseNode == 'spine4':
        flag = 0
        data = pd.read_csv(path + 'baseNode_' + baseNode + '/' + 'BravoData' + '/' + dataset + '.csv')
    else:
        flag = 1
        baseNode = 'spine4'
        dataset = "bgpclear_no_traffic_2hourRun"
        data = pd.read_csv(path + 'baseNode_' + baseNode + '/' + 'DataPlane' + '/' + dataset + '.csv')
    for i in range(1, 6):
        k = str(i) + '_Neighbor(s)'
        plotFunction(delta_lst, data[k].values, color_list[i - 1], i, flag)

plot_name = 'TP_Delta_k_alarms'
plotme(plt, plot_id, plot_name, show_flag=SHOW_PLOT_FLAG)
plt.close()
