from ClinetA.ClientA import ClientA
import os


def process_A(name, data, config):
    """
    The process of client A, where A communicate with client B and C in each iteration to do secure gradient update.
    :param name: the name of client A
    :param data: training dataset of client A
    :param config: the config dict, including the params for training
    :return: True
    """
    print('A Run task %s (%s)...' % (name, os.getpid()))
    client_A = ClientA(name, data, config)
    # client_A.set_up(host='47.98.255.118', port=27017, db_name='DB_C')
    pro_name = client_A.pro_name
    A_addr = client_A.addr
    B_addr = client_A.B_addr
    C_addr = client_A.C_addr

    while not client_A.data.exit_flag:
        iter_num = client_A.data.iter_num
        print("A iter num: ", iter_num)
        param_dict = {'pro_name': pro_name, 'iter_num': iter_num,
                      'origin_client': C_addr, 'target_client': A_addr}
        client_A.client_sync(C_addr, "public_key", "getPublicKey", param_dict)
        client_A.task_1()
        print("A successfully finished task1")
        param_dict = {'pro_name': pro_name, 'iter_num': iter_num,
                      'origin_client': B_addr, 'target_client': A_addr}
        client_A.client_sync(A_addr, "encrypted_u_b", "getEncryptedWeight", param_dict)
        client_A.task_2()
        print("A successfully finished task2")
        param_dict = {'pro_name': pro_name, 'iter_num': iter_num,
                      'origin_client': C_addr, 'target_client': A_addr}
        client_A.client_sync(C_addr, "masked_dJ_a", "getGradient", param_dict)
        client_A.task_3()
        print("A successfully finished task3")
        if client_A.data.iter_num >= config['n_iter']:
            client_A.data.exit_flag = True
        client_A.data.iter_num += 1
    print("A done")
    return True