from flask import jsonify
import jwt


def response(status, message=None, data=None):
    return jsonify({'status': status, 'message': message, 'data': data})


secret = "secret key"


def token_encode(user_id):
    return jwt.encode({'user_id': user_id}, secret, algorithm='HS256')


def token_decode(token):
    try:
        message = jwt.decode(token, key=secret, algorithms=["HS256"])
        return message["user_id"]
    except Exception as e:
        return None
