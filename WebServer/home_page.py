from flask import Blueprint, request, jsonify
from models import Users, Transactions, Targets
from utils import response, token_encode, check_token

home_page = Blueprint('home_page', __name__)


@home_page.route('/home', methods=['POST'])
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
    transactions_data = [
        {'user_id': transaction.user_id, 'amount': transaction.amount,
         'category': transaction.category, 'timestamp': transaction.timestamp}
        for
        transaction in transactions]

    targets = Targets.query.filter_by(user_id=user_id).all()
    targets_data = [
        {'user_id': targets.user_id, 'name': targets.name,
         'amount': targets.amount, 'price': targets.price,
         'timestamp': target.timestamp} for target in targets]

    return response(True, data={
        'user_data': user_data,
        'transactions_data': transactions_data,
        'targets_data': targets_data
    })
