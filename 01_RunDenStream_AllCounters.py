#!/usr/bin/python3
# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] January, 25th 2020.

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "DenStream"))
sys.path.append(os.path.join(os.path.dirname(__file__), "Bravo"))

### MATH, TIME, JSON
import json
import time
import pandas as pd

### Anomaly DenStream Algorithm library
from sample import Sample
from DenStream import DenStream

from readGroundTruth import groundTruth


def normalize_matrix(df):
    return (df - df.mean()) / df.std()


def main(configuration):
    totalExecutionTime = []

    for dataset in configuration['dataset']['availableDataset']:
        print(dataset + '\n')

        truth = groundTruth('GrounTruth/' + dataset + '.txt', fileType='csv')

        for node in configuration['nodes']:
            print('Dataset {} - Node: {} loading ...'.format(dataset, node))

            df = pd.read_csv(configuration['dataset']['path'] + node + dataset + '.csv', low_memory=False).dropna() \
                .drop('Unnamed: 0', axis=1)
            print('Done.')

            times = df['time'].astype('int')
            df = df.drop(['time'], axis=1)

            # Without bravo
            df = df.loc[:, df.std() != 0]
            dfNormalized = normalize_matrix(df).dropna(axis=1)

            bufferDF = dfNormalized[0: configuration['sampleSkip']]
            testDF = dfNormalized[configuration['sampleSkip']:]

            # Anomaly DenStream initialization with the parameters in the configuration file
            aden = DenStream(lamb=configuration['denstreamParameters']['lambda'],
                             epsilon=configuration['denstreamParameters']['epsilon'],
                             beta=configuration['denstreamParameters']['beta'],
                             mu=configuration['denstreamParameters']['mu'],
                             startingBuffer=bufferDF,
                             tp=configuration['denstreamParameters']['tp'])
            aden.runInitialization()

            print('Running algorithm ...')
            outputCurrentNode = []
            startingSimulation = time.time()
            for sampleNumber in range(len(testDF)):
                sample = testDF.iloc[sampleNumber]
                result = aden.runOnNewSample(Sample(sample.values, times.iloc[sampleNumber]))
                outputCurrentNode.append(result)
            endSimulation = time.time() - startingSimulation
            totalExecutionTime.append(endSimulation)
            print('Done in {}'.format(endSimulation))

            df['result'] = [False] * configuration['sampleSkip'] + outputCurrentNode

            print("Number of anomalies in " + str(node) + " is: ", outputCurrentNode.count(True),
                  len(outputCurrentNode))

            if configuration['detectionCriterion'] == 'spatialDetection':
                df['time'] = times
                df[['result', 'time']].to_csv('Data/ResultsSpatialDetection/' + configuration[
                    'featureModel'] + '/' + dataset + '_DENSTREAM_' + node + '.csv', sep=',')
    return aden, truth, df, times, dfNormalized, testDF


if __name__ == "__main__":
    configuration = json.load(open('config.json'))
    aden, truth, df, times, dfNorm, testDF = main(configuration)
