from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import create_transaction, list_transactions, get_transaction_by_id, update_transaction_status, get_contractors, get_statuses, get_system_accounts, get_user_id_by_username
from models import Transaction, Contractor, TransactionStatus, SystemAccount
from schemas import TransactionRead

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/contractors', methods=['GET'])
@jwt_required()
def get_contractors_endpoint():
    contractors = get_contractors()
    return [{'id': c.id, 'name': c.name} for c in contractors]

@transactions_bp.route('/statuses', methods=['GET'])
@jwt_required()
def get_statuses_endpoint():
    statuses = get_statuses()
    return [{'id': s.id, 'name': s.name} for s in statuses]

@transactions_bp.route('/accounts', methods=['GET'])
@jwt_required()
def get_system_accounts_endpoint():
    accounts = get_system_accounts()
    return [{'id': a.id, 'name': a.name, 'balance': float(a.balance)} for a in accounts]

@transactions_bp.route('', methods=['POST'])
@jwt_required()
def create_transaction_endpoint():
    data = request.json
    username = get_jwt_identity()
    user_id = get_user_id_by_username(username)
    if not user_id:
        return jsonify({'message': 'User not found'}), 404
    
    contractor_id = data.get('contractor_id')
    type = data.get('type')
    amount = data.get('amount')
    account_id = data.get('account_id')
    
    if not all([contractor_id, type, amount, account_id]):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        tx = create_transaction(user_id, contractor_id, type, amount, account_id)
        return TransactionRead.model_validate(tx).model_dump(), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@transactions_bp.route('', methods=['GET'])
@jwt_required()
def list_transactions_endpoint():
    sort_by = request.args.get('sort_by', 'date')
    sort_order = request.args.get('sort_order', 'desc')
    search = request.args.get('search')
    txs = list_transactions(sort_by, sort_order, search)
    return [TransactionRead.model_validate(tx).model_dump() for tx in txs]

@transactions_bp.route('/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction_detail(transaction_id):
    tx = get_transaction_by_id(transaction_id)
    if not tx:
        return jsonify({'message': 'Transaction not found'}), 404
    return TransactionRead.model_validate(tx).model_dump()

@transactions_bp.route('/<int:transaction_id>/status', methods=['PUT'])
@jwt_required()
def update_transaction_status_endpoint(transaction_id):
    data = request.json
    new_status_id = data.get('status_id')
    if not new_status_id:
        return jsonify({'message': 'Missing status_id'}), 400
    tx = update_transaction_status(transaction_id, new_status_id)
    if not tx:
        return jsonify({'message': 'Transaction not found'}), 404
    return TransactionRead.model_validate(tx).model_dump() 