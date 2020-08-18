#!/usr/bin/python3
# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] January, 25th 2020.

import os, sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "DenStream"))
sys.path.append(os.path.join(os.path.dirname(__file__), "Bravo"))

# Import libraries and files
import json
import os
# from Bravo import preprocessPipeline
from readGroundTruth import groundTruth
from timeProximity_Delta_k import timeproximity

# load variables
config = json.load(open('config.json'))

path = 'TimeProximityResults/'
features = config['featureModel']

kNeighbors_lst = config['KNeighbors']
delta_lst = config['delta_lst']

baseNodes = config['baseNodes']
features = config['featureModel']

topo = config['topology']

timeProxDF = {}
t = [0.99, 0.95, 0.90, 0.85, 0.80]

delta = 60
# timProx = timeproximity(baseNode, truth, delta)

# get the precision, false +ve and recalls.
results = {}

d_lst = [5, 15, 30, 40, 55]

for baseNode in baseNodes:
    print(baseNode)
    for dataset in config['dataset']['availableDataset']:
        print(dataset)
        for threshold in t:
            print(threshold)
            truth = groundTruth('GrounTruth/' + dataset + '.txt', fileType='csv')
            timProx = timeproximity(baseNode, truth, delta)
            results = timProx.getStats(topo, kNeighbors_lst, delta_lst, dataset, threshold)

            delta_prf = {}
            for i in d_lst:
                prfd = {}
                if len(results[0][i][5]['Precision']) and len(results[0][i][4]['Precision']) \
                        and len(results[0][i][3]['Precision']) and \
                        len(results[0][i][2]['Precision']) and len(results[0][i][1]['Precision']) > 1:
                    prfd["Precision"] = [max(results[0][i][1]['Precision']),
                                         max(results[0][i][2]['Precision']),
                                         max(results[0][i][3]['Precision']),
                                         max(results[0][i][4]['Precision']),
                                         max(results[0][i][5]['Precision'])]
                    if len(results[0][i][1]['Recall']) and len(results[0][i][2]['Recall']) \
                            and len(results[0][i][3]['Recall']) and \
                            len(results[0][i][4]['Recall']) and len(results[0][i][5]['Recall']) > 1:
                        prfd["Recall"] = [np.mean(results[0][i][1]['Recall']),
                                          np.mean(results[0][i][2]['Recall']),
                                          np.mean(results[0][i][3]['Recall']),
                                          np.mean(results[0][i][4]['Recall']),
                                          np.mean(results[0][i][5]['Recall'])]
                    if len(results[0][i][1]['False']) and len(results[0][i][2]['False']) \
                            and len(results[0][i][3]['False']) and len(results[0][i][4]['False']) \
                            and len(results[0][i][5]['False']) > 1:
                        prfd["False"] = [np.mean(results[0][i][1]['False']),
                                         np.mean(results[0][i][2]['False']),
                                         np.mean(results[0][i][3]['False']),
                                         np.mean(results[0][i][4]['False']),
                                         np.mean(results[0][i][5]['False'])]
                    if len(results[0][i][1]['Delay']) and len(results[0][i][2]['Delay']) \
                            and len(results[0][i][3]['Delay']) and len(results[0][i][4]['Delay']) \
                            and len(results[0][i][5]['Delay']) > 1:
                        prfd["Delay"] = [np.mean(results[0][i][1]['Delay']),
                                         np.mean(results[0][i][2]['Delay']),
                                         np.mean(results[0][i][3]['Delay']),
                                         np.mean(results[0][i][4]['Delay']),
                                         np.mean(results[0][i][5]['Delay'])]

                if len(list(prfd.keys())) > 1:
                    delta_prf[i] = prfd

            # Save results into the /TimeProximityResults folder
            with open(path + 'baseNode_' + baseNode + '/' + features + '/' + 'Delta_k' + '/' + str(threshold) +
                      '_TP_' + dataset + '.json', 'w') as outfile:
                json.dump(delta_prf, outfile, indent=2)
                print('Saved {}'.format(outfile))
            outfile.close()
