from flask import Blueprint, request, jsonify, redirect
import hashlib
from models import Users, Friends, db
from utils import response, token_encode, check_token, token_decode

users_api = Blueprint('users_api', __name__)


def hash_password(password):
    salt = "unique_salt"
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return password_hash


def add_user(username, password, email, name):
    password_hash = hash_password(password)
    new_user = Users(username=username, password=password_hash, email=email, name=name)
    db.session.add(new_user)
    db.session.commit()


# Регистрация и получение токена
@users_api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    name = data.get('name')

    username_query = Users.query.filter_by(username=username).first()
    email_query = Users.query.filter_by(email=email).first()

    if not username_query and not email_query:
        add_user(username, password, email, name)
        user = Users.query.filter_by(email=email, username=username).first()
        return response(True, data={'token': token_encode(user.user_id)})
    elif email_query:
        return response(False, "Email уже занят!")
    else:
        return response(False, "Username уже занят!")


# Вход и получение токена
@users_api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    password_hash = hash_password(password)
    user = Users.query.filter_by(username=username, password=password_hash).first()

    if user:
        token = token_encode(user.user_id)
        return response(True, "Ok", data={'user_id': user.user_id, 'token': token}), 200
    else:
        return response(False, "Invalid password or username"), 401


# Получаем список пользователей. Функция временная на период теста
@users_api.route('/get_users', methods=['GET'])
def get_users():
    users = Users.query.all()
    user_list = [{'id': user.user_id, 'username': user.username, 'email': user.email, 'name': user.name} for user in users]
    return jsonify({'users': user_list})

"""@users_api.route('/head', methods=['GET'])
def get_head():
    data = request.get_json()
    user_id = data.get('user_id')
    token = data.get('token')

    # авторизация
    check_token(user_id, token)

    user = Users.query.filter_by(user_id=user_id).first_or_404()
    return response(True, data={
        'name': user.name,
        'username': user.username,
    })


@users_api.route('/profile', methods=['POST'])
def get_profile():
    data = request.get_json()
    user_id = data.get('user_id')
    token = data.get('token')

    # авторизация
    check_token(user_id, token)

    user = Users.query.filter_by(user_id=user_id).first_or_404()
    return response(True, data={
        'name': user.name,
        'username': user.username,
        'email': user.email,
    })"""



