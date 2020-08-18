#!/usr/bin/python3

# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] March 15, 2020
#

# Import libraries
import json
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from tabulate import tabulate
from utils import *

gs1 = gridspec.GridSpec(1, 3, wspace=0.141, hspace=0.1, top=.87, bottom=0.16, left=0.04, right=0.99)

SHOW_PLOT_FLAG = True
plot_name = '01_k_Delta_prf'

# load variables
config = json.load(open('config.json'))

path = 'TimeProximityResults/'
features = config['featureModel']

kNeighbors_lst = config['KNeighbors']
delta_lst = ['5', '15', '30', '40', '55']

baseNodes = config['baseNodes']
features = config['featureModel']

feature_lst = ["ControlPlane", "DataPlane", "BravoData"]

t = [0.99, 0.95, 0.90, 0.85, 0.80]


def text(x, y, text):
    plt.text(x, y, text, ha="center", va="center",
             fontsize=13, )


def plotTK_k_Delta(CP, CPError, DP, DPError, Bravo, BravoError, flag):
    ax = plt.subplot(gs1[flag])
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xlim(1, 5)
    if flag == 0:
        left, width = -0.085, .5
        bottom, height = 0.27, .5
        right = left + width
        top = bottom + height
        ax.text(left, 0.5 * (bottom + top), 'Precision',
                horizontalalignment='right',
                verticalalignment='center',
                fontsize=12,
                rotation='vertical',
                transform=ax.transAxes)

    if flag == 1:
        left, width = -0.085, .5
        bottom, height = 0.27, .5
        right = left + width
        top = bottom + height
        ax.text(left, 0.5 * (bottom + top), 'False Alarms',
                horizontalalignment='right',
                verticalalignment='center',
                fontsize=12,
                rotation='vertical',
                transform=ax.transAxes)
    if flag == 2:
        left, width = -0.085, .5
        bottom, height = 0.27, .5
        right = left + width
        top = bottom + height
        ax.text(left, 0.5 * (bottom + top), 'Delay',
                horizontalalignment='right',
                verticalalignment='center',
                fontsize=12,
                rotation='vertical',
                transform=ax.transAxes)

    left, width = 0.6, .5
    bottom, height = -0.42, .5
    right = left + width
    top = bottom + height
    ax.text(left, 0.5 * (bottom + top), 'K_Neighbors',
            horizontalalignment='right',
            verticalalignment='center',
            fontsize=11,
            rotation='horizontal',
            transform=ax.transAxes)
    ax.plot([], [], ' ', label="$ \delta = 4 $")
    ax.plot([1, 2, 3, 4, 5], DP, linewidth=1, color='red', alpha=0.6, label='DataPlane Features')
    ax.fill_between(np.array([1, 2, 3, 4, 5]), np.array(DP) - np.array(DPError),
                    np.array(DP) + np.array(DPError), color='red', alpha=0.2)

    ax.plot([1, 2, 3, 4, 5], CP, linewidth=1, color='blue', alpha=0.6, label="ControlPlane Feature")
    ax.fill_between(np.array([1, 2, 3, 4, 5]), np.array(CP) - np.array(CPError),
                    np.array(CP) + np.array(CPError), color='blue', alpha=0.2)

    ax.plot([1, 2, 3, 4, 5], Bravo, linewidth=1, color='orange', alpha=0.6, label="Bravo Features")
    ax.fill_between(np.array([1, 2, 3, 4, 5]), np.array(Bravo) - np.array(BravoError),
                    np.array(Bravo) + np.array(BravoError), color='orange', alpha=0.2)

    return


for baseNode in baseNodes:
    print(baseNode)
    for dataset in config['dataset']['availableDataset']:
        print(dataset)
        CP_flag = 0
        DP_flag = 0

        # Load control plane results for baseNode
        CP = json.load(open(path + 'baseNode_' + baseNode + '/' + 'ControlPlane' + '/' + 'k_Delta' + '/' +
                            'TP_' + dataset + '.json'))
        if len(list(CP.keys())) > 1:
            CP_flag = 1

        # Load Data Plane results for baseNode
        DP = json.load(open(path + 'baseNode_' + baseNode + '/' + 'DataPlane' + '/' + 'k_Delta' + '/' +
                            'TP_' + dataset + '.json'))
        if len(list(DP.keys())) > 1:
            DP_flag = 1

        for k in kNeighbors_lst:
            print(k)
            k = str(k)
            for threshold in t:
                print(threshold)
                k_Table = []
                if CP_flag == 1 and ("Precision" in CP[k]) and ("Recall" in CP[k]) \
                        and ("False" in CP[k]) and ("Delay" in CP[k]):
                    k_Table.append(['ControlPlane', "\n".join([str("{:.3f}".format(i)) for i in CP[k]['Precision']]),
                                    "\n".join([str(i) for i in CP[k]['Recall']]),
                                    "\n".join([str(int(i)) for i in CP[k]['False']]),
                                    "\n".join([str(int(i)) for i in CP[k]['Delay']]),
                                    "\n".join([str(i) for i in delta_lst])])
                if DP_flag == 1 and ("Precision" in DP[k]) and ("Recall" in DP[k]) \
                        and ("False" in DP[k]) and ("Delay" in DP[k]):
                    k_Table.append(['DataPlane', "\n".join([str("{:.3f}".format(i)) for i in DP[k]['Precision']]),
                                    "\n".join([str(i) for i in DP[k]['Recall']]),
                                    "\n".join([str(int(i)) for i in DP[k]['False']]),
                                    "\n".join([str(int(i)) for i in DP[k]['Delay']]),
                                    "\n".join([str(i) for i in delta_lst])])
                Bravo = json.load(
                    open(path + 'baseNode_' + baseNode + '/' + 'BravoData' + '/' + 'k_Delta' + '/' + str(threshold) +
                         '_TP_' + dataset + '.json'))
                if (len(list(Bravo.keys())) > 1) and ("Precision" in Bravo[k]) and ("Recall" in Bravo[k]) \
                        and ("False" in Bravo[k]) and ("Delay" in Bravo[k]):
                    k_Table.append(['Bravo', "\n".join([str("{:.3f}".format(i)) for i in Bravo[k]['Precision']]),
                                    "\n".join([str(int(i)) for i in Bravo[k]['Recall']]),
                                    "\n".join([str(int(i)) for i in Bravo[k]['False']]),
                                    "\n".join([str(int(i)) for i in Bravo[k]['Delay']]),
                                    "\n".join([str(i) for i in delta_lst])])
                table = tabulate(k_Table, ["Features", "Precision", "Recall", "False Alarms", "Delay", "Delta"], "grid")
                f = open(path + 'baseNode_' + baseNode + '/' + 'k_Delta_Compare' + '/' + dataset + '/' + k + '-' + str(
                    threshold) +
                         '_' + dataset + '.txt', 'w')
                f.write(table)
                print('Saved {}'.format(f.name))
                f.close()
