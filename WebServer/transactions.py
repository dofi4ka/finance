from flask import Blueprint, request
from datetime import datetime

from utils import *
from models import Transactions, db

transactions_api = Blueprint('transactions_api', __name__)

# Добавляем новую транзакцию
@transactions_api.route('/add', methods=['POST'])
def add_transaction():
    data = request.get_json()
    user_id = data.get('user_id')
    token = data.get('token')
    amount = data.get('amount')
    category = data.get('category')

    # авторизация
    check_token(user_id, token)

    new_transaction = Transactions(user_id=user_id, amount=amount, category=category, timestamp=datetime.utcnow())
    db.session.add(new_transaction)
    db.session.commit()

    return response(True)

# Получаем список транзакций пользователя
@transactions_api.route('/get', methods=['POST'])
def get_transactions():
    data = request.get_json()
    user_id = data.get('user_id')
    token = data.get('token')

    # авторизация
    check_token(user_id, token)

    transactions = Transactions.query.filter_by(user_id=user_id).all()
    transaction_list = [
        {'user_id': transaction.user_id, 'amount': transaction.amount,
         'category': transaction.category, 'timestamp': transaction.timestamp} for
        transaction in transactions]
    return response(True, data={'transactions': transaction_list})
