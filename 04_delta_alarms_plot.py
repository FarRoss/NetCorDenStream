#!/usr/bin/python3

# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] March 15, 2020
#

# Import libraries
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from utils import *

gs1 = gridspec.GridSpec(1, 1, wspace=0.0, hspace=0.32, top=.88, bottom=0.22, left=0.12, right=0.99)

# load variables
config = json.load(open('config.json'))

path = 'TimeProximityResults/'
features = config['featureModel']

kNeighbors_lst = config['KNeighbors']
delta_lst = config['delta_lst']

baseNodes = config['baseNodes']
features = config['featureModel']

SHOW_PLOT_FLAG = True
plot_id = '13'
plot_name = 'delta_alarm'

t = [0.99, 0.95, 0.90, 0.85, 0.80]

for baseNode in baseNodes:
    print(baseNode)
    for dataset in config['dataset']['availableDataset']:
        print(dataset)
        data = pd.read_csv(
            'TimeProximityResults/' + 'baseNode' + '_' + baseNode + '/' + features + '/' + dataset + '.csv')
        fig = plt.figure(figsize=(5, 2.2))
        ax = plt.subplot(gs1[0])
        ax.plot(data.delta.tolist(), data['1_Neighbor(s)'].values.tolist(), '-o', label='k=1', c='goldenrod', alpha=0.6)
        ax.plot(data.delta.tolist(), data['2_Neighbor(s)'].values.tolist(), '-o', label='k=2', c='c', alpha=0.6)
        ax.plot(data.delta.tolist(), data['3_Neighbor(s)'].values.tolist(), '-o', label='k=3', c='royalblue', alpha=0.6)
        ax.plot(data.delta.tolist(), data['4_Neighbor(s)'].values.tolist(), '-o', label='k=4', c='firebrick', alpha=0.6)
        ax.plot(data.delta.tolist(), data['5_Neighbor(s)'].values.tolist(), '-o', label='k=5', c='darkorange',
                alpha=0.6)
        ax.set_xlabel('Delta (in seconds)', size=12)  # , weight='bold')
        ax.set_ylabel('Alarms Raised', size=12)  # , weight='bold')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, ncol=5,
                  loc='upper center', prop={'size': 10},
                  bbox_to_anchor=(0.52, 1), borderpad=.12,
                  bbox_transform=plt.gcf().transFigure)
        plt.xticks(np.arange(5, 61, 5))
        plt.yticks(np.arange(0, data.values.max() + 5, data.values.max() / 6))
        plot_name = baseNode + '_' + dataset
        plot_id = features
        plotme(plt, plot_id, plot_name, show_flag=SHOW_PLOT_FLAG, png_only=False)
        plt.close()
        break
    break
