from flask import Blueprint, request, redirect

from utils import *
from models import Users, Friends, db
from sqlalchemy.orm import joinedload

friends_api = Blueprint('friends_api', __name__)


# Переписанный код для добавления друга
@friends_api.route('/add', methods=['POST'])
def add_friend():
    if "Authorisation" in request.headers:
        if token_decode(request.headers):
            return redirect("/")

    data = request.get_json()
    user_id = data.get('user_id')
    friend_id = data.get('friend_id')

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
    if "Authorisation" in request.headers:
        if token_decode(request.headers):
            return redirect("/")

    data = request.get_json()
    user_id = data.get('user_id')

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
        {'username': friend.username, 'name': friend.name}
        for friend in friends
    ]

    return response(True, data={'friends': friends_data}), 200
