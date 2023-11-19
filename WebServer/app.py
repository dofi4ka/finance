from flask import Flask, send_file
from flask_cors import CORS

from home_page import home_page
from users import users_api
from friends import friends_api
from transactions import transactions_api
from finance_page import finance_api
from page_3 import page_3
from invest_page import invest_page

from models import db

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db.init_app(app)
app.register_blueprint(home_page)
app.register_blueprint(users_api, url_prefix="/users")
app.register_blueprint(friends_api, url_prefix="/friends")
app.register_blueprint(transactions_api, url_prefix="/transactions")
app.register_blueprint(finance_api)
app.register_blueprint(page_3)
app.register_blueprint(invest_page)


@app.route('/login', methods=['GET'])
def login():
    return send_file('login.html')


@app.route('/', methods=['GET'])
def index():
    return send_file('home.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
