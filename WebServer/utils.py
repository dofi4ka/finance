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


def get_company_price(company_name):
    import requests

    url = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json'

    response = requests.get(url)

    jj = response.json()
    jjj = jj["securities"]["data"]

    for l in jjj:
        if company_name in l[9]:
            data = {
                'ticker': l[0],
                'price': l[3],
                'full_name': l[9]
            }
            return jsonify(data)


def get_user_ratio(ratio):
    categories_dict = {
        "1-0.95": "Великолепно",
        "0.94-0.93": "Отлично",
        "0.92-0.9": "Замечательно",
        "0.89-0.81": "Хорошо",
        "0.8-0.7": "Выше среднего",
        "0.69-0.58": "Нормально",
        "0.57-0.5": "Допустимо",
        "0.49-0.44": "Надо стараться",
        "0.43-0.31": "Плохо",
        "0.3-0": "Хуже некуда"
    }

    result_category = None
    for key, value in categories_dict.items():
        end, start = map(float, key.split('-'))
        if start <= ratio <= end:
            result_category = value
            break

    return result_category