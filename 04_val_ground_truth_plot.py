#!/usr/bin/python3
# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] January, 25th 2020.

# Import libraries
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from utils import *
from pathlib import Path
from set_paths import *
from prettytable import PrettyTable
from readGroundTruth import groundTruth

gs1 = gridspec.GridSpec(2, 1, wspace=0.0, hspace=0.1, top=.9, bottom=0.17, left=0.14, right=0.98)

config = json.load(open('config.json'))

SHOW_PLOT_FLAG = False
plot_id = '13'
plot_name = '01_val_groundTruth'

left, width = -0.13, .5
bottom, height = .18, .5
right = left + width
top = bottom + height

fig = plt.figure(figsize=(5, 2.5))


def plotFunction(anomalyDF, truth, flag):
    ax = plt.subplot(gs1[flag])
    ax.set_xlim((0, 147))
    ax.set_xticks([])
    if flag == 0:
        ax.text(left, 0.5 * (0.45 + top), metric,
                horizontalalignment='right',
                verticalalignment='center',
                rotation='vertical',
                transform=ax.transAxes)
    ax.plot(anomalyDF.index.to_list(), anomalyDF[metric], linewidth=0.5, color='black',
            label='MDT Data counter' if flag == 1 else '')

    tmpGT_df = truth.df[truth.df.Node == node].reset_index()
    for t in range(truth.df[truth.df.Node == node].shape[0]):
        lower_bound = anomalyDF.index[tmpGT_df.Start[t] > anomalyDF.time].tolist()
        upper_bound = anomalyDF.index[tmpGT_df.End[t] < anomalyDF.time].tolist()
        if tmpGT_df.Start[t] > anomalyDF.time[0] and tmpGT_df.End[t] < anomalyDF.time[
            anomalyDF.shape[0] - 1]:
            ax.axvspan(lower_bound[-1], upper_bound[0], alpha=0.25, color='lime',
                       label='groundTruth' if (flag == 1) and (t == 1) else '')
    if flag == 1:
        ax.text(left, 0.5 * (bottom + top), metric,
                horizontalalignment='right',
                verticalalignment='center',
                rotation='vertical',
                transform=ax.transAxes)
        ax.set_xlabel('Time[samples]')
        ax.set_xticks([i for i in range(0, anomalyDF.index.max() + 8, 20)])
        ax.figure.legend(bbox_to_anchor=(0.5, 2.5), ncol=2, loc=9, bbox_transform=ax.transAxes)
    return


for node in config["nodes"]:
    node = 'spine2'
    print(node)
    for dataset in config['dataset']['availableDataset']:
        dataset = 'portflap_first'
        print(dataset)
        table = PrettyTable()
        f_name = str(Path(__file__).parent) + '/Data/DatasetByNodes/' + node + dataset + '.csv'
        print(f_name)
        if os.path.isfile(f_name):
            df = pd.read_csv(f_name, low_memory=False).drop('Unnamed: 0', axis=1)
            truth = groundTruth('GrounTruth/' + dataset + '.txt', fileType='csv')
        print("Files are loaded")

        metric_lst = config['featureList']

        if len(truth.df.index[truth.df.Node == node].tolist()) >= 1:
            node_idx = truth.df.index[truth.df.Node == node].tolist()
            anomalyTime = pd.DataFrame(dtype=bool)

            if len(node_idx) == 1:
                anomalyTime = (df.time.astype('int64') >= truth.events[node_idx[0]]['startTime'] - 50) & (
                        df.time.astype('int64') <= truth.events[node_idx[0]]['endTime'] + 50)
            if len(node_idx) == 2:
                anomalyTime = (df.time.astype('int64') >= truth.events[node_idx[0]]['startTime'] - 50) & (
                        df.time.astype('int64') <= truth.events[node_idx[0]]['endTime'] + 50) | (
                                      df.time.astype('int64') >= truth.events[node_idx[1]]['startTime'] - 50) & (
                                      df.time.astype('int64') <= truth.events[node_idx[1]]['endTime'] + 50)
            if len(node_idx) == 3:
                anomalyTime = (df.time.astype('int64') >= truth.events[node_idx[0]]['startTime'] - 50) & (
                        df.time.astype('int64') <= truth.events[node_idx[0]]['endTime'] + 50) | (
                                      df.time.astype('int64') >= truth.events[node_idx[1]]['startTime'] - 50) & (
                                      df.time.astype('int64') <= truth.events[node_idx[1]]['endTime'] + 50) | (
                                      df.time.astype('int64') >= truth.events[node_idx[2]]['startTime'] - 50) & (
                                      df.time.astype('int64') <= truth.events[node_idx[2]]['endTime'] + 50)
            anomalyDF = df[anomalyTime]
            anomalyDF = anomalyDF.reset_index(drop=True)

            for metric in metric_lst:
                if metric == 'paths-count':
                    flag = 1
                    plotFunction(anomalyDF, truth, flag)
                if metric == 'vrf__path-count':
                    flag = 0
                    plotFunction(anomalyDF, truth, flag)
            plotme(plt, plot_id, plot_name, show_flag=SHOW_PLOT_FLAG)
        break
    break
