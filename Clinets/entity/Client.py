from entity.DataType import DataType
import numpy as np
from phe import paillier
from time import sleep
import pymongo
import requests
import json

class Client:
    PUBLIC_KEY = 0
    ARRAY = 1
    LIST = 2
    ENCRYPTED_NUM = 3
    ENCRYPTED_ARRAY = 4
    def __init__(self, config, addre):
        self.pro_name = config['pro_name']
        self.connections = {}
        self.db = None
        self.data = DataType()
        self.flag = True
        self.config = config
        self.ADDR = addre
        self.name = ""

    def set_up(self, host='127.0.0.1', port=27017, db_name='db'):
        self.set_db(host, port, db_name)
        # os.system(f'python Server.py {host} {port}')
        print(f"{self.name} setting up server successfully!")

    def connect(self, addrs_to_connect):
        for addr in addrs_to_connect:
            client = pymongo.MongoClient(addr[0], addr[1])
            if client is None:
                print("Fail to connect other database!")
            else:
                self.connections[addr] = client
                print("%s connected to %s" % (self.name, str(addr)))

    def set_db(self, host='127.0.0.1', port=27017, db_name='db'):
        client = pymongo.MongoClient(host, port)
        if client is None:
            print("Fail to connect database!")
        else:
            self.db = client[db_name]

    @staticmethod
    def addr_to_str(addr):
        host, port = addr
        return f"{host}:{port}"

    @staticmethod
    def transform_public_key(public_key):
        insert_data = {
            'n': str(public_key.n)
        }
        return insert_data

    @staticmethod
    def transform_array(array):
        return array.tolist()

    @staticmethod
    def transform_encrypted_num(encrypted_num):
        insert_data = [str(encrypted_num.ciphertext()), encrypted_num.exponent]
        return insert_data

    @staticmethod
    def transform_encrypted_array(encrypted_array):
        insert_data = [[str(x.ciphertext()), x.exponent] for x in encrypted_array]
        return insert_data

    @staticmethod
    def get_data_type(data):
        if type(data) is paillier.PaillierPublicKey:
            return Client.PUBLIC_KEY
        elif type(data) is paillier.EncryptedNumber:
            return Client.ENCRYPTED_NUM
        elif type(data) is list and len(data) > 0 and type(data[0]) is paillier.EncryptedNumber:
            return Client.ENCRYPTED_ARRAY
        elif type(data) is list:
            return Client.LIST
        else:
            return Client.ARRAY

    @staticmethod
    def get_stamp(pro_name, iter_num, origin_client, target_client):
        stamp = {
            "pro_name": pro_name,
            "iter_num": iter_num,
            "origin_client": origin_client,
            "target_client": target_client
        }
        return stamp

    def upload_data(self, data, server_addr, method, params):
        url = f"http://{server_addr}/{method}"
        if self.get_data_type(data) == self.ARRAY:
            data = self.transform_array(data)
        data_type = self.get_data_type(data)
        if data_type == self.PUBLIC_KEY:
            print("transforming public_key")
            data = self.transform_public_key(data)
        elif data_type == self.ARRAY:
            print("transforming array")
            data = self.transform_array(data)
        elif data_type == self.ENCRYPTED_NUM:
            print("transforming encrypted_num")
            data = self.transform_encrypted_num(data)
        elif data_type == self.ENCRYPTED_ARRAY:
            print("transforming encrypted_array")
            data = self.transform_encrypted_array(data)
        upload_data = {'content': data}
        requests.post(url, data=json.dumps(upload_data), params=params)

    # def upload_data(self, data, stamp):
    #     upload_data = {}
    #     if self.db is None:
    #         print("Please connect to a database before upload data")
    #     else:
    #         assert type(data) is dict, "data to be uploaded must be a dict"
    #         for key in data.keys():
    #             if self.get_data_type(data[key]) == self.ARRAY:
    #                 data[key] = self.transform_array(data[key])
    #             data_type = self.get_data_type(data[key])
    #             if data_type == self.PUBLIC_KEY:
    #                 print("transforming public_key")
    #                 upload_data[key] = self.transform_public_key(data[key])
    #             elif data_type == self.ARRAY:
    #                 print("transforming array")
    #                 upload_data[key] = self.transform_array(data[key])
    #             elif data_type == self.ENCRYPTED_NUM:
    #                 print("transforming encrypted_num")
    #                 upload_data[key] = self.transform_encrypted_num(data[key])
    #             elif data_type == self.ENCRYPTED_ARRAY:
    #                 print("transforming encrypted_array")
    #                 upload_data[key] = self.transform_encrypted_array(data[key])
    #             else:
    #                 upload_data[key] = data[key]
    #
    #         for key, value in upload_data.items():
    #             data = {}
    #             data.update(stamp)
    #             data['content'] = value
    #             print(f"{self.name} is inserting data {key}...")
    #             self.db[key].insert_one(data)
    #             print(self.name, "successfully upload", key)


    def client_sync(self, server_addr, target_data,  method, params):
        dt = self.data.data
        url = f"http://{server_addr}/{method}"
        print(url)
        while True:
            try:
                r = requests.get(url, params=params)
                print(params)
            except Exception as e:
                # print(f"request error: {e}")
                print(r.status_code, 'error')
            if r.status_code == 200:
                try:
                    # print(r.json())
                    data = r.json()['content']
                    if type(data) is list:
                        public_key = dt['public_key']
                        if type(data[0]) is list:
                            data = [paillier.EncryptedNumber(public_key, int(x[0]), int(x[1])) for x in data]
                            data = np.asarray(data)
                        elif type(data[0]) is float:
                            data = np.asarray(data)
                        else:
                            data = paillier.EncryptedNumber(public_key, int(data[0]), int(data[1]))
                    elif type(data) is dict:
                        data = paillier.PaillierPublicKey(n=int(data['n']))
                    dt.update({target_data: data})
                    break
                except Exception as e:
                    print("fail to transform data error: %s" % e)
                    print(data)
            else:
                print(f"{self.name} failed to run method {method}, waiting....")
                sleep(1)
        print(f"{self.name} successfully finished {method}")


    # def client_sync(self, targets, step, config):
    #     dt = self.data.data
    #     for target in targets:
    #         target_data = target[0]
    #         target_client = target[1]
    #         host, port = config["ADDR_" + target_client]
    #         print(host, port)
    #         url = f"http://{host}:{port}/{target_data}/{self.data.iter_num}_{step}"
    #         print(url)
    #         print(f"{self.name} is looking for {target_data} from {target_client}")
    #         while True:
    #             try:
    #                 r = requests.get(url)
    #                 print(r, r.status_code, 'success')
    #                 sleep(1)
    #             except Exception as e:
    #                 # print(f"request error: {e}")
    #                 print(r.status_code,'error')
    #             if r.status_code == 200:
    #                 try:
    #                     data = r.json()['data']
    #                     if type(data) is list:
    #                         public_key = dt['public_key']
    #                         if type(data[0]) is list:
    #                             data = [paillier.EncryptedNumber(public_key, int(x[0]), int(x[1])) for x in data]
    #                             data = np.asarray(data)
    #                         elif type(data[0]) is float:
    #                             data = np.asarray(data)
    #                         else:
    #                             data = paillier.EncryptedNumber(public_key, int(data[0]), int(data[1]))
    #                     elif type(data) is dict:
    #                         data = paillier.PaillierPublicKey(n=int(data['n']))
    #                     dt.update({target_data: data})
    #                     break
    #                 except Exception as e:
    #                     print("fail to transform data error: %s" % e)
    #                     print(data)
    #             else:
    #                 print(f"{self.name} failed to get {target_data} from {target_client}, waiting....")
    #                 sleep(1)
    #         print(f"{self.name} successfully got {target_data} from {target_client}")



# class TestClient(unittest.TestCase):
#
#     def test_upload_public_key(self):
#         client = Client(1, 1)
#         client.set_db(db_name='vertical_learning')
#         public_key, private_key = paillier.generate_paillier_keypair()
#         client.upload_data({'public_key': public_key}, [0, 0])
#
#     def test_upload_array(self):
#         client = Client(1, 1)
#         client.set_db(db_name='vertical_learning')
#         array = np.array([1,2,3])
#         client.upload_data({'gradient':array}, [0,0])
#
#     def test_upload_encrypted_num(self):
#         client = Client(1, 1)
#         client.set_db(db_name='vertical_learning')
#         public_key, private_key = paillier.generate_paillier_keypair()
#         encrypted_num = public_key.encrypt(3)
#         client.upload_data({'loss': encrypted_num}, [0, 0])
#
#     def test_upload_encrypted_array(self):
#         client = Client(1, 1)
#         client.set_db(db_name='vertical_learning')
#         public_key, private_key = paillier.generate_paillier_keypair()
#         array = [2, 3, 4]
#         encrypted_array = [public_key.encrypt(x) for x in array]
#         client.upload_data({'dJ': encrypted_array}, [0, 0])
#
#
#
# if __name__ == "__main__":
#     # response = requests.get('http://127.0.0.1:8080/vertical_learning/public_key/0')
#     # print(response.content)
#     unittest.main()