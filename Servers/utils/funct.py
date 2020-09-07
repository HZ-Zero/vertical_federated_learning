from phe import paillier


def generate_key_pair():
    try:
        public_key, private_key = paillier.generate_paillier_keypair()
        public_key = public_key
    except Exception as e:
        print("generPublicKey error")
        return 0
    return public_key, private_key


def check_params(request, params):
    for i in params:
        if request.args.get(i):
            continue
        else:
            print(i)
            return False
    return True