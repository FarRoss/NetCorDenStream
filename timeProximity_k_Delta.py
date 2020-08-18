#!/usr/bin/python3
# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] January, 25th 2020.

import numpy as np
import pandas as pd
import json

configuration = json.load(open('config.json'))

path = 'Data/ResultsSpatialDetection/'
features = configuration['featureModel']
import sys
import statsmodels.stats.api as sms
import numpy as np

algorithm = 'DENSTREAM'


class timeproximity():
    def __init__(self, node, truth, delta):
        self.node = node
        self.truth = truth
        self.delta = delta

    def sampleData(self, topoNode, dataset, indexTime, threshold):

        if threshold != 0:
            df = pd.read_csv(
                path + features + '/' + dataset + '_' + algorithm + '_' + topoNode + '_' + str(threshold) + '.csv')
        else:
            df = pd.read_csv(
                path + features + '/' + dataset + '_' + algorithm + '_' + topoNode + '.csv')
        df['datetime'] = pd.to_datetime(df.time, unit='s')
        df = df.set_index('datetime')
        dfresampled = df.resample('5s')

        lstSampResults = []
        prev = None

        for index in indexTime:
            try:
                curSamp = dfresampled.get_group(index)['result']

                if len(curSamp) > 1:
                    lstSampResults.append(curSamp.iloc[-1])
                    prev = curSamp.iloc[-1]
                elif len(curSamp) == 1:
                    lstSampResults.append(curSamp.iloc[0])
                    prev = curSamp.iloc[0]
                else:
                    print('Resampling error')
            except:
                lstSampResults.append(prev)
        return lstSampResults

    def getTimeIdx(self, baseNode, dataset, threshold):

        if threshold != 0:
            df = pd.read_csv(
                path + features + '/' + dataset + '_' + algorithm + '_' + baseNode + '_' + str(threshold) + '.csv')
        else:
            df = pd.read_csv(
                path + features + '/' + dataset + '_' + algorithm + '_' + baseNode + '.csv')
        times = pd.to_datetime(df.time, unit='s')

        start_Time = times.iloc[0].replace(second=0, microsecond=0)
        end_Time = times.iloc[-1].replace(second=0, microsecond=0)
        idx_Time = pd.date_range(start=start_Time, end=end_Time, freq='5s')

        return idx_Time

    def proximityAlgo(self, df, topology, KNeighbors):
        # get node neighbors
        nodeNeighbors = topology[self.node]

        timeProximityCt = 0

        node_idx = df.columns.get_loc(self.node) + 1

        # loop through each row
        for row in df.itertuples(index=True):
            if row[node_idx] == True:  # event node has flag sample as anomalous
                if (row.ind + self.delta // 5) < df.shape[0]:
                    deltaRow = df.iloc[row.ind + self.delta // 5]  # get the row for t + delta
                    if (deltaRow[
                            nodeNeighbors] == True).sum() >= KNeighbors:  # k Neighbor has flag sample as anomalous, time proximity
                        timeProximityCt += 1
        return timeProximityCt

    def proximity(self, topology, KNeighbors, dataset, threshold=0):

        # dataset = configuration['dataset']['list']

        idxTime = self.getTimeIdx(self.node, dataset, threshold)
        df = pd.DataFrame(index=idxTime)
        df['time'] = idxTime.astype('int64') // 1e9

        for node in configuration['nodes']:
            df[node] = self.sampleData(node, dataset, idxTime, threshold)
        df = df.dropna()

        # get df for range of injected anomalies based on ground truth.
        time = df['time']

        timeProximCt = 0
        for event in self.truth.events:
            anomalyTimes = (time >= event['startTime']) & (time <= event['endTime'])
            anomalyDF = df[anomalyTimes]

            anomalyDF['ind'] = [i for i in range(len(anomalyDF))]

            timeProximCt = timeProximCt + self.proximityAlgo(anomalyDF, topology, KNeighbors)
        return timeProximCt

    def getStats(self, topology, kNeighbors_lst, delta_lst, dataset, threshold=0):

        TP = pd.read_csv(
            'TimeProximityResults/' + 'baseNode' + '_' + self.node + '/' + features + '/' + dataset + '.csv')

        resultStats = {}
        # dataset = configuration['dataset']['list']

        idxTime = self.getTimeIdx(self.node, dataset, threshold)
        df = pd.DataFrame(index=idxTime)
        df['time'] = idxTime.astype('int64') // 1e9

        for node in configuration['nodes']:
            df[node] = np.array(self.sampleData(node, dataset, idxTime, threshold), dtype='O')
        df = df.dropna()

        time = df['time']
        # truth = groundTruth('GrounTruth/' + dataset + '.txt', fileType='csv')

        timeProxStats = {}

        for i in delta_lst:
            timeProxStats[i] = {}
            timeProxStats[i]['Precision'] = []
            timeProxStats[i]['Recall'] = []
            timeProxStats[i]['False'] = []
            timeProxStats[i]['Delay'] = []

        for ct in range(len(self.truth.clears)):
            print('event ', ct)
            event = self.truth.events[ct]
            clear = self.truth.clears[ct]

            # Get event anomalous data
            anomalyTimes = (time >= event['startTime']) & (time <= event['endTime'])
            anomalyDF = df[anomalyTimes]

            anomalyDF['ind'] = [i for i in range(len(anomalyDF))]

            # get node neighbors
            nodeNeighbors = topology[self.node]

            node_idx = anomalyDF.columns.get_loc(self.node) + 1

            # Get clear anomalous data
            anomalyClear = (time > clear['startTime']) & (time <= clear['endTime'])
            # anomalyClearDF = df[anomalyClear]
            anomalyClearDF = df[~anomalyTimes]

            anomalyClearDF['ind'] = [i for i in range(len(anomalyClearDF))]
            # currentEvent = currentEvent.drop(currentEvent.tail(1).index)

            resultStats[ct] = {}
            for kNeighbors in kNeighbors_lst:
                k = kNeighbors
                resultStats[ct][k] = {}

                for delta in delta_lst:

                    resultStats[ct][k] = timeProxStats
                    checkOnce = True

                    for row in anomalyDF.itertuples(index=True):
                        # Running algorithm to get delay
                        if (row[node_idx] == True):  # event node has flag sample as anomalous
                            if (row.ind + delta // 5) < anomalyDF.shape[0]:  # get the row for t + delta
                                deltaRow = anomalyDF.iloc[row.ind + delta // 5]
                                if (deltaRow[
                                        nodeNeighbors] == True).sum() >= kNeighbors and checkOnce:  # k Neighbor has flag sample as anomalous, time proximity
                                    checkOnce = False
                                    timeProxStats[delta]['Delay'].append(deltaRow.time - event['startTime'])

                        if checkOnce == False:
                            timeProxStats[delta]['Recall'].append(1)
                            break

                    # lastDetection = 300
                    # counterFalsePositives = 0
                    # # Running algorithm to find precision, recall and false alarms
                    # for r1 in anomalyClearDF.itertuples(index=True):
                    #     if (r1[node_idx] == True):  # event node has flag sample as anomalous
                    #         if (r1.ind + delta // 5) < anomalyClearDF.shape[0]:  # get the row for t + delta
                    #             deltaRow1 = anomalyClearDF.iloc[r1.ind + delta // 5]
                    #             if ((deltaRow1[nodeNeighbors] == True).sum() >= kNeighbors): # and (
                    #                     #r1.time > lastDetection):  # k Neighbor has flag sample as anomalous, time proximity
                    #                 counterFalsePositives += 1
                    #                 lastDetection = r1.time

                    counterFalsePositives = self.proximityAlgo(anomalyClearDF, topology, k)
                    tp = TP.at[delta_lst.index(delta), str(kNeighbors) + '_Neighbor(s)']
                    if counterFalsePositives > 0 and checkOnce == False:
                        timeProxStats[delta]['Precision'].append(tp / (tp + counterFalsePositives))
                    elif counterFalsePositives > 0 and checkOnce == True:
                        timeProxStats[delta]['Precision'].append(0)
                    elif counterFalsePositives == 0 and checkOnce == False:
                        timeProxStats[delta]['Precision'].append(1)
                    elif counterFalsePositives == 0 and checkOnce == True:
                        pass
                    else:
                        print('event :#{}'.format(event))
                        print('K: #{}'.format(k))
                        print('False positives: {}'.format(counterFalsePositives))
                        print('CheckOnce: {}'.format(checkOnce))
                        sys.exit('Problem in Precision K')

                    if counterFalsePositives > 0:
                        timeProxStats[delta]['False'].append(counterFalsePositives)
                    elif counterFalsePositives == 0:
                        timeProxStats[delta]['False'].append(0)
                    else:
                        sys.exit('Problem in False')
                    resultStats[ct][k] = timeProxStats
                    # resultStats[k][delta] = timeProxStats
        return resultStats
        #
