from entity.Client import Client
import numpy as np

class ClientA(Client):
    def __init__(self, name, X, config):
        super().__init__(config, config['ADDR_A'])
        self.name = name
        self.X = X
        self.weights = np.zeros(X.shape[1])
        self.addr = self.addr_to_str(config['ADDR_A'])
        self.B_addr = self.addr_to_str(config['ADDR_B'])
        self.C_addr = self.addr_to_str(config['ADDR_C'])
        self.BGD = config['BGD']
        self.batch_size = config['batch_size']
        self.X_b = None

    def compute_z_a(self):
        if self.BGD:
            total_size = len(self.X) - (len(self.X) % self.batch_size)
            start = self.data.iter_num * self.batch_size % total_size
            self.X_b = self.X[start: start + self.batch_size]
            z_a = np.dot(self.X_b, self.weights)
        else:
            z_a = np.dot(self.X, self.weights)
        return z_a

    def get_encrypted_dJ_a(self, encrypted_u):
        if self.BGD:
            encrypted_dJ_a = self.X_b.T.dot(encrypted_u) + self.config['lambda'] * self.weights
        else:
            encrypted_dJ_a = self.X.T.dot(encrypted_u) + self.config['lambda'] * self.weights
        return encrypted_dJ_a

    def update_weight(self, dJ_a):
        if self.BGD:
            self.weights = self.weights - self.config["lr"] * dJ_a / self.batch_size
        else:
            self.weights = self.weights - self.config["lr"] * dJ_a / len(self.X)
        return

    def task_1(self):
        dt = self.data.data
        assert "public_key" in dt.keys(), "Error: 'public_key' from C in step 1 not successfully received."
        public_key = dt['public_key']
        z_a = self.compute_z_a()
        u_a = 0.25 * z_a
        # z_a_square = z_a ** 2
        encrypted_u_a = [public_key.encrypt(x) for x in u_a]
        # encrypted_z_a_square = [public_key.encrypt(x) for x in z_a_square]
        self.data.data.update({"encrypted_u_a": encrypted_u_a})
        stamp = self.get_stamp(self.pro_name, self.data.iter_num, self.addr, self.B_addr)
        print("A is uploading encrypted_u_a...")
        self.upload_data(encrypted_u_a, self.addr, "saveEncryptedWeight", stamp)
        print("A successfully uploaded encrypted_u_a")
        # self.upload_data(encrypted_z_a_square, "encrypted_z_a_square", stamp)

    def task_2(self):
        dt = self.data.data
        assert "encrypted_u_b" in dt.keys(), "Error: 'encrypted_u_b' from B in step 1 not successfully received."
        encrypted_u_b = dt['encrypted_u_b']
        encrypted_u = encrypted_u_b + dt['encrypted_u_a']
        encrypted_dJ_a = self.get_encrypted_dJ_a(encrypted_u)
        mask = np.random.rand(len(encrypted_dJ_a))
        encrypted_masked_dJ_a = encrypted_dJ_a + mask
        self.data.data.update({"mask": mask})
        stamp = self.get_stamp(self.pro_name, self.data.iter_num, self.addr, self.C_addr)
        self.upload_data(encrypted_masked_dJ_a, self.C_addr, "saveEncryptedGradient", stamp)

    def task_3(self):
        dt = self.data.data
        assert "masked_dJ_a" in dt.keys(), "Error: 'masked_dJ_a' from C in step 2 not successfully received."
        masked_dJ_a = dt['masked_dJ_a']
        dJ_a = masked_dJ_a - dt['mask']
        self.update_weight(dJ_a)
        print("A weight %d : " % self.data.iter_num, self.weights)
        return
