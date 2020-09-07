import json
from flask import Flask
from flask import request
from flask import jsonify
from flask_pymongo import PyMongo
from utils.funct import check_params


app = Flask(__name__)
app.config['DEBUG'] = True  # 开启 debug
mongo = PyMongo(app, uri="mongodb://localhost:27017/DB_C")



@app.route('/saveEncryptedWeight', methods=['POST'])
def save_encrypted_gradient():
    flag = check_params(request, ['pro_name', 'iter_num', 'origin_client', 'target_client'])
    if not flag:
        return '参数不合法', 400
    pro_name: str = request.args.get('pro_name')
    iter_num: str = request.args.get('iter_num')
    origin_client: str = request.args.get('origin_client')
    target_client: str = request.args.get('target_client')
    param_dict = {'pro_name': pro_name, 'iter_num': iter_num,
                  'origin_client': origin_client, 'target_client': target_client}
    insert_data = {}
    insert_data.update(param_dict)
    res = mongo.db.encrypted_weight.find_one(param_dict)
    if res:
        return "encrypted weight has already been saved", 200
    else:
        content = json.loads(request.data)
        insert_data.update(content)
        mongo.db.encrypted_weight.insert_one(insert_data)
        return "successfully save encrypted weight!", 200

@app.route('/getEncryptedWeight', methods=['GET'])
def get_gradient():
    flag = check_params(request, ['pro_name', 'iter_num', 'origin_client', 'target_client'])
    if not flag:
        return '参数不合法', 400
    pro_name: str = request.args.get('pro_name')
    iter_num: str = request.args.get('iter_num')
    origin_client: str = request.args.get('origin_client')
    target_client: str = request.args.get('target_client')
    param_dict = {'pro_name': pro_name, 'iter_num': iter_num,
                  'origin_client': origin_client, 'target_client': target_client}
    # 查看key是否已经生成 已经生成返回
    res = mongo.db.encrypted_weight.find_one(param_dict)
    output = {}
    output.update(param_dict)
    if res:
        output['content'] = res['content']
        return jsonify(output)
    else:
        return "corresponding encrypted weight has not been saved yet!", 404


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)