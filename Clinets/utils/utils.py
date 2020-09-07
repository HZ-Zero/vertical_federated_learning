import numpy as np
import pandas as pd
from sklearn import datasets
import time
from contextlib import contextmanager
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_breast_cancer
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle


@contextmanager
def timer():
    """Helper for measuring runtime"""

    time0 = time.perf_counter()
    yield
    print('[elapsed time: %f s]' % (time.perf_counter() - time0))


def split_train_test():
    # 加载数据
    breast = load_breast_cancer()

    # 数据拆分
    X_train, X_test, y_train, y_test = train_test_split(breast.data, breast.target, random_state=1)

    # 数据标准化
    std = StandardScaler()
    X_train = std.fit_transform(X_train)
    X_test = std.transform(X_test)
    return X_train, y_train, X_test, y_test


def split_train_test1():
    # 加载数据
    iris = datasets.load_iris()

    X = iris.data
    y = (iris.target != 0) * 1

    # 数据拆分
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    # 数据标准化
    std = StandardScaler()
    X_train = std.fit_transform(X_train)
    X_test = std.transform(X_test)
    return X_train, y_train, X_test, y_test


def split_train_test2():
    digits = load_digits()
    data = digits.data
    target = digits.target
    target = np.array([num % 2 for num in target])
    X_train, X_test, y_train, y_test = train_test_split(data, target, random_state=1)
    std = StandardScaler()
    X_train = std.fit_transform(X_train)
    X_test = std.transform(X_test)
    return X_train, y_train, X_test, y_test


def vertically_partition_data(X, X_test, A_idx, B_idx):
    """
    Vertically partition feature for party A
    and B
    :param X: train feature
    :param X_test: test feature
    :param A_idx: feature index of party A
    :param B_idx: feature index of party B
    :return: train data for A, B; test data for A, B
    """
    XA = X[:, A_idx]  # Extract A's feature space
    XB = X[:, B_idx]  # Extract B's feature space
    XB = np.c_[np.ones(X.shape[0]), XB]
    XA_test = X_test[:, A_idx]
    XB_test = X_test[:, B_idx]
    XB_test = np.c_[np.ones(XB_test.shape[0]), XB_test]
    return XA, XB, XA_test, XB_test


def log_data(data, file_name):
    """
    log data into the given file_name
    :param data: data to be logged
    :param file_name: log file name
    :return: 
    """
    try:
        with open(file_name, "a+") as des:
            des.write(data)
    except Exception as e:
        print(e)
        exit()


def load_data(file_name1, file_name2):

    X = pd.read_csv(file_name1)
    y = pd.read_csv(file_name2)
    X, y = shuffle(X, y, random_state=10)
    return X.values, y.TARGET
