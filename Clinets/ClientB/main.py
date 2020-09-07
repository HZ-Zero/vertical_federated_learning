from ClientB.ClientB import ClientB
from time import sleep
import os
def process_B(name, X, y, config):
    """
    The process of client A, where A communicate with client B and C in each iteration to do secure gradient update.
    :param name: the name of client B
    :param X: features of the training dataset of client B
    :param y: labels of the training dataset of client B
    :param config: the config dict
    :return: True
    """
    print('B Run task %s (%s)...' % (name, os.getpid()))
    client_B = ClientB(name, X, y, config)
    pro_name = client_B.pro_name
    A_addr = client_B.A_addr
    B_addr = client_B.addr
    C_addr = client_B.C_addr
    while not client_B.data.exit_flag:
        iter_num = client_B.data.iter_num

        param_dict = {'pro_name': pro_name, 'iter_num': iter_num,
                      'origin_client': C_addr, 'target_client': B_addr}
        client_B.client_sync(C_addr, "public_key", "getPublicKey", param_dict)
        client_B.task_1()
        print("B successfully finished task1")
        param_dict = {'pro_name': pro_name, 'iter_num': iter_num,
                      'origin_client': A_addr, 'target_client': B_addr}
        client_B.client_sync(A_addr, "encrypted_u_a", "getEncryptedWeight", param_dict)
        client_B.task_2()
        print("B successfully finished task2")
        param_dict = {'pro_name': pro_name, 'iter_num': iter_num,
                      'origin_client': C_addr, 'target_client': B_addr}
        client_B.client_sync(C_addr, "masked_dJ_b", "getGradient", param_dict)
        print("B successfully finished task3")
        client_B.task_3()

        if client_B.data.iter_num >= config['n_iter']:
            client_B.data.exit_flag = True
        client_B.data.iter_num += 1
    print("B done")
    return True
