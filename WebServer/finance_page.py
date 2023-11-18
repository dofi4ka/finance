import json
from flask import Blueprint, request, jsonify
from models import Users, Transactions
from utils import response, token_encode, check_token
from datetime import datetime
from sqlalchemy import func
from collections import defaultdict

finance_api = Blueprint('finance_api', __name__)

def analyze(transactions):
    income = []
    expenses = []

    for transaction in transactions:
        if transaction.amount >= 0:
            income.append({
                'user_id': transaction.user_id,
                'amount': transaction.amount,
                'category': transaction.category,
                'timestamp': transaction.timestamp
            })
        else:
            expenses.append({
                'user_id': transaction.user_id,
                'amount': transaction.amount,
                'category': transaction.category,
                'timestamp': transaction.timestamp
            })

    income_dict = defaultdict(float)
    for inc in income:
        income_dict[inc['category']] += float(inc['amount'])

    expenses_dict = defaultdict(float)
    for ex in expenses:
        expenses_dict[ex['category']] += float(ex['amount'])

    expenses_dict = dict(sorted(expenses_dict.items(), key=lambda item: item[1], reverse=True))
    income_dict = dict(sorted(income_dict.items(), key=lambda item: item[1], reverse=True))

    top10_expenses = dict(list(expenses_dict.items())[:10])
    top10_income = dict(list(income_dict.items())[:10])

    current_year = datetime.now().year

    transactions_by_month = Transactions.query.with_entities(
        func.extract('month', Transactions.timestamp).label('month'),
        func.sum(Transactions.amount).label('total_amount')
    ).filter(
        func.extract('year', Transactions.timestamp) == current_year
    ).group_by(
        func.extract('month', Transactions.timestamp)
    ).order_by(
        func.extract('month', Transactions.timestamp)
    ).all()

    s = []
    for month, total_amount in transactions_by_month:
        s.append(f"Месяц {month}: {total_amount} руб.")

    return jsonify({
        'expences_per_month': s,
        'top_10_income': top10_income,
        'top_10_expenses': top10_expenses
    })

@finance_api.route('/finance', methods=['POST'])
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
    tt = analyze(transactions)

    return response(True, data={
        'user_data': user_data,
        'username': user.username,
        'email': user.email,
        '123': tt
    })
