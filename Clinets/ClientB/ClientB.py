from entity.Client import Client
import numpy as np


class ClientB(Client):
    def __init__(self, name, X, y, config):
        super().__init__(config, config['ADDR_B'])
        self.name = name
        self.X = X
        self.y = y
        self.weights = np.zeros(X.shape[1])  # np.random.rand(X.shape[1]) * 2 - 1
        self.sum_X = np.sum(X, 0)
        self.addr = self.addr_to_str(config["ADDR_B"])
        self.A_addr = self.addr_to_str(config["ADDR_A"])
        self.C_addr = self.addr_to_str(config['ADDR_C'])
        self.BGD = config['BGD']
        self.batch_size = config['batch_size']
        self.X_b = None
        self.y_b = None


    def get_weights(self):
        return self.weights

    def set_weights(self, weights):
        self.weights = weights

    def compute_u_b(self):
        if self.BGD:
            total_size = len(self.X) - (len(self.X) % self.batch_size)
            start = self.data.iter_num * self.batch_size % total_size
            self.X_b = self.X[start: start + self.batch_size]
            self.y_b = self.y[start: start + self.batch_size]
            z_b = np.dot(self.X_b, self.weights)
            u_b = 0.25 * z_b - self.y_b + 0.5
        else:
            z_b = np.dot(self.X, self.weights)
            u_b = 0.25 * z_b - self.y + 0.5
        return z_b, u_b

    def compute_encrypted_dJ_b(self, encrypted_u):
        if self.BGD:
            encrypted_dJ_b = self.X_b.T.dot(encrypted_u) + self.config['lambda'] * self.weights
        else:
            encrypted_dJ_b = self.X.T.dot(encrypted_u) + self.config['lambda'] * self.weights
        return encrypted_dJ_b

    def update_weights(self, dJ_b):
        if self.BGD:
            self.weights = self.weights - self.config["lr"] * dJ_b / self.batch_size
        else:
            self.weights = self.weights - self.config["lr"] * dJ_b / len(self.X)

    def task_1(self):
        try:
            dt = self.data.data
            assert "public_key" in dt.keys(), "Error: 'public_key' from C in step 1 not successfully received."
            public_key = dt['public_key']
        except Exception as e:
            print("B step 1 exception: %s" % e)
        try:
            z_b, u_b = self.compute_u_b()
            encrypted_u_b = [public_key.encrypt(x) for x in u_b]
            self.data.data.update({"encrypted_u_b": encrypted_u_b})
            self.data.data.update({"z_b": z_b})
        except Exception as e:
            print("Wrong 1 in B: %s" % e)

        stamp = self.get_stamp(self.pro_name, self.data.iter_num, self.addr, self.A_addr)
        self.upload_data(encrypted_u_b, self.A_addr, "saveEncryptedWeight", stamp)

    def task_2(self):
        try:
            dt = self.data.data
            assert "encrypted_u_a" in dt.keys(), "Error: 'encrypt_u_a' from A in step 1 not successfully received."
            encrypted_u_a = dt['encrypted_u_a']
            encrypted_u = encrypted_u_a + dt['encrypted_u_b']
            encrypted_dJ_b = self.compute_encrypted_dJ_b(encrypted_u)
            mask = np.random.rand(len(encrypted_dJ_b))
            encrypted_masked_dJ_b = encrypted_dJ_b + mask
            self.data.data.update({"mask": mask})
        except Exception as e:
            print("B step 2 exception: %s" % e)

        stamp = self.get_stamp(self.pro_name, self.data.iter_num, self.addr, self.C_addr)
        self.upload_data(encrypted_masked_dJ_b, self.C_addr, "saveEncryptedGradient", stamp)

    def task_3(self):
        try:
            dt = self.data.data
            assert "masked_dJ_b" in dt.keys(), "Error: 'masked_dJ_b' from C in step 2 not successfully received."
            masked_dJ_b = dt['masked_dJ_b']
            dJ_b = masked_dJ_b - dt['mask']
            self.update_weights(dJ_b)
        except Exception as e:
            print("A step 3 exception: %s" % e)
        print("B weight %d : " % self.data.iter_num, self.weights)
        return
