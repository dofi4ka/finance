from flask import Blueprint, request, jsonify
import hashlib
from models import Users, Transactions, Targets, db
from utils import response, token_encode, check_token

page_3 = Blueprint('page_3', __name__)


@page_3.route('/home', methods=['POST'])
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
        'ratio': user.ratio,
    }
    """ЗДЕСЬ ДОБАВЛЯЕМ ТО, ЧТО СКИНЕТ ГОША"""
    return response(True, data={
        'user_data': user_data,
        'transactions_data': transactions_data,
        'targets_data': targets_data
    })
