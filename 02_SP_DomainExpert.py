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
from signProximity import signproximity

# load variables
config = json.load(open('config.json'))

kNeighbors_lst = config['KNeighbors']
delta_lst = config['delta_lst']

baseNodes = config['baseNodes']
feature = config['featureModel']

networkNodes = config['nodes']
featureList = config['featureList']

t = [0.99, 0.95, 0.90, 0.85, 0.80]

timeProxDF = {}

# Depending on the networkCorrelation we call the respective Network Correlation algorithm
for baseNode in baseNodes:
    print(baseNode)
    for dataset in config['dataset']['availableDataset']:
        print(dataset)

        truth = groundTruth('GrounTruth/' + dataset + '.txt', fileType='csv')

        # Depending on the networkCorrelation we call the respective Network Correlation algorithm
        if config['networkCorrelation'] == 'signProximity':
            # Call the time proximity function

            timeProx_result = {}
            timeProx_result['delta'] = delta_lst
            for kNeighbors in kNeighbors_lst:
                timProx_lst = []
                for delta in delta_lst:
                    topology = config['topology']
                    SP = signproximity(baseNode, truth, delta, feature)
                    SP.proximity(topology, kNeighbors, dataset, featureList, networkNodes)
