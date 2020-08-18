#!/usr/bin/python3
# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] January, 25th 2020.

import os, sys
from scipy import stats
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "DenStream"))
sys.path.append(os.path.join(os.path.dirname(__file__), "Bravo"))

# Import libraries and files
import json
import os
# from Bravo import preprocessPipeline
from readGroundTruth import groundTruth
from timeProximity_k_Delta import timeproximity

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
            for i in range(1, 6):
                prfd = {}
                if len(results[0][i][5]['Precision']) and len(results[0][i][15]['Precision']) \
                        and len(results[0][i][30]['Precision']) and \
                        len(results[0][i][40]['Precision']) and len(results[0][i][55]['Precision']) > 1:
                    prfd["Precision"] = [np.mean([t for t in results[0][i][5]["Precision"] if t > 0]),
                                         np.mean([t for t in results[0][i][15]["Precision"] if t > 0]),
                                         np.mean([t for t in results[0][i][30]["Precision"] if t > 0]),
                                         np.mean([t for t in results[0][i][40]["Precision"] if t > 0]),
                                         np.mean([t for t in results[0][i][55]["Precision"] if t > 0])]
                    if len(results[0][i][5]['Recall']) and len(results[0][i][15]['Recall']) \
                            and len(results[0][i][30]['Recall']) and \
                            len(results[0][i][40]['Recall']) and len(results[0][i][55]['Recall']) > 1:
                        prfd["Recall"] = [np.mean(results[0][i][5]['Recall']),
                                          np.mean(results[0][i][15]['Recall']),
                                          np.mean(results[0][i][30]['Recall']),
                                          np.mean(results[0][i][40]['Recall']),
                                          np.mean(results[0][i][55]['Recall'])]
                    if len(results[0][i][5]['False']) and len(results[0][i][15]['False']) \
                            and len(results[0][i][30]['False']) and len(results[0][i][40]['False']) \
                            and len(results[0][i][55]['False']) > 1:
                        prfd["False"] = [np.mean(results[0][i][5]['False']),
                                         np.mean(results[0][i][15]['False']),
                                         stats.gmean(results[0][i][30]['False']),
                                         stats.gmean(results[0][i][40]['False']),
                                         stats.hmean([t for t in results[0][i][55]['False'] if t > 0])]
                    if len(results[0][i][5]['Delay']) and len(results[0][i][15]['Delay']) \
                            and len(results[0][i][30]['Delay']) and len(results[0][i][40]['Delay']) \
                            and len(results[0][i][55]['Delay']) > 1:
                        prfd["Delay"] = [np.mean(results[0][i][5]['Delay']),
                                         np.mean(results[0][i][15]['Delay']),
                                         np.mean(results[0][i][30]['Delay']),
                                         np.mean(results[0][i][40]['Delay']),
                                         np.mean(results[0][i][55]['Delay'])]

                if len(list(prfd.keys())) > 1:
                    delta_prf[i] = prfd

            # Save results into the /TimeProximityResults folder
            with open(path + 'baseNode_' + baseNode + '/' + features + '/' + 'k_Delta' + '/' + str(threshold) +
                      '_TP_' + dataset + '.json', 'w') as outfile:
                json.dump(delta_prf, outfile, indent=2)
                print('Saved {}'.format(outfile))
            outfile.close()
