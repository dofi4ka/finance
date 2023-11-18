from flask import jsonify
import jwt


def response(status, message=None, data=None):
    return jsonify({'status': status, 'message': message, 'data': data})


secret = "secret key"


def token_encode(user_id):
    return jwt.encode({'user_id': user_id}, secret, algorithm='HS256')


def token_decode(
        token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1fQ.Yyik3alxPaYrd-pYQ5cKLoAkUyx6xcUZQkeVDRAQYzs'):
    try:
        message = jwt.decode(token, key=secret, algorithms=["HS256"])
        return message["user_id"]
    except Exception as e:
        print(e)


def check_token(user_id, token):
    try:
        if int(token_decode(token)) != int(user_id):
            return response(False, "Invalid token")
    except Exception as e:
        return response(False, "Invalid token")
    return response(True, "Ok")
