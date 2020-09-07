from phe import PaillierPublicKey
from phe import PaillierPrivateKey

class BaseData:
    Normal_Array = "NormalArray"
    Public_Key = "PublicKey"
    Encrypted_Num = "EncryptedNum"
    Encrypted_Array = "EncryptedArray"

    def __init__(self, pro_name: str,
                 iter_num: str,
                 origin_client: str,
                 target_client: str,
                 content):
        self.pro_name = pro_name
        self.iter_num = iter_num
        self.origin_client = origin_client
        self.target_client = target_client
        self.content = content

    def to_dict(self):
        res = {
            "pro_name": self.pro_name,
            "iter_num": self.iter_num,
            "origin_client": self.origin_client,
            "target_client": self.target_client,
            "data_type": self.data_type,
            "content": self.content
        }
        return res


class PublicKey(BaseData):
    def __init__(self):
        super().__init__()

    def regenerate_object(self) -> PaillierPublicKey:
        n = self.content['n']
        return PaillierPublicKey(int(n))


class PrivateKey(BaseData):
    def __init__(self, pro_name: str,
                 iter_num: str,
                 origin_client: str,
                 target_client: str,
                 content):
        super().__init__(pro_name, iter_num, origin_client, target_client, content)

    def regenerate_object(self) -> PaillierPrivateKey:
        n = self.content['n']
        p = self.content['p']
        q = self.content['q']
        public_key = PaillierPublicKey(int(n))
        return PaillierPrivateKey(public_key, int(p), int(q))


class EncryptedNum(BaseData):

    def __init__(self):
        super().__init__()

    def regenerate_object(self):
        encrypted_array = self.content
        return [[str(x.ciphertext()), x.exponent] for x in encrypted_array]


class EncryptedArray(BaseData):
    def __init__(self):
        super().__init__()

    def regenerate_object(self):
        pass


class NormalArray(BaseData):
    def __init__(self):
        super().__init__()

    def regenerate_object(self):
        pass
