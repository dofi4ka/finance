from flask import Blueprint, request, jsonify
import hashlib
from models import Users, Transactions, Targets, db
from utils import response, get_company_price, check_token

invest_page = Blueprint('invest_page', __name__)
@invest_page.route('/invest', methods=['POST'])
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
    }

    transactions = Transactions.query.filter_by(user_id=user_id, type="Инвестиции").all()
    total_invest = -sum(transactions)
    sber = get_company_price("Сбер")
    lukoil = get_company_price("Лукойл")
    gazprom = get_company_price("Газпром")


    return response(True, data={
        'total_invest': total_invest,
    })