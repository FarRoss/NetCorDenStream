#!/usr/bin/python3
# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] January, 25th 2020.

# Import libraries
import json
import pandas as pd
import os, sys
import time
from utils import *
from set_paths import *
from prettytable import PrettyTable
from pathlib import Path
import sklearn.preprocessing as sk
import logging

config = json.load(open('config.json'))

t = [0.99, 0.95, 0.90, 0.85, 0.80]


# Function to split telemetry data if multiple router send data.
def split_by_node(data_frame, node_col=None):
    if node_col in list(data_frame):
        node_names = list(set(data_frame[node_col]))
        node_metrics = {}
        for name in node_names:
            node_metrics[name] = data_frame[data_frame[node_col] == name]
    else:
        node_metrics = {'single_node': data_frame}
    return node_metrics


# fill_method='pad','linear','nearest')
def check_fill_missing(dataFrame, fill_method='pad'):
    nan_mask = dataFrame.isna()
    for col_name in list(dataFrame):
        if True in nan_mask[col_name].values:
            missing_index = np.where(nan_mask[col_name].values == True)
            logging.warning('Missing value in telemetry %s. Filling in Nan by padding', col_name)
            print('Missing and filling in values at indexes:', missing_index)
            dataFrame[col_name] = dataFrame[col_name].interpolate(method=fill_method)
    return dataFrame


def CategoricalCols(dataFrame):
    cols = dataFrame.columns
    num_cols = dataFrame._get_numeric_data().columns
    cat_cols = list(set(cols) - set(num_cols))
    cols_lst = list(dataFrame.columns)
    cat_cols_index = []  # List index of cateforical columns is returned
    for i in cat_cols:
        cat_cols_index.append(cols_lst.index(i))
    label_encoder = sk.LabelEncoder()
    for item in cat_cols_index:
        dataFrame.iloc[:, int(item)] = label_encoder.fit_transform(dataFrame.iloc[:, int(item)])
    return dataFrame


# corr_method = {pearson, kendall, spearman}
def correlate(data_frame, corr_method='pearson', threshold=0.999):
    corr = data_frame.corr(method=corr_method)

    # Columns to remove based on threshold
    cols_to_remove = []
    for i in range(corr.shape[0]):
        for j in range(i + 1, corr.shape[0]):
            if corr.iloc[i, j] >= threshold:
                cols_to_remove.append(corr.columns[j])
    cols_to_remove = list(set(cols_to_remove))
    return cols_to_remove


def remove_identical_columns(dataFrame):
    col_names = list(dataFrame)
    names_to_remove = []
    for i in range(len(col_names)):
        for j in range(i + 1, len(col_names)):
            if dataFrame[col_names[i]].equals(dataFrame[col_names[j]]):
                names_to_remove.append(col_names[j])
    return names_to_remove


def remove_same_value(dataFrame):
    data_size = dataFrame.shape[0]
    col_names = list(dataFrame)
    nunique = dataFrame.apply(pd.Series.nunique)
    col_to_drop = nunique[nunique == 1].index
    return dataFrame.drop(col_to_drop, axis=1)


# preprocess the data
def preprocessPipeline(df, threshold):
    # ---------------------Remove columns with values not changing.
    node_data = remove_same_value(df)

    # ---------------------Check and fill missing values <methods: linear, index, nearest, zero, slinear, quadratic, krogh, from_derivatives.
    node_data = check_fill_missing(node_data, fill_method='pad')

    # ---------------------remove identical columns
    node_data = node_data.drop(columns=remove_identical_columns(node_data))

    # ---------------------Categorize the data
    CategoricalCols(node_data)

    # ---------------------Data Visualization
    # print(node_data.head(3))
    # visualize(node_data, node_name, visualKey='BoxPlot')

    # ---------------------Data correlation
    cols = correlate(node_data, corr_method='pearson', threshold=threshold)
    node_data = node_data[cols]
    return node_data


if __name__ == "__main__":
    for node in config['nodes']:
        for dataset in config['dataset']['availableDataset']:
            print(dataset)
            exec_time = []
            table = PrettyTable()
            f_name = str(Path(__file__).parent.parent) + '/Data/DatasetByNodes/' + node + dataset + '.csv'
            print(f_name)
            if os.path.isfile(f_name):
                df = pd.read_csv(f_name, low_memory=False).drop('Unnamed: 0', axis=1)

                times = df['time'].astype('int')
                df = df.drop(['time'], axis=1)

                for threshold in t:
                    startProcessTime = time.time()
                    precessed_df = preprocessPipeline(df, threshold)
                    endProcessTime = time.time() - startProcessTime
                    new_df = (precessed_df - precessed_df.mean()) / precessed_df.std()
                    exec_time.append(endProcessTime)
                    process_file = DATA_FOLDER + node + dataset + '_' + str(threshold) + '.csv'
                    if os.path.isfile(f_name):
                        new_df.insert(0, 'Time', times.values)
                        new_df.to_csv(process_file, sep=',')
                table.add_column('threshold', t)
                table.add_column('Execution Time', exec_time)
                data = table.get_string()
                results = DATA_FOLDER + 'results_' + node + dataset + '.txt'
                with open(results, 'w') as f:
                    f.write(data)
            else:
                print('{} does now exist'.format(f_name))
        #     break
        # break
