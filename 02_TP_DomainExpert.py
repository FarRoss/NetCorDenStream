#!/usr/bin/python3
# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] January, 25th 2020.

import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "DenStream"))
sys.path.append(os.path.join(os.path.dirname(__file__), "Bravo"))

# Import libraries and files
import json
import pandas as pd
from readGroundTruth import groundTruth
from timeProximity_Delta_k import timeproximity

# load variables
config = json.load(open('config.json'))

kNeighbors_lst = config['KNeighbors']
delta_lst = config['delta_lst']

baseNodes = config['baseNodes']
features = config['featureModel']

t = [0.99, 0.95, 0.90, 0.85, 0.80]

timeProxDF = {}

# Depending on the networkCorrelation we call the respective Network Correlation algorithm
for baseNode in baseNodes:
    print(baseNode)
    for dataset in config['dataset']['availableDataset']:
        print(dataset)

        truth = groundTruth('GrounTruth/' + dataset + '.txt', fileType='csv')

        # Depending on the networkCorrelation we call the respective Network Correlation algorithm
        if config['networkCorrelation'] == 'timeProximity':
            # Call the time proximity function

            timeProx_result = {}
            timeProx_result['delta'] = delta_lst
            for kNeighbors in kNeighbors_lst:
                timProx_lst = []
                for delta in delta_lst:
                    topology = config['topology']
                    timeProximity = timeproximity(baseNode, truth, delta)
                    timeProxAlarms = timeProximity.proximity(topology, kNeighbors, dataset)
                    timeProxDF[baseNode] = timeProxAlarms
                    timProx_lst.append(timeProxAlarms)
                print(delta_lst)
                print(timProx_lst)
                timeProx_result[str(kNeighbors) + '_Neighbor(s)'] = timProx_lst
            dfTmp = pd.DataFrame.from_dict(timeProx_result)
            dfTmp.to_csv(os.getcwd() + '/TimeProximityResults/' + 'baseNode' + '_' + baseNode + '/' +
                         features + '/' + dataset + '.csv', index=False)
