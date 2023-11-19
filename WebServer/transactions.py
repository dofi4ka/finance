from flask import Blueprint, request, redirect
from datetime import datetime

from utils import *
from models import Transactions, db

transactions_api = Blueprint('transactions_api', __name__)


# Добавляем новую транзакцию
@transactions_api.route('/add', methods=['POST'])
def add_transaction():
    token = request.cookies.get("Authorisation")
    if token:
        user_id = token_decode(token)
        if user_id:
            data = request.get_json()
            amount = data.get('amount')
            category = data.get('category')

            new_transaction = Transactions(user_id=user_id, amount=amount, category=category, timestamp=datetime.utcnow())
            db.session.add(new_transaction)
            db.session.commit()

            return response(True), 200
    return response(False), 403


# Получаем список транзакций пользователя
@transactions_api.route('/get', methods=['POST'])
def get_transactions():
    token = request.cookies.get("Authorisation")
    if token:
        user_id = token_decode(token)
        if user_id:
            transactions = Transactions.query.filter_by(user_id=user_id).all()
            transaction_list = [
                {'user_id': transaction.user_id, 'amount': transaction.amount,
                 'category': transaction.category, 'timestamp': transaction.timestamp} for
                transaction in transactions]
            return response(True, data={'transactions': transaction_list})
