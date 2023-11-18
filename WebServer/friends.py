from flask import Blueprint, request

from utils import *
from models import Users, Friends, db

friends_api = Blueprint('friends_api', __name__)


def add_friend(user_id, friend_id):
    new_friend = Friends(user_id=user_id, friend_id=friend_id)
    db.session.add(new_friend)
    db.session.commit()


# Добавляем друга
@friends_api.route('/add', methods=['POST'])
def add_friend():
    data = request.get_json()
    user_id = data.get('user_id')
    token = data.get('token')
    friend_id = data.get('friend_id')

    # авторизация
    if token_decode(token) != user_id:
        return response(False, "Invalid token")

    new_friend = Friends(user_id=user_id, friend_id=friend_id)
    db.session.add(new_friend)
    db.session.commit()

    return response(True, "Friend successfully added")


# Получаем писок друзей пользвоателя
@friends_api.route('/get', methods=['GET'])
def get_friends():
    data = request.get_json()
    user_id = data.get('user_id')
    token = data.get('token')

    # авторизация
    if token_decode(token) != user_id:
        return response(False, "Invalid token")

    friends = db.session.query(Friends, Users).join(Users,
                                                    Friends.friend_id == Users.id).filter(
        Friends.user_id == user_id).all()
    friends_data = [
        {'username': friend.Users.username, 'email': friend.Users.email,
         'name': friend.Users.name} for friend in friends]
    return response(True, data={'friends': friends_data})