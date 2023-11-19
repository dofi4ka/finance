from flask import Blueprint, request, jsonify
import hashlib
from models import Users, Friends
from utils import response, get_company_price, check_token, get_user_ratio

friends_rating_page = Blueprint('friends_rating_page', __name__)
@friends_rating_page.route('/friends_rating', methods=['POST'])
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

    friends_list = Friends.query.filter_by(user_id=user_id).all()
    friends_dict = {}
    for friend in friends_list:
        user = Users.query.filter_by(user_id=friend).first_or_404()
        friends_dict[user.username] = user.ratio
    friends_dict = dict(
        sorted(friends_dict.items(), key=lambda item: item[1], reverse=True))
    for friend in friends_dict.keys():
        friends_dict[friend] = get_user_ratio(friends_list[friend])





    # return response(True, data={
    #     'total_invest': total_invest,
    # })