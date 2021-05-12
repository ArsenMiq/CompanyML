import pandas as pd
import numpy as np


def readCSV(filename):
    data = pd.read_csv(filename)
    return (np.array(data))


def trainingData(filename, start, end):
    train_data = readCSV(filename)
    return train_data[start:end, :114]


def testingData(filename, start, end):
    test_data = readCSV(filename)
    return test_data[start:end, :114]


def getHeaderList(filename):
    data = pd.read_csv(filename)
    list_of_column_names = list(data.columns)
    return list_of_column_names
