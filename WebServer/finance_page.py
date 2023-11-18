from flask import Blueprint, request, jsonify
import hashlib
from models import Users, Transactions, db
from utils import response, token_encode, check_token

from app import app


def analyze(transactions):
    # Колхоз, потом нормально сделаю
    income = []
    expenses = []
    for transaction in transactions:
        if transaction.amount >= 0:
            income.append(
                {'user_id': transaction.user_id, 'amount': transaction.amount,
                 'category': transaction.category,
                 'timestamp': transaction.timestamp})
        else:
            expenses.append(
                {'user_id': transaction.user_id, 'amount': transaction.amount,
                 'category': transaction.category,
                 'timestamp': transaction.timestamp})
    income_dict = {}
    for inc in income:
        if not inc["category"] in income_dict:
            income_dict["category"] = 0
        income_dict["category"] += inc["amount"]

    expenses_dict = {}
    for ex in expenses:
        if not ex["category"] in expenses_dict:
            expenses_dict["category"] = 0
        expenses_dict["category"] += ex["amount"]

    """По этим данным строим диаграммы и выводим топ трат"""


@app.route('/finance', methods=['POST'])
def get_home_page():
    data = request.get_json()
    user_id = data.get('user_id')
    token = data.get('token')

    # авторизация
    check_token(user_id, token)

    user = Users.query.filter_by(user_id=user_id).first_or_404()
    user_data = {
        'name': user.name,
        'username': user.username,
        'email': user.email,
    }

    transactions = Transactions.query.filter_by(user_id=user_id).all()
    analyze(transactions)

    return response(True, data={
        'user_data': user_data,
        'username': user.username,
        'email': user.email,
    })
