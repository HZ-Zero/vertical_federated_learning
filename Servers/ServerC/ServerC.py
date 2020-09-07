import json
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from utils.funct import generate_key_pair
from utils.funct import check_params
from phe import paillier
from entity.data_type import PrivateKey
from threading import Thread

app = Flask(__name__)
app.config['DEBUG'] = True  # 开启 debug
mongo = PyMongo(app, uri="mongodb://localhost:27017/DB_C")


def decrypt_weight(encrypted_gradient, param_dict):
    search_dict = {}
    search_dict.update(param_dict)
    search_dict.pop("target_client")

    private_key_dict = mongo.db.private_key.find_one(search_dict)
    if private_key_dict:
        private_key_dict.pop("_id")
        private_key = PrivateKey(**private_key_dict)
        private_key = private_key.regenerate_object()
        public_key = private_key.public_key
        encrypted_gradient = [paillier.EncryptedNumber(public_key, int(x[0]), int(x[1])) for x in encrypted_gradient]
        gradient = [private_key.decrypt(x) for x in encrypted_gradient]
        gradient_dict = {}
        gradient_dict.update(param_dict)
        gradient_dict.update({'content': gradient})
        mongo.db.gradient.insert_one(gradient_dict)
    else:
        print("fail to find the corresponding private key")
        print(param_dict)


@app.route('/getPublicKey', methods=['GET'])
def get_public_key():
    # 检验参数
    flag = check_params(request, ['pro_name', 'iter_num', 'origin_client', 'target_client'])
    print(request.args.to_dict())
    pro_name: str = request.args.get('pro_name')
    iter_num: int = request.args.get('iter_num')
    origin_client: list = request.args.get('origin_client')
    target_client: list = request.args.get('target_client')
    if not flag:
        return '参数不合法', 400
    param_dict = {'pro_name': pro_name, 'iter_num': iter_num,
                  'origin_client': origin_client}
    # 查看key是否已经生成 已经生成返回
    res = mongo.db.public_key.find_one(param_dict)
    param_dict['target_client'] = target_client
    output = {}
    output.update(param_dict)

    if res:
        output['content'] = res['content']
        return jsonify(output), 200
    else:
        # 没有生成就创建key并返回
        public_key, private_key = generate_key_pair()
        public_key_dict = {}
        public_key_dict.update(param_dict)
        content1 = {'n': str(public_key.n)}
        public_key_dict.update({'content': content1})
        private_key_dict = {}
        private_key_dict.update(param_dict)
        content2 = {'n': str(public_key.n),
                    'p': str(private_key.p),
                    'q': str(private_key.q)}
        private_key_dict.update({'content': content2})
        mongo.db.public_key.insert_one(public_key_dict) #这里会为output加上id属性
        mongo.db.private_key.insert_one(private_key_dict)
        output.update({'content': content1})
        return jsonify(output), 200


@app.route('/saveEncryptedGradient', methods=['POST'])
def save_encrypted_gradient():
    flag = check_params(request, ['pro_name', 'iter_num', 'origin_client', 'target_client'])
    if not flag:
        return '参数不合法', 400
    pro_name: str = request.args.get('pro_name')
    iter_num: int = request.args.get('iter_num')
    origin_client: list = request.args.get('origin_client')
    target_client: list = request.args.get('target_client')
    param_dict = {'pro_name': pro_name, 'iter_num': iter_num,
                  'origin_client': origin_client, 'target_client': target_client}
    insert_data = {}
    insert_data.update(param_dict)
    res = mongo.db.encrypted_gradient.find_one(param_dict)
    if res:
        return "encrypted gradient has been saved", 200
    else:
        content = json.loads(request.data)
        insert_data.update(content)
        mongo.db.encrypted_gradient.insert_one(insert_data)
        param_dict['origin_client'], param_dict['target_client'] = param_dict['target_client'], param_dict['origin_client']
        args = (insert_data['content'], param_dict)
        decryption_thread = Thread(target=decrypt_weight, args=args)
        decryption_thread.start()
        return "successfully save encrypted gradient!", 200


@app.route('/getGradient', methods=['GET'])
def get_gradient():
    flag = check_params(request, ['pro_name', 'iter_num', 'origin_client', 'target_client'])
    if not flag:
        return '参数不合法', 400
    pro_name: str = request.args.get('pro_name')
    iter_num: int = request.args.get('iter_num')
    origin_client: list = request.args.get('origin_client')
    target_client: list = request.args.get('target_client')
    param_dict = {'pro_name': pro_name, 'iter_num': iter_num,
                  'origin_client': origin_client, 'target_client': target_client}
    # 查看key是否已经生成 已经生成返回
    res = mongo.db.gradient.find_one(param_dict)
    output = {}
    output.update(param_dict)
    if res:
        output['content'] = res['content']
        return jsonify(output), 200
    else:
        return "encrypted gradient has not been decrypted yet!", 404


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8083,threaded=False)
