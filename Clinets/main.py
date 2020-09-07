from utils.utils import *
from multiprocessing import Pool
from ClinetA.main import process_A
from ClientB.main import process_B


def vertical_logistic_regression(X, y, X_test, y_test, config):
    """
    Start the processes of the three clients: A, B and C.
    :param X: features of the training dataset
    :param y: labels of the training dataset
    :param X_test: features of the test dataset
    :param y_test: labels of the test dataset
    :param config: the config dict
    :return: True
    """
    XA, XB, XA_test, XB_test = vertically_partition_data(X, X_test, config['A_idx'], config['B_idx'])
    print('XA:', XA.shape, '   XB:', XB.shape)

    p = Pool(2)  # Init a pool that can run 2 processes concurrently.
    p.apply_async(process_A, args=("A", XA, config))    # apply_async是异步非阻塞的
    p.apply_async(process_B, args=("B", XB, y, config))
    print("All process initialized")
    p.close()
    print("All process done1.")
    p.join()
    print("All process done2.")
    return True

if __name__ == '__main__':
    HOST = "127.0.0.1"
    REMOTE = "47.98.255.118"
    ADDR_A = (REMOTE, 9090)
    ADDR_B = (HOST, 8081)
    ADDR_C = (REMOTE, 9093)

    config = {
        'pro_name': 'pro_0908',
        'n_clients': 1,
        'key_length': 512,
        'n_iter': 30,
        'lambda': 10,
        'lr': 0.05,
        'BGD': False,
        'batch_size': 1000,
        'pause_time': 0.001,
        'A_idx': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        'B_idx': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        'ADDR_A': ADDR_A,
        'ADDR_B': ADDR_B,
        'ADDR_C': ADDR_C,
    }

    X, y, X_test, y_test = split_train_test()
    print(X.shape, y.shape, X_test.shape, y_test.shape)
    vertical_logistic_regression(X, y, X_test, y_test, config)