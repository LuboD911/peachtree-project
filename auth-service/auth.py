from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
)
from db import get_user_by_username, create_user, delete_user, store_refresh_token, revoke_refresh_token, is_refresh_token_revoked
from passlib.hash import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password required'}), 400
    if get_user_by_username(data['username']):
        return jsonify({'message': 'User already exists'}), 409
    create_user(data['username'], data['password'])
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password required'}), 400
    user = get_user_by_username(data['username'])
    if user and bcrypt.verify(data['password'], user.password):
        additional_claims = {"username": user.username, "key": "my-client-key"}
        access_token = create_access_token(identity=user.username, additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=user.username)
        store_refresh_token(user.username, refresh_token)
        return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    jti = get_jwt()['jti']
    raw_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if is_refresh_token_revoked(raw_token):
        return jsonify({'msg': 'Refresh token revoked'}), 401
    additional_claims = {"username": current_user, "key": "my-client-key"}
    new_access_token = create_access_token(identity=current_user, additional_claims=additional_claims)
    return jsonify({'access_token': new_access_token})

@auth_bp.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
def logout():
    raw_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    revoke_refresh_token(raw_token)
    return jsonify({'msg': 'Logged out and refresh token revoked'})

@auth_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    username = get_jwt_identity()
    if not get_user_by_username(username):
        return jsonify({'message': 'User not found'}), 404
    delete_user(username)
    return jsonify({'message': 'User deleted successfully'}) 