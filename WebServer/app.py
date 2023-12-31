from flask import Flask, send_file, request, redirect, render_template
from flask_cors import CORS

from utils import token_decode
from users import users_api
from transactions import transactions_api

from models import db, Users, Transactions, Targets

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db.init_app(app)
app.register_blueprint(users_api, url_prefix="/users")
app.register_blueprint(transactions_api, url_prefix="/transactions")


@app.route('/login', methods=['GET'])
def login():
    token = request.cookies.get("Authorisation")
    if token:
        user_id = token_decode(token)
        if user_id:
            return redirect("/")
    return send_file('login.html')


@app.route('/', methods=['GET'])
def index():
    token = request.cookies.get("Authorisation")
    if token:
        user_id = token_decode(token)
        if user_id:
            user = Users.query.filter_by(user_id=user_id).first()
            transactions = Transactions.query.filter_by(user_id=user_id).all()
            balance = 0

            def c_add(base, amount, category):
                for i in range(len(base)):
                    if base[i]["category"] == category:
                        base[i]["amount"] += amount
                        return
                base.append({"category": category, "amount": amount})

            amount_investments = 0
            c_incomes = []
            incomes = 0
            c_expenses = []
            expenses = 0
            for transaction in transactions:

                balance += transaction.amount
                if transaction.amount > 0:
                    incomes += transaction.amount
                    c_add(c_incomes, transaction.amount, transaction.category)
                else:
                    if transaction.category == "Инвестиции":
                        amount_investments -= transaction.amount
                    expenses -= transaction.amount
                    c_add(c_expenses, -transaction.amount, transaction.category)

            m = max(incomes, expenses)
            if m:
                h1 = incomes / m * 100
                if h1 < 4: h1 = 4
                h2 = expenses / m * 100
                if h2 < 4: h2 = 4
            else:
                h1, h2 = 4, 4

            targets = Targets.query.filter_by(user_id=user_id).all()
            targets_data = [
                {'name': targets.name, 'progress': f"{targets.amount}₽/{targets.price}₽"} for target in targets]

            return render_template('index.html',
                                   name=user.name,
                                   username=user.username,
                                   balance=f"{balance}₽",
                                   fast_actions=[],  # [{"name": None, "action": None}],
                                   targets=[],  # [{"name": None, "progress": None}],
                                   graphs=[
                                       {"class": "graph-income", "h1": 4, "h2": 4, "month": "Июль"},
                                       {"class": "graph-income", "h1": 4, "h2": 4, "month": "Август"},
                                       {"class": "graph-income", "h1": 4, "h2": 4, "month": "Сентябрь"},
                                       {"class": "graph-income", "h1": 4, "h2": 4, "month": "Октябрь"},
                                       {"class": "graph-income" if balance >= 0 else "graph-expense",
                                        "h1": h1, "h2": h2, "month": "Ноябрь"}
                                   ],
                                   c_incomes=c_incomes,
                                   c_expenses=c_expenses,
                                   ratio_str="Неизвестно",
                                   ratio_bar=0,
                                   personal_suggestions=["Мы пока ничего не можем предложить"],
                                   is_followed=False,
                                   popular_investments=[
                                       {"logo": "", "name": "Роснефть", "change": "583.30₽ (+1,84%)"},
                                       {"logo": "", "name": "Лукойл", "change": "7 225.50₽ (+1,26%)"},
                                       {"logo": "", "name": "Сбербанк", "change": "281.60₽ (+0,68%)"},
                                   ],
                                   amount_investments=f"{balance}₽",
                                   friends=[{"logo": "", "name": "У вас пока нет друзей", "ratio_str": ""}]
                                   )
    return redirect("/login")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0")
