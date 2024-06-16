# app/signup.py

from flask import Blueprint, request, jsonify, current_app

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        print("Received request data:", data)
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({"status": "failed", "message": "Email and password required"}), 400
        auth = current_app.config['auth']
        user = auth.create_user_with_email_and_password(email, password)
        return jsonify({"status": "success", "data": user}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"status": "failed", "message": str(e)}), 400
