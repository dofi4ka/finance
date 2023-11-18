from flask import Blueprint, request

from utils import *
import hashlib
from models import Users, Friends, db

users_api = Blueprint('users_api', __name__)


def hash_password(password):
    salt = "unique_salt"
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return password_hash


def add_user(username, password, email, name):
    password_hash = hash_password(password)
    new_user = Users(username=username, password=password_hash, email=email,
                     name=name)
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
        return response(True)
    elif email_query:
        return response(False, "Email already taken")
    else:
        return response(False, "Username already taken")


# Вход и получение токена
@users_api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    password_hash = hash_password(password)
    user = Users.query.filter_by(username=username,
                                 password=password_hash).first()
    if user:
        token = token_encode(user.user_id)
        return response(True, data={'token': token})
    else:
        return response(False, "Invalid password or username"), 401


# Получаем список пользователей. Функция временная на период теста
@users_api.route('/get_users', methods=['GET'])
def get_users():
    users = Users.query.all()
    user_list = [
        {'id': user.user_id, 'username': user.username, 'email': user.email,
         'name': user.name} for user in users]
    return jsonify({'users': user_list})
