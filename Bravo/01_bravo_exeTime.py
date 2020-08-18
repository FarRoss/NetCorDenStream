#!/usr/bin/python3
# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] January, 25th 2020.

# Import libraries
import json
import pandas as pd
import time
from set_paths import *
from prettytable import PrettyTable
from Bravo.bravo import *

data_config = json.load(open('sensor_groups.json'))

# Defining constants
N = [50000, 100000, 150000, 200000, 250000]
N = [700000, 900000, 1100000, 1300000, 1500000]
h = False

if __name__ == "__main__":

    for dataset in data_config['fileName']:
        table = PrettyTable()
        stream_length = []
        data_set = []
        exec_time = []

        f_name = RAWDATA_FOLDER + dataset

        if os.path.isfile(f_name):
            print(f_name)
            df = pd.read_csv(f_name, low_memory=False)

            times = df['time']
            df = df.drop(['time'], axis=1)

            if df.shape[0] > 1500000:
                for threshold in t:
                    for n in N:
                        print(n)
                        h = True
                        startProcessTime = time.time()
                        precessed_df = preprocessPipeline(df.head(n), threshold)
                        endProcessTime = time.time() - startProcessTime
                        exec_time.append(endProcessTime)
                        data_set.append(dataset + '_' + str(threshold))
                        stream_length.append(n)
                table.add_column('Data Set', data_set)
                table.add_column('Stream Length', stream_length)
                table.add_column('Execution Time', exec_time)
                data = table.get_string()
                results = RAWDATA_FOLDER + 'results_' + dataset + '.txt'
                with open(results, 'w') as f:
                    f.write(data)
                    print('-------> {} is saved'.format(results))
        else:
            print('{} does now exist'.format(f_name))
        if h:
            break
