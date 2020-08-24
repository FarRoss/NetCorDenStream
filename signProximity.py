#!/usr/bin/python3
# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] January, 25th 2020.

import pandas as pd
from utils import *
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

path = 'Data/ResultsSpatialDetection/'
data_Path = 'Data/DatasetByNodes/'

algorithm = 'DENSTREAM'


gs1 = gridspec.GridSpec(2, 1, wspace=0.0, hspace=0.15, top=.88, bottom=0.16, left=0.08, right=0.98)
SHOW_PLOT_FLAG = False
plot_id = '14'
fig = plt.figure(figsize=(5, 2.5))


class signproximity():
    def __init__(self, node, truth, delta, feature):
        self.node = node
        self.truth = truth
        self.delta = delta
        self.feature = feature
        self.nodeDataDF = {}
        self.eventSP = {}

    def getRawData(self, node, dataset, featureList):
        rawDF = pd.read_csv(
            data_Path + node + dataset + '.csv', low_memory=False).dropna().drop('Unnamed: 0', axis=1)

        if self.feature == "ControlPlane":
            rawDF = rawDF[featureList]

        # Without bravo
        rawDF = rawDF.loc[:, rawDF.std() != 0]
        rawDF = ((rawDF - rawDF.mean()) / rawDF.std()).dropna(axis=1)

        rawDF['ind'] = [i for i in range(len(rawDF))]

        self.nodeDataDF[node] = rawDF

    def getRawSampleData(self, topoNode, dataset, indexTime, featureList, threshold):

        # Loading all datasets needed
        if threshold != 0:
            df = pd.read_csv(
                path + self.feature + '/' + dataset + '_' + algorithm + '_' + topoNode + '_' + str(threshold) + '.csv')
        else:
            df = pd.read_csv(
                path + self.feature + '/' + dataset + '_' + algorithm + '_' + topoNode + '.csv')

        rawDF = pd.read_csv(
            data_Path + topoNode + dataset + '.csv', low_memory=False).dropna().drop('Unnamed: 0', axis=1)

        # Depending on the feature selection, choice features.
        if self.feature == "ControlPlane":
            rawDF = rawDF[featureList]

        # Without bravo
        rawDFTimes = df['time'].astype('int')
        rawDF = rawDF.drop(['time'], axis=1)

        rawDF = rawDF.loc[:, rawDF.std() != 0]
        rawDF = ((rawDF - rawDF.mean()) / rawDF.std()).dropna(axis=1)

        rawDF['time'] = rawDFTimes
        rawDF['ind'] = [i for i in range(len(rawDF))]
        df['ind'] = [i for i in range(len(df))]

        rawDF['results'] = df.result
        self.nodeDataDF[topoNode] = rawDF

        df['datetime'] = pd.to_datetime(df.time, unit='s')
        df = df.set_index('datetime')
        dfresampled = df.resample('5s')  # Resample to 5 seconds interval.

        listResults = []
        listInd = []
        precedent = None

        for index in indexTime:
            try:
                currentSample = dfresampled.get_group(index)['result']

                sample = dfresampled.ind.indices[index][0]
                if len(currentSample) > 1:
                    listResults.append(currentSample.iloc[-1])
                    listInd.append(sample)
                    precedent = currentSample.iloc[-1]
                elif len(currentSample) == 1:
                    listResults.append(currentSample.iloc[0])
                    listInd.append(sample)
                    precedent = currentSample.iloc[0]
                else:
                    print('Resampling Error')
            except:
                listResults.append(precedent)
                if precedent != None:
                    listInd.append(sample)
                else:
                    listInd.append(999)
        return listResults, listInd

    def getIndexTime(self, baseNode, dataset, threshold):

        if threshold != 0:
            df = pd.read_csv(
                path + self.feature + '/' + dataset + '_' + algorithm + '_' + baseNode + '_' + str(threshold) + '.csv')
        else:
            df = pd.read_csv(
                path + self.feature + '/' + dataset + '_' + algorithm + '_' + baseNode + '.csv')
        times = pd.to_datetime(df.time, unit='s')

        startTime = times.iloc[0].replace(second=0, microsecond=0)
        endTime = times.iloc[-1].replace(second=0, microsecond=0)
        indexTime = pd.date_range(start=startTime, end=endTime, freq='5s')

        return indexTime

    def proximityAlgo(self, df, topology, KNeighbors):
        # get node neighbors
        nodeNeighbors = topology[self.node]

        SPct = []

        node_idx = df.columns.get_loc(self.node) + 1

        # loop through each row
        for row in df.itertuples(index=True):
            if row[node_idx] == True:  # event node has flag sample as anomalous
                if (row.ind + self.delta // 5) < df.shape[0]:
                    deltaRow = df.iloc[row.ind + self.delta // 5]  # get the row for t + delta
                    if (deltaRow[nodeNeighbors] == True).sum() >= KNeighbors:
                        SPctTmp = {}
                        SPctTmp[self.node] = row[node_idx + 1]
                        for n in nodeNeighbors:
                            if deltaRow[n] == True:
                                SPctTmp[n] = deltaRow[n + '_ind']
                        SPct.append(SPctTmp)
        return SPct

    def proximity(self, topology, KNeighbors, dataset, featureList, networkNodes, threshold=0):

        # dataset = configuration['dataset']['list']

        idxTime = self.getIndexTime(self.node, dataset, threshold)
        df = pd.DataFrame(index=idxTime)
        # dfInd = pd.DataFrame(index=idxTime)
        df['time'] = idxTime.astype('int64') // 1e9
        # dfInd['time'] = idxTime.astype('int64') // 1e9

        # for node in config['nodes']:
        for node in networkNodes:
            df[node], df[str(node) + '_ind'] = self.getRawSampleData(node, dataset, idxTime, featureList, threshold)
            # self.getRawData(node, dataset)
        df = df.dropna()

        # get df for range of injected anomalies based on ground truth.
        time = df['time']

        for event in self.truth.events:
            # self.eventSP[event.name] = {}
            anomalyTimes = (time >= event['startTime']) & (time <= event['endTime'])
            anomalyDF = df[anomalyTimes]
            # anomalyDFInd = dfInd[anomalyTimes]

            anomalyDF['ind'] = [i for i in range(len(anomalyDF))]

            self.eventSP[event['name']] = self.proximityAlgo(anomalyDF, topology, KNeighbors)
            dfSP = self.getRowNodeData(event)
            # self.plotSP(event['name'], KNeighbors, dataset, dfSP)
            if int(event['name']) == 5 or int(event['name']) == 6:
                self.finalplotSP(event['name'], KNeighbors, dataset, dfSP)

        return

    def getRowNodeData(self, event):
        # Process self.nodeDataDF and self.eventSP to plot correlation

        eDF = {}
        SP_eStats = self.eventSP[event['name']]
        for ct in range(len(SP_eStats)):
            SP_dict = SP_eStats[ct]

            eDF[ct] = pd.DataFrame()
            for k, va in SP_dict.items():
                eDF[ct] = eDF[ct].append(self.nodeDataDF[k].loc[self.nodeDataDF[k].ind == va],
                                         ignore_index=True)  # Get row for SP alarm event.
            eDF[ct] = eDF[ct].append(self.nodeDataDF[self.node].head(va - 1))
            colsToDrop = (eDF[ct].count()[eDF[ct].count().array < 3]).index.values.tolist()
            eDF[ct] = eDF[ct].drop(colsToDrop, axis=1)
        return eDF

    def plotSP(self, eName, k, dataset, SP_df):
        for e, spDF in SP_df.items():
            fig = plt.figure(figsize=(5, 1.6))
            ax = plt.subplot(gs1[0])
            spDF = spDF.dropna()
            del spDF['time']
            del spDF['ind']
            if len(str(e)) == 1:
                vaCt = list(self.eventSP[int(eName)][int(str(0) + str(e))].values())[-1]
            else:
                vaCt = list(self.eventSP[int(eName)][int(str(e))].values())[-1]

            spDF_Tmp = spDF.head(spDF.shape[0] - vaCt)
            nDF = spDF.tail(vaCt)
            ax.plot([i for i in range(nDF.mean().values.size)], nDF.mean().values, marker='s', ms=1.5, linewidth=1,
                    color='black')
            ax.fill_between([i for i in range(nDF.mean().values.size)], nDF.mean().values - nDF.std().values,
                            nDF.mean().values + nDF.std().values)
            for i, (name, row) in enumerate(spDF_Tmp.iterrows()):
                if i == 0:
                    ax.plot([i for i in range(row.size)], row.values, marker='.', linewidth=1)
                    ax.set_title(str(dataset) + '_delta=' + str(self.delta) + '_Kneighbor=' + str(k) + '_' + str(
                        eName) + '_' + str(e))
                    plot_name = 'Kneighbor=' + str(k) + '_delta=' + str(self.delta) + '_' + str(
                        eName) + '_' + str(e)
                    plotme(plt, plot_id, plot_name, plot_path='./SignProximityResults/' + str(self.node),
                           show_flag=SHOW_PLOT_FLAG, pdf_only=True)
                    break
            # plt.show()
            plt.close()

    def plotFunction(self, x, y, nDF, k, flag):
        ax = plt.subplot(gs1[flag])

        ax.set_xlim((0, 11))
        ax.set_xticks([i for i in range(0, 11)])

        if flag == 0:
            ax.set_xticklabels(labels='')
            ax.set_ylabel('Node $n_2$')
            ax.yaxis.set_label_coords(-0.04, 0.5)
            ax.plot(x, y, '-o', marker='s', ms=3, linewidth=1, color='blue', alpha=0.6, zorder=1)
            ax.plot([i for i in range(nDF.mean().values.size)], nDF.mean().values,
                    linewidth=0.5, color='black', zorder=3)
            ax.fill_between([i for i in range(nDF.mean().values.size)], nDF.mean().values - nDF.std().values,
                            nDF.mean().values + nDF.std().values, color='lime',
                            alpha=0.4, linewidth=0, zorder=3, interpolate=True)


        if flag == 1:
            ax.set_xticks([i for i in range(0, 12)])
            ax.set_ylabel('Node $n_1$')
            ax.yaxis.set_label_coords(-0.04, 0.5)
            #
            ax.set_xlabel('MDT Counters')
            #
            ax.xaxis.set_label_coords(0.5, -0.3)
            ax.plot(x, y, '-o', marker='s', ms=3, linewidth=1, color='blue', alpha=0.6,
                    label='t+$\delta$ counter stream', zorder=1)
            ax.plot([i for i in range(nDF.mean().values.size)], nDF.mean().values,
                    linewidth=0.5, color='black', label='Mean', zorder=3)
            ax.fill_between([i for i in range(nDF.mean().values.size)], nDF.mean().values - nDF.std().values,
                            nDF.mean().values + nDF.std().values, color='lime',
                            alpha=0.4, linewidth=0, label='1 STD', zorder=3, interpolate=True)
            ax.figure.legend(bbox_to_anchor=(0.5, 2.55), ncol=3, loc=9, bbox_transform=ax.transAxes)


        return

    def finalplotSP(self, eName, k, dataset, SP_df):

        for e, spDF in SP_df.items():
            w = False

            spDF = spDF.dropna()
            del spDF['time']
            del spDF['ind']
            if len(str(e)) == 1:
                vaCt = list(self.eventSP[int(eName)][int(str(0) + str(e))].values())[-1]
            else:
                vaCt = list(self.eventSP[int(eName)][int(str(e))].values())[-1]

            spDF_Tmp = spDF.head(spDF.shape[0] - vaCt)
            nDF = spDF.tail(vaCt)
            for i, (name, row) in enumerate(spDF_Tmp.iterrows()):
                if i == 0:
                    if dataset == 'bgpclear_second' and self.delta == 10 and k == 1 and eName == 5 and e == 33:
                        self.plotFunction([i for i in range(row.size)], row.values, nDF, k=1, flag=0)
                    if dataset == 'bgpclear_second' and self.delta == 10 and k == 1 and eName == 6 and e == 0:
                        self.plotFunction([i for i in range(row.size)], row.values, nDF, k=1, flag=1)
                        w = True
                        plot_name = 'SP_Delta_k_alarms'
                        plotme(plt, plot_id, plot_name, show_flag=SHOW_PLOT_FLAG)
                        plt.close()