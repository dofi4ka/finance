from flask import Blueprint, request

from utils import *
from models import Users, Friends, db
from sqlalchemy.orm import joinedload

friends_api = Blueprint('friends_api', __name__)


# Переписанный код для добавления друга
@friends_api.route('/add', methods=['POST'])
def add_friend():
    data = request.get_json()
    user_id = data.get('user_id')
    token = data.get('token')
    friend_id = data.get('friend_id')

    # авторизация
    if token_decode(token) != user_id:
        return response(False, "Invalid token"), 500

    # Проверка наличия записи в базе данных
    existing_friendship_1 = Friends.query.filter_by(user_id=user_id, friend_id=friend_id).first()
    existing_friendship_2 = Friends.query.filter_by(user_id=friend_id, friend_id=user_id).first()

    if existing_friendship_1 or existing_friendship_2:
        return response(False, "Friendship already exists"), 400

    new_friend = Friends(user_id=user_id, friend_id=friend_id)
    db.session.add(new_friend)
    db.session.commit()

    return response(True, "Friend successfully added"), 200


# Переписанный код для получения списка друзей пользователя
@friends_api.route('/get', methods=['POST'])
def get_friends():
    data = request.get_json()
    user_id = data.get('user_id')
    token = data.get('token')

    # Проверка наличия данных
    if not user_id or not token:
        return response(False, "Отсутствует user_id или token")

    # авторизация
    r = check_token(user_id, token)
    if r:
        return r

    # Запрос списка друзей
    friends = (
        db.session.query(Users)
        .join(Friends, Friends.friend_id == Users.user_id)
        .filter(Friends.user_id == user_id)
        .options(joinedload(
            Users.friends))  # Загрузка связанных объектов Users.friends
        .all()
    )

    friends_data = [
        {'username': friend.username, 'email': friend.email,
         'name': friend.name}
        for friend in friends
    ]

    return response(True, data={'friends': friends_data}), 200
