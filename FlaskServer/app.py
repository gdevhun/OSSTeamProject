# app.py
from flask import Flask, request, jsonify
import json
import os
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)

# Firebase Admin 초기화
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")  # 서비스 계정 키 파일의 경로
firebase_admin.initialize_app(cred)

# 데이터 받기
@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.get_json()
    id_token = data.get('idToken')

    if not id_token:
        return jsonify({"status": "error", "message": "ID token is required."}), 400

    try:
        # 토큰 검증
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        user_name = decoded_token.get('name')
        user_email = decoded_token.get('email')
    except Exception as e:
        return jsonify({"status": "error", "message": "Invalid ID token."}), 401

    # 검증된 사용자 정보 출력
    print(f"Received data: {data}")
    print(f"Decoded token: userId={user_id}, userName={user_name}, userEmail={user_email}")

    # 사용자 ID를 파일 이름으로 설정하여 데이터를 JSON 파일로 저장
    json_file_path = f'{user_id}.json'
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return jsonify({"status": "success", "received_data": data})

# 저장된 JSON 파일을 읽어오기
@app.route('/read_data/<user_id>', methods=['GET'])
def read_data(user_id):
    json_file_path = f'{user_id}.json'
    
    if not os.path.exists(json_file_path):
        return jsonify({"status": "error", "message": "No data file found for the given user ID."}), 404

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    return jsonify({"status": "success", "data": data})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
