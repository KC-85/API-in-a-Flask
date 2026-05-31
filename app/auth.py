from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import resources
from utils.security_utils import SecurityEnhancements  # ✅ Import security module
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """ Registers a new user """
    data = request.get_json() or {}
    username, password = data.get("username"), data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    try:
        username = SecurityEnhancements.validate_input(username)
        password = SecurityEnhancements.validate_input(password)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if any(user["username"] == username for user in resources["users"]):
        return jsonify({"error": "User already exists"}), 409

    new_user = {
        "id": len(resources["users"]) + 1,
        "username": username,
        "role": "user",
        "password_hash": generate_password_hash(password),
    }
    resources["users"].append(new_user)
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """ Authenticates a user and returns a JWT token """
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:  # ✅ Prevent `NoneType` issue
        return jsonify({"error": "Username and password required"}), 400

    try:
        username = SecurityEnhancements.validate_input(username)
        password = SecurityEnhancements.validate_input(password)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    user = next((user for user in resources["users"] if user["username"] == username), None)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user.get("password_hash", ""), password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)
