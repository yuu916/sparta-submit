from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
import requests
import json

ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.bwwoewj.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/auth", methods=["POST"])
def auth_post():
    authKey_receive = request.form['authKey']
    authKeyId_receive = request.form['authKeyId']
    headers = {'Content-Type': 'application/json'}

    data = {
        'authKey' : authKey_receive,
        'authKeyId' : authKeyId_receive
    }
    #soracomのauth APIをCall
    response = requests.post('https://api.soracom.io/v1/auth', headers=headers, data=json.dumps(data))
    # HTTPステータスコードの取得
    status_code = response.status_code
    # レスポンスボディの取得
    response_text = response.text

    if status_code == 200: #認証に成功
        auth_data = response.json()

        # doc = {
        #     'authKey' : authKey_receive,
        #     'authKeyId' : authKeyId_receive,
        #     'apiKey':auth_data['apiKey'],
        #     'token':auth_data['token'],
        #     'userName':auth_data['userName'],
        #     'operatorId':auth_data['operatorId']
        # }
        # db.auth.insert_one(doc)

        json_data = {
            'msg':'200:認証に成功しました。',
            'apiKey':auth_data['apiKey'],
            'token':auth_data['token']
        }
        return jsonify(json_data)

    else:
        return jsonify({
            'msg':'401:認証に失敗しました。'
        })

@app.route("/deviceList", methods=["POST"])
def get_devliceList():
    apiKey_receive = request.form['apiKey']
    token_receive = request.form['token']
    headers = {
    'accept': 'application/json',
    'X-Soracom-API-Key':apiKey_receive,
    'X-Soracom-Token':token_receive
    }
    response = requests.get('https://api.soracom.io/v1/sora_cam/devices', headers=headers)
    # HTTPステータスコードの取得
    status_code = response.status_code
    # レスポンスボディの取得
    response_text = response.text

    if status_code == 200: #認証に成功
        json_data = response.json()
        return jsonify(json_data)

    else:
        return jsonify({
            'msg':'APIリクエストに失敗しました。'
        })
    
@app.route("/liveStream", methods=["POST"])
def get_liveStreamData():
    apiKey_receive = request.form['apiKey']
    token_receive = request.form['token']
    deviceId_receive = request.form['deviceId']
    url = f'https://api.soracom.io/v1/sora_cam/devices/{deviceId_receive}/stream'

    headers = {
    'accept': 'application/json',
    'X-Soracom-API-Key':apiKey_receive,
    'X-Soracom-Token':token_receive
    }

    response = requests.get(url, headers=headers)
    status_code = response.status_code
    response_text = response.text

    if status_code == 200: #認証に成功
        json_data = response.json()
        return jsonify(json_data)
    else:
        return jsonify({
            'msg':'APIリクエストに失敗しました。'
        })

@app.route("/getImage", methods=["POST"])
def get_imageData():
    apiKey_receive = request.form['apiKey']
    token_receive = request.form['token']
    deviceId_receive = request.form['deviceId']
    url = f'https://api.soracom.io/v1/sora_cam/devices/events?device_id={deviceId_receive}&limit=1&sort=desc' #get only 1 picture

    headers = {
    'accept': 'application/json',
    'X-Soracom-API-Key':apiKey_receive,
    'X-Soracom-Token':token_receive
    }

    response = requests.get(url, headers=headers)
    status_code = response.status_code
    response_text = response.text

    if status_code == 200: #認証に成功
        json_data = response.json()
        return jsonify(json_data)
    else:
        return jsonify({
            'msg':'APIリクエストに失敗しました。'
        })


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)